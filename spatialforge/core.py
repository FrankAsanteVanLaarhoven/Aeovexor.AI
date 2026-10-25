"""SpatialForge: auditable CPU baselines. Inputs are XYZ meters in one declared frame."""
import numpy as np
from scipy.spatial import cKDTree
from scipy.spatial.transform import Rotation
from sklearn.cluster import DBSCAN, OPTICS, KMeans
from sklearn.metrics import adjusted_rand_score

def load_cloud(path, fmt='auto', labels=None):
    from pathlib import Path
    p=Path(path); fmt=p.suffix.lstrip('.').lower() if fmt=='auto' else fmt
    if fmt=='npy':
        a=np.load(p,allow_pickle=False)
    elif fmt=='npz':
        with np.load(p,allow_pickle=False) as f:
            a=f['xyz']; gt=f['labels'] if 'labels' in f else None
    elif fmt in ('bin','kitti'):
        raw=np.fromfile(p,dtype='<f4')
        if raw.size%4: raise ValueError('KITTI scan requires float32 XYZI')
        a=raw.reshape(-1,4)
    elif fmt in ('pcd','ply'):
        try: import open3d as o3d
        except ImportError as e: raise RuntimeError('Install open3d optional dependency') from e
        a=np.asarray(o3d.io.read_point_cloud(str(p)).points)
    else: raise ValueError('Unsupported format')
    a=np.asarray(a,dtype=np.float64)
    if a.ndim!=2 or a.shape[1] not in (3,4) or not np.isfinite(a).all():
        raise ValueError('Expected finite Nx3 or Nx4 cloud')
    gt=locals().get('gt')
    if labels:
        gt=np.fromfile(labels,dtype='<u4') & 0xffff # SemanticKITTI semantic labels
    if gt is not None and len(gt)!=len(a): raise ValueError('Label count mismatch')
    return a[:,:3],gt

def voxel(x,step):
    if step<=0: raise ValueError('voxel size must be >0')
    if not len(x): return np.empty((0,3))
    _,inv=np.unique(np.floor(x/step).astype('int64'),axis=0,return_inverse=True)
    sums=np.zeros((inv.max()+1,3)); np.add.at(sums,inv,x)
    return sums/np.bincount(inv)[:,None]

def pca(x,k=16):
    if len(x)<3: raise ValueError('Need >=3 points')
    _,ids=cKDTree(x).query(x,k=min(max(k,3),len(x)))
    y=x[ids]; y-=y.mean(axis=1,keepdims=True)
    eig=np.linalg.eigvalsh(np.einsum('nki,nkj->nij',y,y)/y.shape[1])
    return {'curvature':eig[:,0]/np.maximum(eig.sum(1),1e-12),
            'linearity':(eig[:,2]-eig[:,1])/np.maximum(eig[:,2],1e-12),
            'planarity':(eig[:,1]-eig[:,0])/np.maximum(eig[:,2],1e-12)}

def cluster(x,method='dbscan',eps=0.5,min_samples=5,n_clusters=2,min_cluster_size=10):
    if not len(x): return np.array([],dtype=int)
    if method=='dbscan': return DBSCAN(eps=eps,min_samples=min_samples).fit_predict(x)
    if method=='optics': return OPTICS(max_eps=eps,min_samples=min(max(min_samples,2),len(x))).fit_predict(x)
    if method=='kmeans': return KMeans(n_clusters=n_clusters,random_state=0,n_init=10).fit_predict(x)
    if method=='hdbscan':
        try: import hdbscan
        except ImportError as e: raise RuntimeError('Install hdbscan optional dependency') from e
        return hdbscan.HDBSCAN(min_cluster_size=min_cluster_size,min_samples=min_samples).fit_predict(x)
    raise ValueError('Unknown method')

def icp(src,dst,max_distance=1.0,iterations=40):
    if min(len(src),len(dst))<3: raise ValueError('Need >=3 points in each cloud')
    T=np.eye(4); tree=cKDTree(dst); rmse=float('inf'); matches=0
    for _ in range(iterations):
        moved=src@T[:3,:3].T+T[:3,3]
        dist,ix=tree.query(moved); mask=dist<=max_distance; matches=int(mask.sum())
        if matches<3: break
        a=moved[mask]; b=dst[ix[mask]]; ac=a.mean(0); bc=b.mean(0)
        u,_,vt=np.linalg.svd((a-ac).T@(b-bc)); R=vt.T@u.T
        if np.linalg.det(R)<0: vt[-1]*=-1; R=vt.T@u.T
        delta=np.eye(4); delta[:3,:3]=R; delta[:3,3]=bc-R@ac
        T=delta@T
        new=float(np.sqrt(np.mean(np.sum((a@R.T+delta[:3,3]-b)**2,axis=1))))
        if abs(rmse-new)<1e-8: rmse=new; break
        rmse=new
    return T,{'inlier_rmse_m':rmse,'fitness':matches/len(src)}

def ari(gt,pred):
    gt=np.asarray(gt); pred=np.asarray(pred)
    if gt.shape!=pred.shape: raise ValueError('Label count mismatch')
    mask=gt!=-1
    if not mask.any(): raise ValueError('No valid ground truth')
    return {'adjusted_rand_index':float(adjusted_rand_score(gt[mask],pred[mask])),
            'predicted_noise_fraction':float(np.mean(pred==-1))}

def miou(gt,pred,ignore=(-1,)):
    gt=np.asarray(gt); pred=np.asarray(pred)
    if gt.shape!=pred.shape: raise ValueError('Label count mismatch')
    mask=~np.isin(gt,ignore); gt=gt[mask]; pred=pred[mask]
    if not len(gt): raise ValueError('No valid ground truth')
    classes=np.unique(gt)
    scores={int(c):float(np.sum((gt==c)&(pred==c))/np.sum((gt==c)|(pred==c))) for c in classes}
    return {'miou':float(np.mean(list(scores.values()))),'per_class_iou':scores}

def load_poses(path,fmt='kitti'):
    a=np.loadtxt(path,comments='#',ndmin=2)
    T=np.repeat(np.eye(4)[None],len(a),axis=0)
    if fmt=='kitti' and a.shape[1]==12: T[:,:3,:]=a.reshape(-1,3,4); return T
    if fmt=='tum' and a.shape[1]==8:
        T[:,:3,3]=a[:,1:4]; T[:,:3,:3]=Rotation.from_quat(a[:,4:8]).as_matrix()
        return T
    raise ValueError('Invalid trajectory file')

def trajectory(est,gt):
    if est.shape!=gt.shape or est.ndim!=3 or est.shape[1:]!=(4,4): raise ValueError('Matched Nx4x4 required')
    if not len(est): raise ValueError('Empty trajectory')
    ate=float(np.sqrt(np.mean(np.sum((est[:,:3,3]-gt[:,:3,3])**2,axis=1))))
    rpe=[]
    for i in range(len(est)-1):
        d=np.linalg.inv(np.linalg.inv(gt[i])@gt[i+1])@(np.linalg.inv(est[i])@est[i+1])
        rpe.append(np.linalg.norm(d[:3,3]))
    return {'ate_rmse_m':ate,'rpe_translation_rmse_m':float(np.sqrt(np.mean(np.square(rpe)))) if rpe else None}

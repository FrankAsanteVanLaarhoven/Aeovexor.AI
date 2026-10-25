import numpy as np
import pytest
from spatialforge.core import cluster,voxel,pca,icp,ari,miou,trajectory,load_cloud

def test_voxel():
    x=np.array([[0,0,0],[.1,0,0],[2,0,0.]])
    assert voxel(x,1).shape==(2,3)
    assert np.allclose(voxel(x,1)[0],[.05,0,0])
def test_pca():
    rng=np.random.default_rng(1); x=rng.normal(size=(40,3))
    assert np.isfinite(pca(x)['curvature']).all()
def test_dbscan():
    rng=np.random.default_rng(2); x=np.r_[rng.normal(0,.03,(30,3)),rng.normal(3,.03,(30,3))]
    pred=cluster(x,eps=.2,min_samples=4)
    assert len(set(pred)-{-1})==2
    assert ari(np.r_[np.zeros(30),np.ones(30)],pred)['adjusted_rand_index']==1.
def test_icp():
    rng=np.random.default_rng(4); a=rng.normal(size=(100,3)); b=a+np.array([.1,-.04,.02])
    T,m=icp(a,b,max_distance=.5)
    assert np.allclose(T[:3,3],[.1,-.04,.02],atol=1e-4)
    assert m['fitness']>.9
def test_metrics():
    assert miou(np.array([0,0,1,1]),np.array([0,0,1,1]))['miou']==1
    p=np.repeat(np.eye(4)[None],3,axis=0)
    assert trajectory(p,p)['ate_rmse_m']==0
def test_reject_invalid(tmp_path):
    p=tmp_path/'bad.npy'; np.save(p,np.array([[np.nan,0,0]]))
    with pytest.raises(ValueError): load_cloud(p)

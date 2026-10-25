from pathlib import Path
import numpy as np
rng=np.random.default_rng(42)
x=np.r_[rng.normal([0,0,0],.05,(80,3)),rng.normal([2,2,2],.05,(80,3))]
y=np.r_[np.zeros(80,dtype=np.int32),np.ones(80,dtype=np.int32)]
p=Path(__file__).resolve().parents[1]/'examples'/'synthetic.npz'
np.savez_compressed(p,xyz=x,labels=y)
print(p)

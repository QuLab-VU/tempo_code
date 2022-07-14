# Setting Up STELLAR Environment

Create conda env
```
conda create -n stellar python=3.8
conda activate stellar
```

Install PyTorch Geometric (using: https://github.com/pyg-team/pytorch_geometric/issues/3574) 
```
conda install -q -y pyg -c pyg
```

Then install cuda enabled version of pytorch: 
```
conda install -q -y pytorch cudatoolkit=11.3 -c pytorch
```

Install other requirements (from cloned: https://github.com/snap-stanford/stellar)
```
pip install -r requirements.txt
```

Set up jupyter kernel
```
conda install ipykernel 
ipython kernel install --user --name=stellar
```

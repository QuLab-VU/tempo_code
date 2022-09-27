## Dropkick Environment Set Up
The following set up was used to run dropkick on a Centos server and conda. See `dropkick` documentation [here](https://github.com/KenLauLab/dropkick#automated-cell-filtering-for-single-cell-rna-sequencing-data)
for additional information.

### Create Conda Environment
Use the `env.yml` follow to create a conda environment named `rna_seq` (name can be changed by editing the first line of the file). 
```bash
conda env create -f env.yml
conda activate scrnaseq
```

Clone the `dropkick` repository
```bash
git clone https://github.com/KenLauLab/dropkick.git
cd dropkick
```

Modify the `setup.py` script to prevent `glmnet` extension from causing installation issues. Comment the following sections:
```python
# lines 63-68
# glmnet_lib = Extension(
#     name="_glmnet",
#     sources=["dropkick/_glmnet.pyf", "dropkick/src/glmnet/glmnet5.f90"],
#     extra_f90_compile_args=f_compile_args,
#     library_dirs=library_dirs,
# )

# line 86 in setup()
# ext_modules=[glmnet_lib],
```

Then run setup script
```bash
python setup.py install
```

Finally, manually install `glmnet` package and create Jupyter kernel
```bash
conda install -c conda-forge glmnet
ipython kernel install --user --name=scrnaseq
```



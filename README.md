# Multimodal Datasets

`mudatasets` provides some public datasets with multimodal data, primarily focosing on multimodal omics datasets.

[MuData library](https://github.com/PMBio/mudata) | [MuData documentation](https://mudata.readthedocs.io/)

## Installation

```
# Stable
pip install mudatasets
# Dev
pip install git+https://github.com/gtca/mudatasets
```

## Getting started

```py
import mudatasets as mds
```

### Find available datasets

```py
mds.list_datasets()
```

### Load a dataset

```py
mdata = mds.load("pbmc10k_multiome")
print(mdata)
```

Some common attributes for `.load()` are:

- `data_dir=` for location to save the dataset (`~/mudatasets/` by default)
- `with_info=True` for also returning the second argument with dataset description as a dictionary (`False` by default)
- `backed=True` for reading data in a backed format, only for `.h5mu` files (`True` by default)

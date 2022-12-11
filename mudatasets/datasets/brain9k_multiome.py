from ..core import MuDataSet
from ..utils import sizefmt


class Brain9kMultiome(MuDataSet):
    """
    Chromatin and gene-regulatory dynamics 
    of the developing human cerebral cortex 
    at single-cell resolution.

    Trevino, ..., Greenleaf, 2021
    DOI: 10.1016/j.cell.2021.07.039
    """

    def __init__(self):
        self.name = "brain9k_multiome"
        self.version = "1.0"
        self.files = [
            {
                "name": "brain9k_multiome_processed.h5mu",
                "url": "https://osf.io/cjsmu/download",
                "md5": "a33e4d13384643f3b1734357aa17ba70",
                "size": 912470998,
                "format": "h5mu",
                "raw": False,
                "processed": True,
            },
            {
                "name": "brain9k_multiome_raw.h5mu",
                "url": "https://osf.io/64bc3/download",
                "md5": "ee946b981d57b9a31e3124280ded063e",
                "size": 3949539614,
                "format": "h5mu",
                "raw": True,
            },
            {
                "name": "GSE162170_multiome_rna_counts.tsv.gz",
                "url": "https://www.ncbi.nlm.nih.gov/geo/download/?acc=GSE162170&format=file&file=GSE162170%5Fmultiome%5Frna%5Fcounts%2Etsv%2Egz",
                "md5": "7283504077be065a86b4e4fb49fa07d0",
                "size": 24845803,
                "format": "tsv.gz",
                "raw": True,
            },
            {
                "name": "GSE162170_multiome_spliced_rna_counts.tsv.gz",
                "url": "https://www.ncbi.nlm.nih.gov/geo/download/?acc=GSE162170&format=file&file=GSE162170%5Fmultiome%5Fspliced%5Frna%5Fcounts%2Etsv%2Egz",
                "md5": "695ff462dc5049500f0f84cfd3ca99ef",
                "size": 11115238,
                "format": "tsv.gz",
                "raw": True,
            },
            {
                "name": "GSE162170_multiome_unspliced_rna_counts.tsv.gz",
                "url": "https://www.ncbi.nlm.nih.gov/geo/download/?acc=GSE162170&format=file&file=GSE162170%5Fmultiome%5Funspliced%5Frna%5Fcounts%2Etsv%2Egz",
                "md5": "b0fd66acd2e98b56e024a2556f24a5de",
                "size": 15622285,
                "format": "tsv.gz",
                "raw": True,
            },
            {
                "name": "GSE162170_multiome_atac_counts.tsv.gz",
                "url": "https://www.ncbi.nlm.nih.gov/geo/download/?acc=GSE162170&format=file&file=GSE162170%5Fmultiome%5Fatac%5Fcounts%2Etsv%2Egz",
                "md5": "c0991a4766d8f5e0c93fe69378069bbf",
                "size": 149865144,
                "format": "tsv.gz",
                "raw": True,
            },
            {
                "name": "GSE162170_multiome_atac_consensus_peaks.txt.gz",
                "url": "https://www.ncbi.nlm.nih.gov/geo/download/?acc=GSE162170&format=file&file=GSE162170%5Fmultiome%5Fatac%5Fconsensus%5Fpeaks%2Etxt%2Egz",
                "md5": "9481374ba303b098ed74286961fa561f",
                "size": 18315449,
                "format": "txt.gz",
                "raw": True,
            },
            {
                "name": "GSE162170_multiome_cell_metadata.txt.gz",
                "url": "https://www.ncbi.nlm.nih.gov/geo/download/?acc=GSE162170&format=file&file=GSE162170%5Fmultiome%5Fcell%5Fmetadata%2Etxt%2Egz",
                "md5": "ab2687f9c01448d07bd0411d8d20b2f4",
                "size": 492098,
                "format": "txt.gz",
                "raw": True,
            },
            {
                "name": "GSE162170_multiome_cluster_names.txt.gz",
                "url": "https://www.ncbi.nlm.nih.gov/geo/download/?acc=GSE162170&format=file&file=GSE162170%5Fmultiome%5Fcluster%5Fnames%2Etxt%2Egz",
                "md5": "07427984630409803b2ac568aaf248c3",
                "size": 278,
                "format": "txt.gz",
                "raw": False,
            },
            {
                "name": "GSE162170_multiome_atac_gene_activities.tsv.gz",
                "url": "https://www.ncbi.nlm.nih.gov/geo/download/?acc=GSE162170&format=file&file=GSE162170%5Fmultiome%5Fatac%5Fgene%5Factivities%2Etsv%2Egz",
                "md5": "4f967ec9929240503c5083c718e80142",
                "size": 831813316,
                "format": "tsv.gz",
                "raw": False,
            },
        ]

        self.total_size_int = sum([f["size"] for f in self.files])
        self.total_size = sizefmt(self.total_size_int)

        self.data = {
            "name": self.name,
            "version": self.version,
            "total_size": self.total_size,
            "files": self.files,
        }
        self.data_versions = [
            self.data,
        ]

        self.info = {
            **self.data,
            "data_versions": self.data_versions,
        }

    def load(self, data_dir="./"):
        from os import path
        import gzip
        from tqdm import tqdm

        import numpy as np
        from scipy.sparse import coo_matrix, csr_matrix
        import pandas as pd
        from mudata import AnnData, MuData

        try:
            import polars as pl
        except ImportError:
            raise ImportError("polars is required for this data loader to read dense count matrices. Install it e.g. with `pip install polars`.")

        try:
            import pyarrow
        except ImportError:
            raise ImportError("pyarrow is required for this data loader to convert polars data frames to pandas data frames. Install it e.g. with `pip install pyarrow`.")

        def read_counts(fname, sep="\t", header=True, index=True, int32=True):
            # make a sparse matrix
            if int32:
                ncol = 0
                with gzip.open(fname) as f:
                    if header:
                        f.readline()
                    ncol = len(f.readline().decode().split("\t"))
                    if index:
                        ncol = ncol - 1
                dtypes = list(np.repeat(pl.datatypes.Int32, ncol))
                if index:
                    dtypes = [str] + dtypes
                df = pl.read_csv(fname, null_values="0", sep=sep, has_header=header, dtypes=dtypes, skip_rows=int(header))
            else:
                df = pl.read_csv(fname, null_values="0", sep=sep, has_header=header, skip_rows=int(header))
            df = df.fill_null(0)
            x = csr_matrix(df[:,int(index):df.shape[1]])

            # define var_names
            if index:
                var_names = list(df[:,0])

            # define obs_names
            if header:
                with gzip.open(fname) as f:
                    obs_names = f.readline().decode().split("\t")

            if index and header:
                adata = AnnData(X=x, obs=pd.DataFrame(index=obs_names), var=pd.DataFrame(index=var_names))
            elif index:
                adata = AnnData(X=x, var=pd.DataFrame(index=var_names))
            elif header:
                adata = AnnData(X=x, obs=pd.DataFrame(index=obs_names))
            else:
                adata = AnnData(X=x)
            return adata

        modalities = dict()
        counts = {"rna": "GSE162170_multiome_rna_counts.tsv.gz", "atac": "GSE162170_multiome_atac_counts.tsv.gz"}
        for m, fname in counts.items():
            fpath = path.join(data_dir, fname)
            modalities[m] = read_counts(fpath, sep="\t")

        # [atac].var
        peaks = pl.read_csv("GSE162170_multiome_atac_consensus_peaks.txt.gz", sep="\t").to_pandas().set_index("name")
        peaks.index.name = None
        modalities['atac'].var = peaks

        # .obs
        metadata = pd.read_csv("GSE162170_multiome_cell_metadata.txt.gz", sep="\t").set_index("Cell.ID")
        metadata.index.name = None
        modalities['atac'].obs_names = metadata.index
        # RNA modality should have cell IDs already

        mdata = MuData(modalities)
        mdata.obs = metadata

        return mdata


def dataset():
    return Brain9kMultiome()

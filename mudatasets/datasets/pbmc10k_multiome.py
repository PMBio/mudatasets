from ..core import MuDataSet
from ..utils import sizefmt


class PBMC10kMultiome(MuDataSet):
    """
    Sorted human granulocytes
    from peripheral blood
    provided by 10X Genomics
    """

    def __init__(self):
        self.name = "pbmc10k_multiome"
        self.version = "1.0.0"
        self.format = "10x_h5"
        self.files = [
            {
                "name": "filtered_feature_bc_matrix.h5",
                "url": "https://cf.10xgenomics.com/samples/cell-arc/1.0.0/pbmc_granulocyte_sorted_10k/pbmc_granulocyte_sorted_10k_filtered_feature_bc_matrix.h5",
                "md5": "920b16bf1e63b6610bf74bf9040ed386",
                "size": 162282142,
                "required": True,
            },
        ]

        self.total_size_int = sum([f["size"] for f in self.files])
        self.total_size = sizefmt(self.total_size_int)

        self.data = {
            "name": self.name,
            "version": self.version,
            "format": self.format,
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


def dataset():
    return PBMC10kMultiome()

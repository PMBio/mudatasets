from ..core import MuDataSet
from ..utils import sizefmt


class Brain3kMultiome(MuDataSet):
    """
    Frozen human healthy brain tissue
    provided by 10X Genomics
    """

    def __init__(self):
        self.name = "brain3k_multiome"
        self.version = "2.0.0"
        self.format = "10x_h5"
        self.files = [
            {
                "name": "filtered_feature_bc_matrix.h5",
                "url": "https://cf.10xgenomics.com/samples/cell-arc/2.0.0/human_brain_3k/human_brain_3k_filtered_feature_bc_matrix.h5",
                "md5": "ba0b765eddb138d6d6294227879b9a9b",
                "size": 68830100,
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
    return Brain3kMultiome()

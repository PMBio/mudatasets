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
        self.url = "https://www.10xgenomics.com/resources/datasets/frozen-human-healthy-brain-tissue-3-k-1-standard-2-0-0"
        self.files = [
            {
                "name": "filtered_feature_bc_matrix.h5",
                "url": "https://cf.10xgenomics.com/samples/cell-arc/2.0.0/human_brain_3k/human_brain_3k_filtered_feature_bc_matrix.h5",
                "md5": "ba0b765eddb138d6d6294227879b9a9b",
                "size": 68830100,
                "format": "10x_h5",
                "raw": True,
            },
            {
                "name": "atac_fragments.tsv.gz",
                "description": "ATAC per fragment information",
                "url": "https://cf.10xgenomics.com/samples/cell-arc/2.0.0/human_brain_3k/human_brain_3k_atac_fragments.tsv.gz",
                "md5": "b1594a4096405128e646e6a275e3ada3",
                "size": 1710609012,
                "raw": True,
            },
            {
                "name": "atac_fragments.tsv.gz.tbi",
                "description": "ATAC per fragment information index",
                "url": "https://cf.10xgenomics.com/samples/cell-arc/2.0.0/human_brain_3k/human_brain_3k_atac_fragments.tsv.gz.tbi",
                "md5": "3054c179689ff025f9e64df6d7a79040",
                "size": 965500,
                "raw": True,
            },
            {
                "name": "atac_peaks.bed",
                "description": "ATAC peak locations",
                "url": "https://cf.10xgenomics.com/samples/cell-arc/2.0.0/human_brain_3k/human_brain_3k_atac_peaks.bed",
                "md5": "55abaab48951b115f696e9255a2da33b",
                "size": 3205172,
                "raw": True,
            },
            {
                "name": "atac_peak_annotation.tsv",
                "description": "ATAC peak annotations based on proximal genes",
                "url": "https://cf.10xgenomics.com/samples/cell-arc/2.0.0/human_brain_3k/human_brain_3k_atac_peak_annotation.tsv",
                "md5": "5c9cde0442444bbc2c4c57c577db6c80",
                "size": 7677885,
                "raw": True,
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


def dataset():
    return Brain3kMultiome()

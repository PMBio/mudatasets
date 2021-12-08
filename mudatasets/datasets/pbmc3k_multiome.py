from ..core import MuDataSet
from ..utils import sizefmt


class PBMC3kMultiome(MuDataSet):
    """
    Sorted human granulocytes
    from peripheral blood
    provided by 10X Genomics
    """

    def __init__(self):
        self.name = "pbmc3k_multiome"
        self.version = "2.0.0"
        self.url = "https://www.10xgenomics.com/resources/datasets/pbmc-from-a-healthy-donor-granulocytes-removed-through-cell-sorting-3-k-1-standard-2-0-0"
        self.files = [
            {
                "name": "filtered_feature_bc_matrix.h5",
                "url": "https://cf.10xgenomics.com/samples/cell-arc/2.0.0/pbmc_granulocyte_sorted_3k/pbmc_granulocyte_sorted_3k_filtered_feature_bc_matrix.h5",
                "md5": "e326066b51ec8975197c29a7f911a4fd",
                "size": 38844318,
                "format": "10x_h5",
                "raw": True,
            },
            {
                "name": "atac_fragments.tsv.gz",
                "description": "ATAC per fragment information",
                "url": "https://cf.10xgenomics.com/samples/cell-arc/2.0.0/pbmc_granulocyte_sorted_3k/pbmc_granulocyte_sorted_3k_atac_fragments.tsv.gz",
                "md5": "d49f4012ff65d9edfee86281d6afb286",
                "size": 467587065,
                "raw": True,
            },
            {
                "name": "atac_fragments.tsv.gz.tbi",
                "description": "ATAC per fragment information index",
                "url": "https://cf.10xgenomics.com/samples/cell-arc/2.0.0/pbmc_granulocyte_sorted_3k/pbmc_granulocyte_sorted_3k_atac_fragments.tsv.gz.tbi",
                "md5": "7f73915aff0f3ed18b133ca9e0af2bb2",
                "size": 667597,
                "raw": True,
            },
            {
                "name": "atac_peaks.bed",
                "description": "ATAC peak locations",
                "url": "https://cf.10xgenomics.com/samples/cell-arc/2.0.0/pbmc_granulocyte_sorted_3k/pbmc_granulocyte_sorted_3k_atac_peaks.bed",
                "md5": "6259822fc2958a8854bd7b52424b5b57",
                "size": 2350219,
                "raw": True,
            },
            {
                "name": "atac_peak_annotation.tsv",
                "description": "ATAC peak annotations based on proximal genes",
                "url": "https://cf.10xgenomics.com/samples/cell-arc/2.0.0/pbmc_granulocyte_sorted_3k/pbmc_granulocyte_sorted_3k_atac_peak_annotation.tsv",
                "md5": "8673a07eab65e4bcf855abbe4da6bc3b",
                "size": 5450627,
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
    return PBMC3kMultiome()

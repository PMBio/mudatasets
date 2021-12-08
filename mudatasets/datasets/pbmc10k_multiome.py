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
        self.url = "https://www.10xgenomics.com/resources/datasets/pbmc-from-a-healthy-donor-granulocytes-removed-through-cell-sorting-10-k-1-standard-1-0-0"
        self.files = [
            {
                "name": "filtered_feature_bc_matrix.h5",
                "description": "Filtered feature barcode matrix",
                "url": "https://cf.10xgenomics.com/samples/cell-arc/1.0.0/pbmc_granulocyte_sorted_10k/pbmc_granulocyte_sorted_10k_filtered_feature_bc_matrix.h5",
                "format": "10x_h5",
                "md5": "920b16bf1e63b6610bf74bf9040ed386",
                "size": 162282142,
                "raw": True,
            },
            {
                "name": "atac_fragments.tsv.gz",
                "description": "ATAC per fragment information",
                "url": "https://cf.10xgenomics.com/samples/cell-arc/1.0.0/pbmc_granulocyte_sorted_10k/pbmc_granulocyte_sorted_10k_atac_fragments.tsv.gz",
                "md5": "a959ef83dfb9cae6ff73ab0147d547d1",
                "size": 2051027831,
                "raw": True,
            },
            {
                "name": "atac_fragments.tsv.gz.tbi",
                "description": "ATAC per fragment information index",
                "url": "https://cf.10xgenomics.com/samples/cell-arc/1.0.0/pbmc_granulocyte_sorted_10k/pbmc_granulocyte_sorted_10k_atac_fragments.tsv.gz.tbi",
                "md5": "df967acbe28da89aed9cfdd89370b7af",
                "size": 1027204,
                "raw": True,
            },
            {
                "name": "atac_peaks.bed",
                "description": "ATAC peak locations",
                "url": "https://cf.10xgenomics.com/samples/cell-arc/1.0.0/pbmc_granulocyte_sorted_10k/pbmc_granulocyte_sorted_10k_atac_peaks.bed",
                "md5": "fcd3f4ec84bd23a1b985e8efc511d6c0",
                "size": 2588261,
                "raw": True,
            },
            {
                "name": "atac_peak_annotation.tsv",
                "description": "ATAC peak annotations based on proximal genes",
                "url": "https://cf.10xgenomics.com/samples/cell-arc/1.0.0/pbmc_granulocyte_sorted_10k/pbmc_granulocyte_sorted_10k_atac_peak_annotation.tsv",
                "md5": "84696e7ce8b64bfccff7ecc4e3c7ea6b",
                "size": 5357234,
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
    return PBMC10kMultiome()

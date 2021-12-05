from ..core import MuDataSet
from ..utils import sizefmt


class PBMC3kCITEseq(MuDataSet):
    """
    Peripheral blood mononuclear cells (PBMCs) 
    stained with a panel of 31 TotalSeq™-B antibodies
    provided by 10X Genomics
    """

    def __init__(self):
        self.name = "pbmc5k_citeseq"
        self.version = "1.0.0"
        self.files = [
            {
                "name": "filtered_feature_bc_matrix.h5",
                "url": "https://cf.10xgenomics.com/samples/cell-exp/3.0.2/5k_pbmc_protein_v3/5k_pbmc_protein_v3_filtered_feature_bc_matrix.h5",
                "md5": "3366a47283177fe9af143d5819fad61f",
                "format": "10x_h5",
                "size": 17129253,
                "raw": True,
            },
            {
                "name": "minipbcite.h5mu",
                "url": "https://download.wetransfer.com/eugv/eb52f5fdb68fcf20325599354042cc9d20211205184307/fd0471a0e1f38e6a8fc4fe1fb1e938922b5f8041/minipbcite.h5mu?token=eyJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2Mzg3MzE4NzcsImV4cCI6MTYzODczMjQ3NywidW5pcXVlIjoiZWI1MmY1ZmRiNjhmY2YyMDMyNTU5OTM1NDA0MmNjOWQyMDIxMTIwNTE4NDMwNyIsImZpbGVuYW1lIjoibWluaXBiY2l0ZS5oNW11Iiwid2F5YmlsbF91cmwiOiJodHRwOi8vc3Rvcm0taW50ZXJuYWwuc2VydmljZS5ldS13ZXN0LTEud2V0cmFuc2Zlci5uZXQvYXBpL3dheWJpbGxzP3NpZ25lZF93YXliaWxsX2lkPWV5SmZjbUZwYkhNaU9uc2liV1Z6YzJGblpTSTZJa0pCYUhOTGQyUjJWVlJ0ZFNJc0ltVjRjQ0k2SWpJd01qRXRNVEl0TURWVU1UazZNamM2TlRjdU1EQXdXaUlzSW5CMWNpSTZJbmRoZVdKcGJHeGZhV1FpZlgwLS0xODQ4YjFlZTA3MjNjYWYzNDU4ZTEzYzgxMWJhZDY5ZTk3NzFlZGNmYTIyNTVjNWM4YTc3MGMxYzQxYjg2YmNhIiwiZmluZ2VycHJpbnQiOiJmZDA0NzFhMGUxZjM4ZTZhOGZjNGZlMWZiMWU5Mzg5MjJiNWY4MDQxIiwiY2FsbGJhY2siOiJ7XCJmb3JtZGF0YVwiOntcImFjdGlvblwiOlwiaHR0cDovL2Zyb250ZW5kLnNlcnZpY2UuZXUtd2VzdC0xLndldHJhbnNmZXIubmV0L3dlYmhvb2tzL2JhY2tlbmRcIn0sXCJmb3JtXCI6e1widHJhbnNmZXJfaWRcIjpcImViNTJmNWZkYjY4ZmNmMjAzMjU1OTkzNTQwNDJjYzlkMjAyMTEyMDUxODQzMDdcIixcImRvd25sb2FkX2lkXCI6MTM4MjMyNDk1Nzh9fSJ9.6qzYzeCxdEblRNEF6AS-hBtC3H5WmbBc5IPTjMBMFR0&cf=y",
                "md5": "6dc66fc56970193ad498b8eb5d96306c",
                "size": 17151496,
                "raw": False,
                "subsampled": True,
                "subsample_fraction": 0.1,
                "selected_features": True,
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
    return PBMC3kCITEseq()

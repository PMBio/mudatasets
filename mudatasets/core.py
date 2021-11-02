import os
import sys
import requests
from importlib import import_module
from hashlib import md5, sha1, sha256, sha512
from warnings import warn
import mudata
from mudata import MuData

from .utils import sizefmt

PREFIX = "\u25A0 "


class MuDataSet:
    """
    Base class for all datasets.
    """

    def __init__(self, path):
        self.name = None

    def download(
        self, data_dir="~/mudatasets/", full=False, files=None, chunk_size=8192, check_sum=True
    ):
        """
        Download the files in the dataset.
        """

        def dwnld(finfo, data_path):
            with requests.get(finfo["url"], stream=True) as r:
                r.raise_for_status()
                total_length = r.headers.get("content-length")
                if total_length:
                    total_length = int(total_length)
                    dl = 0
                with open(data_path, "wb") as f:
                    for chunk in r.iter_content(chunk_size=chunk_size):
                        if chunk:
                            f.write(chunk)
                            if total_length:
                                dl += len(chunk)
                                done = int(50 * dl / total_length)
                                sys.stdout.write(
                                    "\r[%s%s] %s %s %s"
                                    % (
                                        "=" * done,
                                        " " * (50 - done),
                                        sizefmt(finfo["size"]),
                                        self.name,
                                        finfo["name"],
                                    )
                                )
                                sys.stdout.flush()
                print("\n")

        def chck_hsm(finfo, data_path, callback):
            hashfs = {
                "md5": md5,
                "sha1": sha1,
                "sha256": sha256,
                "sha512": sha512,
            }
            hashsums = {k: k in finfo for k in hashfs.keys()}
            hashsums = {k: v for k, v in hashsums.items() if v}
            if len(hashsums) > 0:
                hashf_name = list(hashsums.keys())[0]
                hashf = hashfs[hashf_name]

                hash = hashf()
                with open(data_path, "rb") as f:
                    for chunk in iter(lambda: f.read(chunk_size), b""):
                        hash.update(chunk)
                if hash.hexdigest() == finfo[hashf_name]:
                    print(f"{PREFIX}Checksum is validated ({hashf_name}) for {finfo['name']}")
                else:
                    warn(
                        f"{PREFIX}Checksum does not match ({hashf_name}), will re-download {finfo['name']}"
                    )
                    callback(finfo, data_path)
            else:
                warn(f"No supported checksum to validate has been provided for {finfo['name']}")

        data_dir = os.path.expanduser(data_dir)

        os.makedirs(os.path.join(data_dir, self.name), exist_ok=True)
        # Define files to download
        if files is None or len(files) == 0:
            if full:
                files = [f["name"] for f in self.data["files"]]
            else:
                files = [f["name"] for f in self.data["files"] if f.get("required", False)]

        # Download files
        for i, f in enumerate(files):
            finfo = self.data["files"][i]
            data_path = os.path.join(data_dir, self.name, os.path.basename(finfo["url"]))
            if not os.path.exists(data_path):
                dwnld(finfo, data_path)
            else:
                print(
                    f"{PREFIX}File {finfo['name']} from {self.name} has been found at {data_path}"
                )
                if check_sum:
                    chck_hsm(finfo, data_path, dwnld)
                else:
                    warn("Will not validate the checksum of the data")

        return data_path, self.info


# List all available datasets
def list_datasets():
    datasets = []
    for file in os.listdir(os.path.join(os.path.dirname(__file__), "datasets")):
        if file.endswith(".py") and not file.startswith("_"):
            datasets.append(file.replace(".py", ""))
    return datasets


# Load a dataset
def load(
    dataset,
    data_dir="~/mudatasets/",
    with_info=False,
    full=False,
    files=None,
    backed=True,
    chunk_size=8192,
) -> MuData:
    """
    Download and open the datasets returning a MuData object
    """

    dataset_module = ".datasets." + dataset
    try:
        dataset = import_module(dataset_module, package=__package__)
    except ModuleNotFoundError as e:
        raise ValueError(f"Dataset {dataset} not found")

    dset = dataset.dataset()  # MuDataSet
    data_path, data_info = dset.download(
        data_dir=data_dir, full=full, files=files, chunk_size=chunk_size
    )
    if "format" in data_info:
        if data_info["format"] == "10x_h5":
            if backed:
                warn("Dataset is in the 10X .h5 format and can't be loaded as backed.")
            import muon as mu

            mdata = mu.read_10x_h5(data_path)
        else:
            mdata = mudata.read(data_path, backed=backed)
    else:
        mdata = mudata.read(data_path, backed=backed)
    if with_info:
        return mdata, data_info
    else:
        return mdata

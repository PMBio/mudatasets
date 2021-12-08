import os
import sys
import requests
from importlib import import_module
from hashlib import md5, sha1, sha256, sha512
from warnings import warn
from tqdm import tqdm
from math import ceil 
import mudata
from mudata import MuData

from .utils import sizefmt

PREFIX = "\u25A0 "

# File in one of these formats has to be loaded
MAINFORMATS = ["h5mu", "h5ad", "10x_h5"]  # ordered by priority
MAINEXTENSIONS = ["h5mu", "h5ad", "h5"]   # ordered by priority

class MuDataSet:
    """
    Base class for all datasets.
    """

    def __init__(self, path):
        self.name = None

    def download(
        self, data_dir="~/mudatasets/", full=False, files=None, version=None, chunk_size=8192, check_sum=True
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
                total_chunks = ceil(total_length / chunk_size)
                postfix = ", ".join([sizefmt(finfo["size"]), finfo["name"], self.name])
                with open(data_path, "wb") as f:
                    for chunk in tqdm(r.iter_content(chunk_size=chunk_size), total=total_chunks, postfix=postfix):
                        if chunk:
                            f.write(chunk)
                

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

        # Check version
        available_versions = [e["version"] for e in self.data_versions]
        if version is not None:
            if version not in available_versions:
                raise ValueError(f"Version {version} is not available for the dataset {self.name}. Available versions are {' ,'.join(available_versions)}.")
        else:  # default version
            version = self.version

        # Point to the requested data version
        data = [e for e in self.data_versions if e["version"] == version][0]

        # Define files to download
        if files is None or len(files) == 0:
            if full:
                files = [f["name"] for f in data["files"]]
            else:
                # Search for an appropriate file to be downloaded
                for ext in MAINEXTENSIONS:
                    files = [f["name"] for f in data["files"] if f["name"].endswith(ext)]
                    if len(files) > 0:
                        break
                # If extension search did not succeed, try to find by the format field
                if len(files) == 0:
                    for fmt in MAINFORMATS:
                        files = [f["name"] for f in data["files"] if f.get("format", "") == fmt]
                        if len(files) > 0:
                            break
        elif full:
            warn("Argument `full=True` is ignored since a list of files is provided.")

        if isinstance(files, str):
            files = [files]

        # Check that there's a file with one of the MAINEXTENSIONS
        maybe_priority_file = None
        priority_file = None
        for ext in MAINEXTENSIONS:
            for f in files:
                if f.endswith(f".{ext}"):
                    # Check it is not a subsampled file and all features are available
                    finfo = [e for e in data["files"] if e["name"] == f][0]
                    if not finfo.get("subsampled", False) and not finfo.get("selected_features", False):
                        priority_file = f
                        break
                    # If only subsampled data is requested
                    if maybe_priority_file is None:
                        maybe_priority_file = f
            if priority_file is not None:
                break
        if priority_file is None:
            if maybe_priority_file is None:
                warn(f"None of the files is in the format that can be automatically loaded: {', '.join(MAINFORMATS)}.")
            else:
                priority_file = maybe_priority_file

        # Download files
        priority_file_path = None
        files_avail = [f["name"] for f in data["files"]]
        for f in files:
            if f in files_avail:
                finfo = [e for e in data["files"] if e["name"] == f][0]
                data_path = os.path.join(os.path.join(data_dir, self.name), f)
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
                if f == priority_file:
                    priority_file_path = data_path
            else:
                warn(f"File {f} is not available for {self.name}.")

        return priority_file_path, self.info


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
    full=False,
    files=None,
    version=None,
    with_info=False,
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
        data_dir=data_dir, full=full, files=files, version=version, chunk_size=chunk_size
    )

    mdata = None
    if data_path is not None:
        if data_path.endswith(".h5mu") or data_path.endswith(".h5ad"):
            maybe_backed = " in backed mode" if backed else ""
            print(f"{PREFIX}Loading {os.path.basename(data_path)}{maybe_backed}...")
            mdata = mudata.read(data_path, backed=backed)
        elif data_path.endswith(".h5"):
            if backed:
                warn("Dataset is in the 10X .h5 format and can't be loaded as backed.")
            try:
                import muon as mu
                print(f"{PREFIX}Loading {os.path.basename(data_path)}...")
                mdata = mu.read_10x_h5(data_path)
            except ImportError as e:
                warn("Muon is not installed and is required to load raw data. Install pysam from PyPI (`pip install muon`) or from GitHub (`pip install git+https://github.com/PMBio/muon`)")
                if with_info:
                    return None, data_info
                else:
                    return None
    
    if mdata is None:
        # Check if there's a custom loader
        custom_loader = getattr(dset, "load", None)
        if callable(custom_loader):
            mdata = dset.load(data_dir=data_dir)
        else:
            warn("There seems to be no file with accepted extension to load (h5mu, h5ad, h5). There is no custom loader either.")

    if with_info:
        return mdata, data_info
    else:
        return mdata

# List dataset info
def info(
    dataset
) -> MuData:
    """
    List info on a dataset and included files
    """
    dataset_module = ".datasets." + dataset
    try:
        dataset = import_module(dataset_module, package=__package__)
    except ModuleNotFoundError as e:
        raise ValueError(f"Dataset {dataset} not found")

    dset = dataset.dataset()  # MuDataSet
    return dset.info


# List dataset files
def list_files(
    dataset,
    version=None,
) -> MuData:
    """
    List file names available for a dataset
    """
    dset_info = info(dataset)
    if version is None:
        version = dset_info['version']
    versions = [i for i in dset_info['data_versions'] if i['version'] == version]
    if len(versions) == 0:
        all_versions = [i['version'] for i in dset_info['data_versions']]
        raise ValueError(f"Version {version} is not available for the dataset {dataset}. Available versions are: {', '.join(all_versions)}.")
    # Versions should be unique
    if len(versions) > 1:
        warn(f"There are multiple sets of files with the same version number {version}. Please submit an issue: https://github.com/gtca/mudatasets/issues.")

    files = versions[0]['files']
    file_names = [f['name'] for f in files]

    return file_names

def serve_webpage(port=8000):
    import http.server
    import socketserver
    import tempfile

    with tempfile.TemporaryDirectory() as dirpath:
        index = os.path.join(dirpath, "index.html")
        with open(index, mode="w") as f:
            f.write("<html><body>\n")
            f.write("<h1><pre>mudatasets</pre></h1>\n")
            f.write("<p>Source code: <a href='https://github.com/gtca/mudatasets'>gtca/mudatasets</a></p></br>\n")
            for dataset in list_datasets():
                f.write(f"<h2>{dataset}</h2>\n")
                f.write("<ul>")
                for file in info(dataset)["files"]:
                    f.write(f"<li><a href={file['url']}>{file['name']}</a> ({sizefmt(file['size'])})</li>")
                f.write("</ul>")
            f.write("</body></html>")
            
        DIRECTORY = dirpath
        class Handler(http.server.SimpleHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, directory=DIRECTORY, **kwargs)
        
        with socketserver.TCPServer(("", port), Handler) as httpd:
            print("serving at port", port)
            httpd.serve_forever()

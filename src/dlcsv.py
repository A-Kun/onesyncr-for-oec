#!/usr/bin/env python3
import urllib.request
import os
import multiprocessing

nasa = "http://exoplanetarchive.ipac.caltech.edu/cgi-bin/nstedAPI/nph-nstedAPI?table=exoplanets&format=csv&select=*"
eu = "http://exoplanet.eu/catalog/csv/"


def download():
    """
    Downloads the respective CSV files from the given links.
    """
    # Check if temporary directory exists.
    if not os.path.isdir("tmp"):
        # Create new tmp directory.
        os.mkdir("tmp/")

    download_list = [(nasa, "tmp/nasa.csv"), (eu, "tmp/eu.csv")]
    pool = multiprocessing.Pool(processes=2)
    pool.map(download_one, download_list)


def download_one(task):
    url, path = task[0], task[1]
    print("Downloading to " + path, flush=True)
    urllib.request.urlretrieve(url, path)
    print("Downloaded to " + path, flush=True)


if __name__ == "__main__":
    print("Downloading CSV files... ", flush=True)
    download()
    print("Done.", flush=True)

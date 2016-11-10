#!/usr/bin/env python3
import urllib.request
import os

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

    # NASA EXOPLANET ARCHIVE
    urllib.request.urlretrieve(nasa, "tmp/nasa.csv")
    # EXOPLANET.EU
    urllib.request.urlretrieve(eu, "tmp/eu.csv")

if __name__ == "__main__":
    print("Downloading CSV files...", end="")
    download()
    print("done")

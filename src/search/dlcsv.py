import urllib.request
import os

# Download csv files.

# Check if temporary directory exists.
if not os.path.isdir("tmp"):
    # Create new tmp directory.
    os.mkdir("tmp/")


# NASA EXOPLANET ARCHIVE
url = "http://exoplanetarchive.ipac.caltech.edu/cgi-bin/IceTable/nph-iceTblDownload"
#url = "http://exoplanetarchive.ipac.caltech.edu/cgi-bin/nstedAPI/nph-nstedAPI?table=exoplanets"
urllib.request.urlretrieve(url, "tmp/nasa.csv")


# EXOPLANET.EU
url2 = "http://exoplanet.eu/catalog/csv/"
urllib.request.urlretrieve(url2, "tmp/eu.csv")

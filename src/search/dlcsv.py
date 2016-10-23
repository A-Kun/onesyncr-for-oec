import urllib.request
import os

# Download csv files.
# os.mkdir("tmp/")


url = "http://exoplanetarchive.ipac.caltech.edu/cgi-bin/nstedAPI/nph-nstedAPI?table=exoplanets"

urllib.request.urlretrieve(url, "tmp/nasa.csv")


url2 = "http://exoplanet.eu/catalog/csv/"

urllib.request.urlretrieve(url2, "tmp/eu.csv")

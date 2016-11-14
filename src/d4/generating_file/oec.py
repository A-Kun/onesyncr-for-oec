#!/usr/bin/python
import xmltools
import urllib
import zipfile
import shutil
import os

url_oec = "https://github.com/OpenExoplanetCatalogue/open_exoplanet_catalogue/archive/master.zip"

def get():
    xmltools.ensure_empty_dir("tmp_data")
    urllib.urlretrieve (url_oec, "tmp_data/oec.zip")

def parse():
    # delete old data
    xmltools.ensure_empty_dir("OEC")

    # parse data into default xml format
    ziphandler = zipfile.ZipFile("tmp_data/oec.zip")
    for name in ziphandler.namelist():
        # only keep main systems/ directory
        if name[0:40] == "open_exoplanet_catalogue-master/systems/" and len(name)>40:
            source = ziphandler.open(name)
            target = file("OEC/"+os.path.basename(name), "wb")
            shutil.copyfileobj(source, target)

if __name__=="__main__":
    get()
    parse()
    print ('OEC done')
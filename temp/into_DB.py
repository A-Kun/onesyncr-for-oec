#!/usr/bin/python
import os
import glob
import xmltodict
import json
from pymongo import MongoClient
client = MongoClient('localhost', 27017)

db = client['OEC']

collection = db['OEC']


list_xmldir = glob.glob(os.getcwd() + "/systems_open_exoplanet_catalogue/*.xml")


# read xml into mongoDB
for dir in list_xmldir:
    with open(dir, 'r') as temfile:
        data = temfile.read()
    o = xmltodict.parse(data)
    jdata = json.dumps(o)
    collection.insert_one(json.loads(jdata))
    temfile.close()



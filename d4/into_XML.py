#!/usr/bin/python
import os
import glob
import xmltools
import xmltodict, json
from pymongo import MongoClient
client = MongoClient('localhost', 27017)

def into_xml():

    db = client['OEC']

    collection = db['OEC']

    find_all = collection.find({})

    # create new directory
    xmltools.ensure_empty_dir("new_data")
    target = os.path.join(os.getcwd(),'new_data/')

    for entry in find_all:
        del entry['_id']
        if isinstance(entry['system']['name'],list):
            file_name = target + str(entry['system']['name'][0]) + '.xml'
        else:
            file_name = target + str(entry['system']['name']) + '.xml'
        file = open(file_name,'w')
        xml = xmltodict.unparse(entry,pretty=True).encode('utf-8')
        file.write(str(xml))
        file.close()
print("Finishing writing files")







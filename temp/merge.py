#!/usr/bin/python
import os
import glob
import xmltodict, json
from pymongo import MongoClient
import xmltools
from copy import copy
import shutil

CURRENT = os.getcwd()
DESTINATION = os.path.join(CURRENT,'push')
print DESTINATION



def finditem(obj, key):
    if key in obj: return obj[key]
    for k, v in obj.items():
        if isinstance(v,dict):
            item = finditem(v, key)
            if item is None:
                return -1
            else:
                return item
# get all parent key
def get_keys(d, target,result,path):

    for k, v in d.iteritems():
        path.append(k)
        if isinstance(v, dict):
            get_keys(v, target,result,path)
        if v == target or k == target:
            result.append(copy(path))
        path.pop()
    return result

def diction_help(db_third, db_result,file_path,collection):
    for k in db_third:
        # if value is not None
        if db_third[k] is not None:
            # compare the numbers
            if type(db_third[k]) is dict and '#text' in db_third[k]:
                result, path = [],[]
                for l in get_keys(db_result, '#text',result,path):
                    # find the right target
                    if k in l:
                        print k,l
                        count = 0
                        s = ''
                        inner = db_result
                        # get path in database
                        for element in l:
                            if count == len(l)-1:
                                break
                            count += 1
                            # inner includes @error, #text ect...
                            inner = inner[element]
                            s += str(element) + '.'

                        #update with better measurement
                        # compare which error has smaller value
                        if inner['@errorplus'] > db_third[k]['@errorplus']:
                            error_plus = s + '.' + '@errorplus'
                            error_minus = s + '.' + '@errorminus'
                            text = s + '.' + '#text'
                            # collection.update(
                            #     {
                            #         '_id':
                            #             db_result['_id']
                            #     },
                            #     {
                            #         '$set': {
                            #             error_plus: db_third[k]['@errorplus']
                            #         }
                            #
                            #     },
                            #     {
                            #         '$set': {
                            #             error_minus: db_third[k]['@errorminus']
                            #         }
                            #
                            #     },
                            #     {
                            #         '$set': {
                            #             text: db_third[k]['#text']
                            #         }
                            #
                            #     }
                            # )

            # has inner dictionary or Json object, then recursinve call function
            elif type(db_third[k]) is dict:
                diction_help(db_third[k],db_result,file_path,collection)
            # has mutiple names
            elif type(db_third[k]) is list:
                pass

            # value is declination, compare the element
            elif k == 'declination':
                result, path = [],[]
                res = get_keys(db_result, k,result, path)
                if res != []:
                    inner = db_result
                    s = ''
                    for path in res[0]:

                        s += str(path) + '.'
                        inner = inner[path]
                    # conflicts=> move file to push folder
                    if inner != db_third[k]:
                        # update to database
                        if len(inner) < len(db_third[k]):
                            collection.update(
                                {
                                    '_id':
                                     db_result['_id']
                                 },
                                {
                                    '$set':{
                                        s[:-2]:db_third[k]
                                    }

                                 }
                            )

                        elif len(inner) == len(db_third[k]):
                            shutil.move(file_path, DESTINATION)



            elif type(db_third[k]) is unicode:
                # if db_third[k] !=
                pass

list_xmldir_nasa = glob.glob(os.getcwd()+"/systems_exoplanetarchive/*.xml")
list_xmldir_eu = glob.glob(os.getcwd()+"/systems_exoplaneteu/*.xml")
# open mongoDB
client = MongoClient('localhost', 27017)

db = client['OEC']
xmltools.ensure_empty_dir("push")
collection = db['OEC']


# loop through the file directory
for i in list_xmldir_eu:
    f = open(i,'r')
    xml = f.read()
    f.close()
    data = xmltodict.parse(xml)
    jdata = json.dumps(data)
    jdata = json.loads(jdata)
    eu_system = jdata['system']

    # find the corresponding name in database
    eu_sysname = eu_system['name']
    db_result = collection.find_one({'system.name': eu_sysname}) # type is dict
    # database has such a name for the system
    if db_result:

        print 'the eu system is: ' + str(eu_system)

        print db_result

        print '------------------------------------------'

        diction_help(eu_system, db_result,i,collection)

    else:
        print 'the system is not in database yet!'
        # write into database
        collection.insert_one(jdata)



    f.close()




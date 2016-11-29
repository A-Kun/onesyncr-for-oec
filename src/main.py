#!/usr/bin/python
import time
import os
import glob
import shutil
import threading
import xmltools
import multiprocessing
import eu
import nasa
import oec
import xml.etree.ElementTree as ET

CURRENT = os.getcwd()
DESTINATION = os.path.join(CURRENT,'_data/OEC/')
CONFLICT = os.path.join(CURRENT,'_/data/push/')
# print(DESTINATION, flush=True)
# print(CONFLICT, flush=True)


def file_name(dir):
    '''
    Return the directory with file name only
    :param dir: str
    :return: str
    '''
    return dir.split('/')[-1]


def has_attrib(ele,attr):
    return attr in ele.attrib


def compare_list_dir(other,oec):
    '''
    :param other: list of str
    :param oec: list of str
    :return: list of (list of str, dict)
    Return the new list of list, fist inner list in outer list stores the different
     filename exist and the second inner list will be same file name
    '''

    dir_maping = {}
    # dir maping is dict stores that mapping the with same file names
    diff = []
    outer = [diff,dir_maping]

    # loop through director in other list
    for dir_other in other:
        marker = False
        for dir_oec in oec:
            # find the same file names
            if file_name(dir_other) == file_name(dir_oec):
                # mapping dir_other to dir_oec
                dir_maping[dir_other] = dir_oec
                marker = True
                # break out current loop
                break
            # files that are the same
        # did not find a match file name
        if marker is False:
            diff.append(dir_other)
    return outer

#
# other = ['a','b','c']
# oec = ['a','e','t']
# print(compare_list_dir(other,oec), flush=True)

def merge(Eother, Eoec, dirOther,dirOec,root,first,is_move):
    '''
    This is function deal with all compare cases
    :param Eother: Element tree
    :param Eoec: Element tree
    :return:
    '''
    # first use to control return once at root
    first += 1
    # loop through the child tag in Etree of other database
    for child in Eother:
        a = Eoec.getchildren()

        # get one element with given tag in current level
        childOEC = Eoec.find(child.tag) # DONT change this

        if childOEC != None: # find only check direct children
            if child.tag == 'star' or child.tag == 'planet':
                star_planet = Eoec.findall(child.tag)
                for element in star_planet:
                    merge(child, element, dirOther, dirOec, root, first, is_move)
            # if child tag in third database is None then just skip
            elif child.text is None:
                continue
            # tag is name
            elif child.tag == 'name':
                all_names = Eoec.findall(child.tag)
                marker = False
                for oec_name in all_names:
                    if oec_name.text == child.text:
                        marker = True
                        break
                # the name tag does not exist in OEC then append the name tag
                if marker == False:
                    Eoec.append(child)
            # deal with errors
            elif 'errorplus' in child.attrib:
                # update with smaller error
                try:
                    y = float(child.attrib['errorplus'])
                except:
                    print(child.attrib['errorplus'], flush=True)
                    print('Bad data in errorplus with directory name:' + str(dirOther), flush=True)
                    break
                if not has_attrib(childOEC,'errorplus'):
                    childOEC.text = child.text
                    childOEC.set('errorplus', child.attrib['errorplus'])
                    childOEC.set('errorminus', child.attrib['errorplus'])
                elif float(child.attrib['errorplus']) < float(childOEC.attrib['errorplus']):
                    childOEC.text = child.text
                    childOEC.set('errorplus', child.attrib['errorplus'])
                    childOEC.set('errorminus', child.attrib['errorplus'])
            # never happen child.text is list at this point
            # if OEC tag is none then just update with third database info
            elif childOEC.text is None:
                childOEC.text = child.text
            # deal with numbers
            # elif (child.text).replace('.','',1).isdigit():
            #     # if not equal then up to client's decision(move to confict area)
            #     if child.text != childOEC.text:
            #         move = True
            # # any other cases
            else:
                # the content is not the same then push file to (confict area)
                if child.text != childOEC.text:
                    move = True
            # if is a distance tag
            merge(child,childOEC,dirOther,dirOec,root,first,is_move)
        # oec does not have such tag then update
        else:
            Eoec.append(child)
    # control only one return
    if(first == 0):
        # clear indentation in xml
        xmltools.indent(Eoec, level=0)
        # write to xml directory with all updates
        root.write(dirOec)

        # copy file
        if is_move == True:
            try:
                shutil.copy(dirOther, CONFLICT)
            except IOError:
                os.chmod(dirOther, 777)  # ?? still can raise exception
                shutil.copy(dirOther, CONFLICT)

        return


def merge_two_database(list_third,list_oec):
    mainList = compare_list_dir(list_third ,list_oec)
    diffList = mainList[0]
    sameDict = mainList[1]
    # IF file name do not exist in OEC directory, then move to OEC dir
    for diff_dir in diffList:
        try:
            shutil.copy(diff_dir, DESTINATION)
        except (IOError):
            os.chmod(diff_dir, 777)  # ?? still can raise exception
            shutil.copy(diff_dir, DESTINATION)
    # start merge file that do exist in OEC , each directory create a thread to excute merge
    # since the filename in directory is unique so safe to use threading
    for dirOther,dirOec in sameDict.items():
        other = ET.parse(dirOther).getroot()
        tree = ET.parse(dirOec)
        oec = tree.getroot()
        first = -1  # use to control return statement in merge recursion call
        move = False  # use to decide whehter a file should move
        # create threading excute merge function
        t = threading.Thread(target=merge, args = (other, oec, dirOther,dirOec,tree,first,move,))
        t.daemon = True  # set thread to daemon ('ok' won't be printed in this case)
        t.start()
        t.join()


def run_merge():
    list_xmldir_nasa = glob.glob("_data/Nasa/*.xml")
    list_xmldir_eu = glob.glob("_data/EU/*.xml")
    list_xmldir_oec = glob.glob("_data/OEC/*.xml")

    print("nasa before merge size is :" + str(len(list_xmldir_nasa)), flush=True)
    print("eu before size merge is :" + str(len(list_xmldir_eu)), flush=True)
    print("oec before size merge is :" + str(len(list_xmldir_oec)), flush=True)

    print("start merging....", flush=True)
    try:
        merge_two_database(list_xmldir_nasa, list_xmldir_oec)
        merge_two_database(list_xmldir_eu, list_xmldir_oec)
    except:
        pass
    print('merge done', flush=True)

    list_xmldir_nasa = glob.glob("_data/Nasa/*.xml")
    list_xmldir_eu = glob.glob("_data/EU/*.xml")
    list_xmldir_oec = glob.glob("_data/OEC/*.xml")

    print("nasa after merge size is :" + str(len(list_xmldir_nasa)), flush=True)
    print("eu after merge size is :" + str(len(list_xmldir_eu)), flush=True)
    print("oec after merge size is :" + str(len(list_xmldir_oec)), flush=True)


def download_database(db):
    if db == "nasa":
        print('Start downloading Nasa', flush=True)
        nasa.get()
        nasa.parse()
        print('Nasa done', flush=True)
    elif db == "eu":
        print('Start downloading EU', flush=True)
        eu.get()
        eu.parse()
        print("EU done", flush=True)
    elif db == "oec":
        print('Start downloading OEC', flush=True)
        oec.get()
        oec.parse()
        print('OEC done', flush=True)


def main():
    start_time = time.time()

    download_list = ["nasa", "eu", "oec"]
    pool = multiprocessing.Pool(processes=3)
    pool.map(download_database, download_list)
    pool.close()
    print("Download complete.", flush=True)
    xmltools.ensure_empty_dir("_data/push")
    xmltools.ensure_empty_dir("_data/OEC_old")
    file_list = glob.glob("_data/OEC/*.xml")
    for next_file in file_list:
        shutil.copy2(next_file, "_data/OEC_old/")

    run_merge()
    print("--- %s seconds ---" % (time.time() - start_time), flush=True)


def check_difference():
    list_xmldir_oec = glob.glob("_data/OEC/*.xml")
    result = []
    for next_file in list_xmldir_oec:
        try:
            file_old = open(next_file.replace("_data/OEC/", "_data/OEC_old/"))
            file_new = open(next_file)
            if file_old.read() != file_new.read():
                result.append((next_file, "Modified"))
            file_old.close()
            file_new.close()

        except FileNotFoundError:
            result.append((next_file, "Added"))
    return result


if __name__ == '__main__':
    # main()
    check_difference()
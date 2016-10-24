import os
import glob
import difflib
import sys
import xml.etree.ElementTree as ET

list_xmldir_nasa = glob.glob(os.getcwd()+"/systems_exoplanetarchive/*.xml")
list_xmldir_eu = glob.glob(os.getcwd()+"/systems_exoplaneteu/*.xml")
count = 0
print "nasa has: " + str(len(list_xmldir_nasa))
print "eu has : " + str(len(list_xmldir_eu))

for i in list_xmldir_eu:
    for j in list_xmldir_nasa:
        if i.split('/')[-1] == j.split('/')[-1]:
            outputfilename = "new/"+ i.split('/')[-1] +".xml"

            oec_eu = ET.parse(i)
            oec_nasa = ET.parse(j)

            for star in oec_nasa.findall(".//star"):
                #print star.findtext("name")  
                for planet in star.findall("planet"):
                    print planet.findtext("name")  
                print "---------------------"
                

        else:
            pass
print "files with same has :" + str(count)
            

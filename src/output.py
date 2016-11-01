#!/usr/bin/env python3
import xml.etree.ElementTree as ET
import shutil
import os

if os.path.isdir("systems"):
    shutil.rmtree('./systems')
os.mkdir("systems")


# Taken from OEC external
def indent(elem, level=0):
    i = "\n" + level*"\t"
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "\t"
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


def generate_xml(systems):
    for key in systems:
        # Output file name
        filename = "systems/" + key + ".xml"

        sys = systems[key]
        system = ET.Element("system")
        ET.SubElement(system, "name").text = key
        ET.SubElement(system, "rightascension").text = sys._rightascension
        ET.SubElement(system, "declination").text = sys._declination


        for key2 in sys._stars:
            st = sys._stars[key2]
            star = ET.SubElement(system, "star")
            ET.SubElement(star, "name").text = st._name
            for i in range(len(st._attrkey)):
                if st._attrvalue[i]:
                    if len(st._attrvalue[i]) > 1:
                        if isinstance(st._attrvalue[i], list):
                            ET.SubElement(star, st._attrkey[i], errorminus=st._attrvalue[i][1], errorvalue=st._attrvalue[i][2]).text = st._attrvalue[i][0]
                        else:
                            ET.SubElement(star, st._attrkey[i]).text = st._attrvalue[i]
                    else:
                        if isinstance(st._attrvalue[i], list):
                            ET.SubElement(star, st._attrkey[i]).text = st._attrvalue[i][0]
                        else:
                            ET.SubElement(star, st._attrkey[i]).text = st._attrvalue[i]

            for key3 in st._planets:
                pl = st._planets[key3]
                planet = ET.SubElement(star, "planet")
                ET.SubElement(planet, "name").text = pl._name
                for i in range(len(pl._attrkey)):
                    if pl._attrvalue[i]:
                        if len(pl._attrvalue[i]) > 1:
                            if isinstance(pl._attrvalue[i], list):
                                ET.SubElement(planet, pl._attrkey[i], errorminus=pl._attrvalue[i][1], errorvalue=pl._attrvalue[i][2]).text = pl._attrvalue[i][0]
                            else:
                                ET.SubElement(planet, pl._attrkey[i]).text = pl._attrvalue[i]
                        else:
                            if isinstance(st._attrvalue[i], list):
                                ET.SubElement(planet, pl._attrkey[i]).text = pl._attrvalue[i][0]
                            else:
                                ET.SubElement(planet, pl._attrkey[i]).text = pl._attrvalue[i]

        indent(system)
        ET.ElementTree(system).write(filename)

if __name__ == "__main__":
    if 0:
        print("Generating xml files from exoplanet.eu...", end="")
        from eu import *
        get_eu()
        generate_xml(SYSTEMS)
    else:
        print("Generating xml files from NASA Exoplanet Archive...", end="")
        from nasa import *
        get_nasa()
        generate_xml(SYSTEMS)
    print("done")

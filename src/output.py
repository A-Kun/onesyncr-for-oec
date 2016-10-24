import xml.etree.ElementTree as ET
import shutil
import os

if os.path.isdir("systems"):
    shutil.rmtree('./systems')
os.mkdir("systems")

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
            """
            ET.SubElement(star, "mass", errorminus=st._mass[1], errorplus=st._mass[2]).text = st._mass[0]
            ET.SubElement(star, "radius", errorminus=st._radius[1], errorplus=st._radius[2]).text = st._radius[0]
            ET.SubElement(star, "temperature", errorminus=st._temperature[1], errorplus=st._temperature[2]).text = st._temperature[0]
            ET.SubElement(star, "age", errorminus=st._age[1], errorplus=st._age[2]).text = st._age[0]
            ET.SubElement(star, "metallicity").text = st._metallicity
            ET.SubElement(star, "spectraltype").text = st._spectraltype


            if st._magV:
                if len(st._magV > 1):
                    ET.SubElement(star, "magV", errorminus=st._magV[1], errorplus=st._magV[2]).text = st._magV[0]
                else:
                    ET.SubElement(star, "magV").text = st._magV[0]

            if st._magR:
                if len(st._magR > 1):
                    ET.SubElement(star, "magR", errorminus=st._magR[1], errorplus=st._magR[2]).text = st._magR[0]
                else:
                    ET.SubElement(star, "magR").text = st._magR[0]

            if st._magI:
                if len(st._magI > 1):
                    ET.SubElement(star, "magI", errorminus=st._magI[1], errorplus=st._magI[2]).text = st._magI[0]
                else:
                    ET.SubElement(star, "magI").text = st._magI[0]
            if st._magJ:
                if len(st._magJ > 1):
                    ET.SubElement(star, "magJ", errorminus=st._magJ[1], errorplus=st._magJ[2]).text = st._magJ[0]
                else:
                    ET.SubElement(star, "magJ").text = st._magJ[0]
            if st._magH:
                if len(st._magH > 1):
                    ET.SubElement(star, "magH", errorminus=st._magH[1], errorplus=st._magH[2]).text = st._magH[0]
                else:
                    ET.SubElement(star, "magH").text = st._magH[0]
            if st._magK:
                if len(st._magK > 1):
                    ET.SubElement(star, "magK", errorminus=st._magK[1], errorplus=st._magK[2]).text = st._magK[0]
                else:
                    ET.SubElement(star, "magK").text = st._magK[0]"""


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
                """
                ET.SubElement(planet, "mass", errorminus=pl._mass[1], errorplus=pl._mass[2]).text = pl._mass[0]
                ET.SubElement(planet, "radius", errorminus=pl._radius[1], errorplus=pl._radius[2]).text = pl._radius[0]
                ET.SubElement(planet, "temperature", errorminus=pl._temperature[1], errorplus=pl._temperature[2]).text = pl._temperature[0]
                ET.SubElement(planet, "semimajoraxis", errorminus=pl._semimajoraxis[1], errorplus=pl._semimajoraxis[2]).text = pl._semimajoraxis[0]
                ET.SubElement(planet, "eccentrincity", errorminus=pl._eccentricity[1], errorplus=pl._eccentricity[2]).text = pl._eccentricity[0]
                ET.SubElement(planet, "periastron", errorminus=pl._periastron[1], errorplus=pl._periastron[2]).text = pl._perriastron[0]
                ET.SubElement(planet, "inclination", errorminus=pl._inclination[1], errorplus=pl._inclination[2]).text = pl._inclination[0]
                ET.SubElement(planet, "period", errorminus=pl._period[1], errorplus=pl._period[2]).text = pl._period[0]
                ET.SubElement(planet, "periastrontime", errorminus=pl._periastrontime[1], errorplus=pl._periastrontime[2]).text = pl._periastrontime[0]

                ET.SubElement(planet, "discoverymethod").text = pl._discoverymethod
                ET.SubElement(planet, "discoveryyear").text = pl._discoveryyear
                ET.SubElement(planet, "lastupdate").text = pl._lastupdate
                """
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
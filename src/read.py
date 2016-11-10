#!/usr/bin/env python3

# File for reading xml files into class
import xml.etree.ElementTree as ET
import glob
import oec

SYSTEMS = {}

for item in glob.glob("systems/*"):
    tree = ET.parse(item)
    root = tree.getroot()
    break


def add(root, system=None):
    for child in root:
        # ADD to object later
        print(child.tag, root.find(child.tag).text, child.attrib, len(child.attrib))

if __name__ == "__main__":
    add(root)

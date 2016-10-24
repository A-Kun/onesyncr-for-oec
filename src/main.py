print("Downloading CSV files from Exoplanet.eu and NASA... ", end="", flush=True)
#import dlcsv
print("Done.", flush=True)

print("Parsing data from downloaded CSV file... ", end="", flush=True)
from eu import *
get_eu()
print("Done.", flush=True)
print("\t-> " + str(len(SYSTEMS)) + " entries found.", flush=True)

print("Generating XML files from exoplanet.eu... ", end="", flush=True)
from output import *
generate_xml(SYSTEMS)
print("Done.", flush=True)

print("Getting XML file list... ", end="", flush=True)
import glob
xml_list = glob.glob('systems/*.xml')
print("Done.", flush=True)
print("\t-> " + str(len(xml_list)) + " files found.", flush=True)

print("Pushing XML files to GitHub...", flush=True)
print("(Since pushing everything takes forever,\nonly 10 files will be pushed for demo.)", flush=True)
from github import *
count_create = 0
count_modify = 0
count_no_change = 0
for next_file in xml_list:
    file = open(next_file)
    content = file.read()
    try:
        if push_file(next_file, "Update" + next_file[next_file.find("/") + 1:], content):
            count_create += 1
        else:
            count_modify += 1
    except:
        pass
    else:
        print("\t(" + str(count_create + count_modify) + "/10)", flush=True)
    file.close()
    if count_create + count_modify >= 10:
        break
print("Done.", flush=True)
print("\t-> " + str(count_create) + " files created.", flush=True)
print("\t-> " + str(count_modify) + " files modified.", flush=True)

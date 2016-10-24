print("Downloading CSV files from Exoplanet.eu and NASA... ", end="", flush=True)
import dlcsv
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
updated_list = []
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
        updated_list.append(next_file[next_file.find("/") + 1:])
        print("\t(" + str(count_create + count_modify) + "/10)", flush=True)
    file.close()
    if count_create + count_modify >= 10:
        break
print("Done.", flush=True)
print("\t-> " + str(count_create) + " files created.", flush=True)
print("\t-> " + str(count_modify) + " files modified.", flush=True)


print("Creating pull request... ", end="", flush=True)
pr = create_pull_request("Update exoplanet systems")
pr_number = pr.number
print("Done.", flush=True)

print("Sending notification email... ", end="", flush=True)
from mail import *
body = """Hi there,

The following files were updated:

"""
for next_file in updated_list:
    body += "\t" + next_file + "\n"
body += "\nA pull request has been created: https://github.com/poppintk/open_exoplanet_catalogue/pull/"
body += str(pr.number) + "\n"
send_email("Andrew Wang <me@andrewwang.ca>",
           "Andrew Wang <andrewwang963@gmail.com>",
           "Update to Open Exoplanet Catelogue",
           body)
print("Done.")

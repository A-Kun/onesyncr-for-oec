import dlcsv
import eu
import output
import glob
import github
import mail
import random
from github3 import login


def run(token):
    gh = login(token=token)
    user = gh.user()

    EMAIL_RECEIVER = user.name + " <" + user.email + ">"

    print("Downloading CSV files from Exoplanet.eu and NASA... ", flush=True)
    # dlcsv.download()
    print("Done.", flush=True)

    print("Parsing data from downloaded CSV file... ", end="", flush=True)
    eu.get_eu()
    print("Done.", flush=True)
    print("\t-> " + str(len(eu.SYSTEMS)) + " entries found.", flush=True)

    print("Generating XML files from exoplanet.eu... ", end="", flush=True)
    output.generate_xml(eu.SYSTEMS)
    print("Done.", flush=True)

    print("Getting XML file list... ", end="", flush=True)
    xml_list = glob.glob('systems/*.xml')
    print("Done.", flush=True)
    print("\t-> " + str(len(xml_list)) + " files found.", flush=True)

    print("Pushing XML files to GitHub...", flush=True)

    num_push = 100  # number of files to be pushed for demo.
    push_set = set()
    for i in range(num_push):
        rand_num = random.randint(0, len(xml_list) - 1)
        while xml_list[rand_num] in push_set:
            rand_num = random.randint(0, len(xml_list) - 1)
        push_set.add(xml_list[rand_num])

    print("(Randomly pushing " + str(num_push) + " files.)", flush=True)

    updated_list = []

    def process_push(next_file):
        file = open(next_file)
        content = file.read()
        try:
            github.push_file(next_file, "Update " + next_file[next_file.find("/") + 1:], content, token)
        except IndexError:
            pass
        else:
            updated_list.append(next_file[next_file.find("/") + 1:])
        file.close()

    ## multiprocessing does not work here...
    # import multiprocessing
    # pool = multiprocessing.Pool(processes=10)
    # pool.map(process_push, xml_list)
    for next_xml in push_set:
        process_push(next_xml)

    print("\nDone.", flush=True)

    print("Creating pull request... ", end="", flush=True)
    try:
        pr = github.create_pull_request("Update exoplanet systems", token)
        pr_number = "/" + str(pr.number)
    except github.github3.models.GitHubError:
        pr_number = "s/"
        print("Pull request already exists.", flush=True)
    else:
        print("Done.", flush=True)

    print("Sending notification email... ", end="", flush=True)
    body = """Hi there,

    The following files were updated:

    """
    for next_file in updated_list:
        body += "\t" + next_file + "\n"
    pr_url = "https://github.com/" + github.TARGET_USERNAME + "/open_exoplanet_catalogue/pull" + pr_number + "\n"
    body += "\nA pull request has been created: " + pr_url + "\n"
    mail.send_email("Andrew Wang <me@andrewwang.ca>",
               EMAIL_RECEIVER,
               "Update to Open Exoplanet Catelogue",
               body)
    print("Done.", flush=True)
    print("An email was sent to " + EMAIL_RECEIVER)

    return pr_url

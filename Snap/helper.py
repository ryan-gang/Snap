import os
import re
import requests
from datetime import datetime
from datetime import timedelta
from bs4 import BeautifulSoup

from Snap.credentials import *


def get_site():
    url = "https://web.snapworks.me/parent-students/activities"
    r = requests.get(url, cookies = cookies)
    return r


def get_all_dates(webpage):
    soup = BeautifulSoup(webpage, "html.parser")
    all_dates = soup.find_all("span", class_ = "notify-date")
    formatted_dates = []
    for i in (range(len(all_dates))):
        try:
            date = soup.find_all("span", class_ = "notify-date")[i].text.strip()
            formatted_dates.append(datetime.strptime(date, "%d %b %Y %I:%M%p"))
        except ValueError:
            pass
    return formatted_dates


def get_domain_deprecated(link):
    if (link.startswith("https://")):
        link = link.split("https://")[-1]
    parts = link.split("/")
    domains = parts[0]
    second_level_domain = domains.split(".")[1]
    return second_level_domain


def domain_name_deprecated(link):
    full_domain = link.split("/")[2]
    domain = full_domain.split(".")[0]
    return domain


def full_yt_link(link):
    param = link.split("/")[-1]
    base = "https://www.youtube.com/watch?v="
    return base + param


def domain_name(link):
    try:
        regex = r"[a-zA-Z]*://(.*?)[.](.*?)[./]"
        domain = re.match(regex, link).group(1)
        # print(domain)
        if ((domain != "www") and (domain != "web")):
            return domain
        else:
            domain = re.match(regex, link).group(2)
            # print(domain)
            return domain
    except AttributeError:
        print(link)
        return link


def write_html(webpage, file):
    fhand = open(file, "w")
    for i in webpage:
        fhand.write(i)
    fhand.close()


def get_required_html(user_date):
    in_file = "fullwebsite.html"
    out_file = "full.html"
    fhand = open(in_file, "r")
    webpage = fhand.read()

    if isinstance((user_date), str):
        user_date = datetime.strptime(user_date, "%d/%m/%Y")
    else:
        pass

    regex = r"notify-date\">([\s\S]*?)<"
    match = re.findall(regex, webpage)
    # print(len(match))

    for i in match:
        date = i.strip()
        if (date is not ""):
            # print("date :", date)
            formatted_date = datetime.strptime(date, "%d %b %Y %I:%M%p")
            if formatted_date > user_date:
                # print(webpage.find(i))
                pass
            else:
                latest = webpage.find(i)
                # print(webpage.find(i))
                break

    try:
        website = webpage[:latest]
        write_html(website, "full.html")
    except:
        write_html(webpage, "full.html")


def get_all_links():
    outfile = "all_links.txt"
    fout = open(outfile, "w")
    # regex = r"[\'\"](https://.+?)[\'\"]"
    regex = r"[\'\"\s](https://.+?)[\'\"\s]"
    files = []

    file = "full.html"
    fhand = open(file, "r", encoding = "utf-8", errors = "surrogateescape")
    text = fhand.read()
    fhand.close()
    match = (re.findall(regex, text))
    print("Found", len(match), "links.")
    # not_allowed = ["apple", "snapworks", "googleapis", "gstatic", "firebaseio", "googletagmanager", "play"]
    for i in match:
        # print(i)
        files.append(i)
        fout.write(i)
        fout.write("\n")

    # print(len(files))
    fout.close()


def clean_links():
    drivedomains = ["drive"]
    ytdomains = ["youtu", "youtube"]
    otherdomains = ["storage", "itunes", "play", "nani", "gstatic", "gcptest-poc", "s3-us-west-2",
                    "swlivestorage", "googletagmanager"]
    xdomains = ["snapworks"]
    yt = []
    drive = []
    other = []
    file = "all_links.txt"
    fhand = open(file, "r")
    for link in fhand:
        link = link.strip()
        if (re.findall("<.*>", link)):
            link = link.split("<")[0]
        dom = domain_name(link)
        if dom in ytdomains:
            if link not in yt:
                yt.append(link)
        elif dom in drivedomains:
            if link not in drive:
                drive.append(link)
        elif dom in xdomains:
            continue
        else:
            other.append(link)

    print("Number of youtube links :", len(yt))
    print("Number of google drive links :", len(drive))
    print("Number of other links :", len(other))
    yt_file = "yt_links.txt"
    drive_file = "drive_links.txt"
    other_file = "others_links.txt"

    fout = open(yt_file, "w")
    for link in yt:
        if ((domain_name(link)) == "youtu"):
            new_link = full_yt_link(link)
        else:
            new_link = link
        fout.write(new_link)
        fout.write("\n")
    fout.close()

    fout = open(drive_file, "w")
    for link in drive:
        fout.write(link)
        fout.write("\n")
    fout.close()

    fout = open(other_file, "w")
    for link in other:
        fout.write(link)
        fout.write("\n")
    fout.close()
    return


next_steps = """
If there are links in yt_links.txt, copy them and paste them into the YT-DLG app. It will automatically download them.
Also I'd suggest take a look at the other_links.txt file. It should contain a lot of helpful links.
"""


def clean_up():
    home_dir = "G:\Coding\Projects\Snap"
    os.chdir(home_dir)
    try:
        os.remove("fullwebsite.html")
        os.remove("full.html")
        os.remove("all_links.txt")
        os.remove("drive_links.txt")
    except:
        pass

    print("Finished cleaning up.")

from datetime import datetime
import re
import requests
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


def write_html(webpage):
    file = "full.txt"
    fhand = open(file, "w")
    for i in webpage:
        fhand.write(i)

    fhand.close()


def get_all_links():
    outfile = "links.txt"
    fout = open(outfile, "w")
    # regex = r"[\'\"](https://.+?)[\'\"]"
    regex = r"[\'\"\s](https://.+?)[\'\"\s]"
    files = []

    file = "full.txt"
    fhand = open(file, "r", encoding = "utf-8", errors = "surrogateescape")
    text = fhand.read()
    fhand.close()
    match = (re.findall(regex, text))
    # not_allowed = ["apple", "snapworks", "googleapis", "gstatic", "firebaseio", "googletagmanager", "play"]
    for i in match:
        # print(i)
        files.append(i)
        fout.write(i)
        fout.write("\n")

    print(len(files))
    fout.close()


def clean_links():
    drivedomains = ["drive"]
    ytdomains = ["youtu"]
    otherdomains = ["storage", "itunes", "play", "nani", "gstatic", "gcptest-poc", "s3-us-west-2",
                    "swlivestorage", "googletagmanager"]
    xdomains = ["snapworks"]
    yt = []
    drive = []
    other = []
    file = "links.txt"
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

    yt_file = "yt_links.txt"
    drive_file = "drive_links.txt"
    other_file = "others_links.txt"
    fout = open(yt_file, "w")
    for link in yt:
        fout.write(link)
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

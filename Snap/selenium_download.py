import os
import time

from fake_useragent import UserAgent
from selenium.webdriver.chrome.options import Options


def new_chrome(chromedriver_path, headless = True, downloadPath = None):
    """ Helper function that creates a new Selenium browser """
    from selenium import webdriver
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument('headless')
    if downloadPath is not None:
        prefs = {}
        os.makedirs(downloadPath)
        prefs["profile.default_content_settings.popups"] = 0
        prefs["download.default_directory"] = downloadPath
        options.add_experimental_option("prefs", prefs)
    browser = webdriver.Chrome(chrome_options = options, executable_path = chromedriver_path)
    return browser


def selenium_download():
    from selenium import webdriver

    file = "drive_links.txt"
    with open(file, "r") as fhand:
        all_links = fhand.read().split("\n")

    options = Options()
    ua = UserAgent()
    userAgent = ua.random
    options.add_argument(f'user-agent={userAgent}')

    dir_name = "downloads"
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
        print("Created Directory", dir_name)
    os.chdir(dir_name)
    print("Current Directory :", os.getcwd())
    chromedriver_path = 'C:/Users/unitel/Downloads/chromedriver.exe'

    download_path = r"G:\Coding\Projects\Snap\downloads"
    headless = False
    if headless:
        options.add_argument('headless')
    prefs = {}
    prefs["profile.default_content_settings.popups"] = 0
    prefs["download.default_directory"] = download_path
    options.add_experimental_option("prefs", prefs)

    webdriver = webdriver.Chrome(chrome_options = options, executable_path = chromedriver_path)
    print(userAgent)
    print("Opened chromedriver")
    time.sleep(5)
    webdriver.get("https://www.google.co.in")

    count = 1
    not_resolved = []

    base_url = "https://drive.google.com/uc?export=download&"
    for link in all_links:
        try:
            initial_num_files = len([name for name in os.listdir('.') if os.path.isfile(name)])
            param = link.split("?")[1].split("&")[0]
            new_link = base_url + param
            webdriver.get(new_link)
            # print(new_link)
            print("Opened Link", count)
            count += 1
            time.sleep(15)
            final_num_files = len([name for name in os.listdir('.') if os.path.isfile(name)])
            if (final_num_files == initial_num_files):
                not_resolved.append(link)
                print("Oooops, couldn't resolve")
        except:
            print("Ooops, couldn't resolve")
            not_resolved.append(link)

    dir_name = "C:/Users/unitel/Desktop/Snap"
    os.chdir(dir_name)
    outfile = "notresolved_links.txt"
    fout = open(outfile, "w")
    for i in not_resolved:
        fout.write(i)
        fout.write("\n")
    fhand.close()
    print("Finished writing", outfile, "to disk.")
    webdriver.close()

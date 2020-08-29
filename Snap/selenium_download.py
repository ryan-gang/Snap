import os
import time
from fake_useragent import UserAgent
from selenium.webdriver.chrome.options import Options


def selenium_download():
    from selenium import webdriver

    file = "drive_links.txt"
    with open(file, "r") as fhand:
        all_links = fhand.read().split("\n")

    options = Options()
    ua = UserAgent()
    userAgent = ua.random
    print(userAgent)
    options.add_argument(f'user-agent={userAgent}')
    dir_name = "C:/Users/unitel/Desktop/Snap/Downloads"
    os.chdir(dir_name)
    chromedriver_path = 'C:/Users/unitel/Downloads/chromedriver.exe'
    webdriver = webdriver.Chrome(chrome_options = options, executable_path = chromedriver_path)
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
    webdriver.close()

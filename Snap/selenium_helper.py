import os
from time import sleep
from selenium import webdriver
from fake_useragent import UserAgent
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from Snap.helper import *


def seleniumhelper(end_date_user):
    options = Options()
    ua = UserAgent()
    userAgent = ua.random
    print(userAgent)
    options.add_argument(f'user-agent={userAgent}')

    dir_name = "C:/Users/unitel/Desktop/Snap/"
    os.chdir(dir_name)
    chromedriver_path = 'C:/Users/unitel/Downloads/chromedriver.exe'  # Change this to your own chromedriver path!
    wd = webdriver.Chrome(chrome_options=options, executable_path=chromedriver_path)
    print("Opened chromedriver")
    # sleep(2)

    homepage = "https://web.snapworks.me/users/login"
    docspage = "https://web.snapworks.me/parent-students/activities"
    wd.get(homepage)
    print("Reached homepage")

    username = wd.find_element_by_xpath("//input[@id = 'UserEmail']")
    # mail = getpass("Enter the Email : ")
    username.send_keys(mail)
    print("Putting in username")
    sleep(3)

    # TODO
    password = wd.find_element_by_xpath("//input[@id = 'UserPassword']")
    # passw = getpass("Enter the Password : ")
    password.send_keys(passw + Keys.RETURN)
    print("Putting in password")
    sleep(5)
    print("Let's goooo!")

    wd.get(docspage)

    webpage = wd.page_source
    earliest_date = min(get_all_dates(webpage))
    print("Data parsed upto :", earliest_date)
    while (earliest_date > end_date_user):
        button = wd.find_element_by_xpath("//button[@id = 'load_more']")
        button.click()
        webpage = wd.page_source
        earliest_date = min(get_all_dates(webpage))

    write_html(webpage, "fullwebsite.html")

    wd.close()
    wd.quit()
    return

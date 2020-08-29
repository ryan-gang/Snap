from selenium_helper import *
from selenium_download import *

if __name__ == '__main__':
    end_date = input("Enter the latest date (DD/MM/YYYY) upto which you wish to fetch documents : ")
    try:
        end_date_user = datetime.strptime(end_date, "%d/%m/%Y")
    except ValueError:
        print("Please enter date in DD/MM/YYYY format.")
        SystemExit("Couldn't parse date")

    r = get_site()
    if (r.status_code != 200):
        SystemExit("Server didn't respond")
    else:
        dates = get_all_dates(r.text)
        earliest_date = min(dates)
        print("Earliest date :", earliest_date)
        if (earliest_date > end_date_user):
            print("All documents not avalaible throught Get request")
            print("Will attempt to get the site through Chromium")
            seleniumhelper(end_date_user)
        else:
            write_html(r.text)

    get_all_links()
    clean_links()
    selenium_download()

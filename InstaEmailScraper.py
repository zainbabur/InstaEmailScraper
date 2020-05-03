'''
This web scraping script searches google for instagram profiles
matching a certain keyword, opens those profiles and gets emails
from their bio, if provided.
Made by Zain
'''

from googlesearch import search
from selenium import webdriver
from bs4 import BeautifulSoup as soup
import time
import regex as re
import pandas as pd

#!initializing path
dest_path = 'C:\\Users\\Zain Babur\\Documents\\PythonProjects\\InstaEmailScraper\\'

#!defining keyword and website
keyword = "health"
site = "instagram.com"

#!initializing empty lists to append information into
url_list=[]
mailing_list=[]
new_url_list=[]

#!making chrome headless to save memory/cpu
options = webdriver.ChromeOptions()
options.add_argument('--headless')

#!Searching google and returnng the first 100 URLs
for i in search(keyword+" site:"+site,tld = 'com',lang = 'en',num = 20,start = 0,stop = 100,pause = 2.0):
    url_list.append(i)

for url in url_list:
    with webdriver.Chrome("C:\\ChromeDriver\\chromedriver.exe", chrome_options=options) as driver:    
        
        #!open url and wait 20 seconds for it to fully load
        driver.get(url)
        time.sleep(20)

        #!get html from the page
        my_html = driver.page_source

        #!passing html to beautifulsoup 
        my_soup = soup(my_html, "html.parser")

    #!find <div> which contains bio
    bio = my_soup.find("div", class_="-vDIg")

    #!using regex to identofy email address, otherwise append empty string
    try:
        emails = re.findall('\w+@\w+\.{1}\w+', bio.text)
    except:
        emails = ''

    #!if that bio had email address(es)    
    if len(emails) != 0:

        #!initializing empty string to store email
        inner_email_list=''

        #!append all emails found for one page and append into a string
        for email in emails:
            inner_email_list += email+';'
        
        #!Append email string and corresponding url to lists
        mailing_list.append(inner_email_list)
        new_url_list.append(url)

#!Make a dataframe, fill with information and write to csv
result = pd.DataFrame()
result['URL'] = new_url_list
result['Emails'] = mailing_list
result.to_csv(dest_path+'Output.csv', index=False)





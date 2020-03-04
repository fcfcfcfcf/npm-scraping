import requests
from bs4 import BeautifulSoup
import re
import random
import hashlib
import time
import threading
import logging
import concurrent.futures
import csv
import json


#function for getting the readme of a url
#has to be valid npm url to package
def get_readme_of_page(url):
    try:
      #getting html of page
        proxies = randomProxy()
        userAgent = randomUserAgent()
        the_text = requests.get(url, headers={'user-agent' : userAgent})#, proxies=proxies)
        while the_text.status_code == 429:
            time.sleep(60)
            the_text = requests.get(url, headers={'user-agent' : userAgent})#, proxies=proxies)
            print(the_text.status_code)
        text = json.loads(the_text.text)
      
      #soup = BeautifulSoup(text, 'html.parser')
      #readme = soup.find('article')
        return(str(text['readme']))
    except Exception as e:
        print(e)
        print('was probably blocked')
        exit()

def randomProxy():
    list_of_proxy = ['96.9.67.84:8080', '217.138.212.125', '84.17.51.193', '200.60.124.109:8080', '125.62.213.33:83', '187.63.18.215:3128', '84.17.47.196']
    ran = random.random()*7
    proxy = {'http' : 'http://' + list_of_proxy[int(ran)] }
    return(proxy)

def randomUserAgent():
    headersDB = {0 : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246", 1 : "Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWeb  Kit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36", 2 : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9", 3 : "Mozilla/5.  0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1", 4 : "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/  604.1", 5 : "Mozilla/5.0 (iPhone9,4; U; CPU iPhone OS 10_0_1 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/14A403 Safari/602.1"}
    ran = random.random()*6
    userAgent = headersDB[int(ran)]
    return(userAgent)

def get_name_ready_for_readme(package_name):
    versions_url = 'https://replicate.npmjs.com/' + package_name
    return(versions_url)


def drews_grepping(list_from_csv):
    perp_url = get_name_ready_for_readme(list_from_csv[0])
    perp_readme = get_readme_of_page(perp_url)
    for i in range(1, len(list_from_csv)):
        matches = open('allTheMatches.txt', 'a')
        no_match = open('doesntMatch.txt', 'a')
        target = ' ' + str(list_from_csv[i]) + ' '
    	#if(re.match(target, perp_readme)):
        if(perp_readme.find(target) >= 0):
            print(target + '\t\thas a match in the readme of\t\t' + list_from_csv[0] + '\n')
            matches.write(target + '\t\thas a match in the readme of\t\t' + list_from_csv[0] + '\n')
        else:
            print(target + '\t\tdoes not match in the readme of \t\t' + list_from_csv[0] + '\n')
            no_match.write(target + '\t\tdoes not match in the readme of \t\t' + list_from_csv[0] + '\n')
            matches.close()
            no_match.close()

def big_list_of_packages():
    perpetrators = []
    with open('npm_typosquatting_perpetrators.csv') as csvfile:
      	pkg_reader = csv.reader(csvfile, delimiter=',')
      	for row in pkg_reader:
            new_perpetrator = []
            for ind in range (len(row)):
                if ind%2 == 0:
                    if row[ind] != '':
                        new_perpetrator += [row[ind]]
            perpetrators += [new_perpetrator]
    return(perpetrators)

def main():
    all_packages = big_list_of_packages()
    print('got all the packages loaded')

    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(drews_grepping, all_packages)
    matches.close()
    no_match.close()

main()

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

matches = open('allTheMatches.txt', 'w+')
no_match = open('doesntMatch.txt', 'w+')

#function for getting the readme of a url
#has to be valid npm url to package
def get_readme_of_page(url):
    try:
        #getting html of page
        the_text = requests.get(url)
        while the_text.status_code == 429:
            time.sleep(20)
            the_text = requests.get(url)
        text = the_text.text
        soup = BeautifulSoup(text, 'html.parser')
        readme = soup.find('article')
        return(readme.text)
    except Exception as e:
        print(e)
        print('was probably blocked')
        exit()

# format = "%(asctime)s: %(message)s"
# logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
# threads = list()

# for i in range(10):
#     logging.info("Creating and starting thread %d.", i)
#     new_thread = threading.Thread(target=get_readme, ars=(,)) #put urls in args when we have csv
#     threads.append(new_thread)
#     new_thread.start()
   
def get_name_ready_for_readme(package_name):
    versions_url = 'https://www.npmjs.com/package/' + package_name
    return(versions_url)

def drews_grepping(list_from_csv):
    perp_url = get_name_ready_for_readme(list_from_csv[0])
    perp_readme = get_readme_of_page(perp_url)
    for i in range(1, len(list_from_csv)):
        target = ' ' + str(list_from_csv[i]) + ' '
        #if(re.match(target, perp_readme)):
        if(perp_readme.find(target) >= 0):
            print(target + '\t\thas a match in the readme of\t\t' + list_from_csv[0] + '\n')
            matches.write(target + '\t\thas a match in the readme of\t\t' + list_from_csv[0] + '\n')
        else:
            print(target + '\t\tdoes not match in the readme of \t\t' + list_from_csv[0] + '\n')
            no_match.write(target + '\t\tdoes not match in the readme of \t\t' + list_from_csv[0] + '\n')

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
    with concurrent.futures.ThreadPoolExecutor(max_workers=13) as executor:
        executor.map(drews_grepping, all_packages)
    matches.close()
    no_match.close()

main()








#returns a list of all versions from latest to oldest
def getAllVersions(url):
    try:
    
        list_of_versions = []
        the_latest_version = ''
        the_text = requests.get(url)
        while the_text.status_code == 429:
            time.sleep(20)
            the_text = requests.get(url)
        text = the_text.text
        soup = BeautifulSoup(text, 'html.parser')
        try:
            #this is because we are not assured that there will be a latest version     
            allVersions = soup.findAll('ul', {'class', 'c495d29d list ml0 pl0'}) 
            #checking if there is a latest version
            latest_version = allVersions[0]
            the_latest_version = latest_version.find('a', href=True)
            #had to remove text from number
            #the_latest_version = re.match(r'.*latest', latest_version)
            list_of_versions.append(url + the_latest_version['href'])

            other_versions = allVersions[1]
            #print(allVersions[1])
            for a in other_versions.find_all('a', href=True):
                list_of_versions.append(url + a['href'])

        except Exception as e:
            allVersions = soup.find('ul', {'class', 'c495d29d list ml0 pl0'})
            other_versions = allVersions[0]
            #print(allVersions[1])
            for a in other_versions.find_all('a', href=True):
                list_of_versions.append(url + a['href'])
        return(list_of_versions)
        
    except Exception as e:
        print(e)

def grepping_not_hashing():
    all_packages = big_list_of_packages()
    print('got all the packages loaded')
    for instance in all_packages:
        drews_grepping(instance)
    matches.close()
    no_match.close()

def hashing_not_grepping():
    all_packages = big_list_of_packages()
    print('packages loaded')

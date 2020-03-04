import requests
from bs4 import BeautifulSoup
import re
import random
import hashlib
import time


big_dict_of_hashes = {}


#function for getting the readme of a url
#has to be valid npm url to package
def get_readme_of_page(url):
    try:
        #getting html of page
        text = requests.get(url, timeout=10).text
        soup = BeautifulSoup(text, 'html.parser')
        readme = soup.find('article')
        return(readme.text)
    except Exception as e:
        print(e)
        print('was probably blocked')
        exit()

#returns a list of all versions from latest to oldest
def getAllVersions(url):
    try:
        list_of_versions = []
        the_latest_version = ''
        text = requests.get(url).text
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



def get_name_ready_for_readme(package_name):
    versions_url = 'https://www.npmjs.com/package/' + package_name
    return(versions_url)

def drews_grepping(list_from_csv):
    perp_url = list_from_csv[0]
    perp_readme = get_readme_of_page(perp_url)
    for target in list_from_csv:
        re.match(target, perp_readme) 

the_soup = print(getAllVersions('https://www.npmjs.com/package/lodash?activeTab=versions'))

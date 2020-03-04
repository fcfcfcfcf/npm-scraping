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



big_dict_of_hashes = {}
#function for getting the readme of a url
#has to be valid npm url to package
def get_readme(url):
    try:
        #getting html of page
        text = requests.get(url, timeout=10).text
        soup = BeautifulSoup(text, 'html.parser')
        #retrieve readme from that place 
        readme = soup.find('article')
        return(readme.text)
    except Exception as e:
        print(e)
        exit()




perpetrators = []
print(get_readme('https://www.npmjs.com/package/loadsh'))
with open('npm_typosquatting_perpetrators.csv') as csvfile:
    pkg_reader = csv.reader(csvfile, delimiter=',')
    for row in pkg_reader:
        new_perpetrator = []
        for ind in range (len(row)):
            if ind%2 == 0:
                if row[ind] != '':
                    new_perpetrator += [row[ind]]
        perpetrators += [new_perpetrator]
print(str(perpetrators))


                
# format = "%(asctime)s: %(message)s"
# logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
# threads = list()

# for i in range(10):
#     logging.info("Creating and starting thread %d.", i)
#     new_thread = threading.Thread(target=get_readme, ars=(,)) #put urls in args when we have csv
#     threads.append(new_thread)
#     new_thread.start()
   





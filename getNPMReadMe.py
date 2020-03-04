import requests
from bs4 import BeautifulSoup
import re
import random
import hashlib
import time
import threading
import logging
import concurrent.futures


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





print(get_readme('https://www.npmjs.com/package/loadsh'))
    
format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
threads = list()

for i in range(10):
    logging.info("Creating and starting thread %d.", i)
    new_thread = threading.Thread(target=get_readme, ars=(,)) #put urls in args when we have csv
    threads.append(new_thread)
    new_thread.start()
   





import requests
from bs4 import BeautifulSoup
import time
import urllib.parse

global_var_of_dependents = 0

loadsh_url = "https://www.npmjs.com/browse/depended/loadsh"
dependents_url = "https://www.npmjs.com/browse/depended/"
other_depend = "https://www.npmjs.com"

def getPage(url, the_set):
    global global_var_of_dependents
    global set_of_dependents
    try:
        print(url)
        #print(global_var_of_dependents)
        s = requests.get(url, timeout=20)
        if s.status_code == 429:
            print('we got blocked for a bit')
            exit()
        if s.status_code == 404:
            print('we have a problem with the code')
            print(url)
            exit()
        r = s.text
        time.sleep(1)
        soup = BeautifulSoup(r, 'html.parser')
        dependents = soup.findAll('div', {'class', 'flex flex-row items-end pr3'})
        if len(dependents) == 0:
            return
        print(global_var_of_dependents)
        global_var_of_dependents += len(dependents)
        dependent_names = [x.text for x in dependents]
        for name in dependent_names:
            the_set.add(name)
            name = urllib.parse.quote(name)
            dep_name_url = dependents_url + name

            getPage(dep_name_url, the_set)
        
        #finding the next page
        link_dict = {}
        hrefs = soup.findAll('a', href=True)
        for h in hrefs:
            link_dict[h.text] = h
        if "Next Page" in link_dict:
            getPage(other_depend + link_dict["Next Page"]['href'], the_set)
        print(the_set)
        print(len(the_set))
    except Exception as e:
        print(e)

    print(global_var_of_dependents)

getPage(loadsh_url, set())

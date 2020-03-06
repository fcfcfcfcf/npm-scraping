import hashlib
import sys
import csv
import re
import json
import requests
import subprocess
import urllib.request
import os
from os import listdir
from os.path import isfile, join
import glob

#read in packages from file
def get_package_names():
    pattern = re.compile('[^\t]+')
    package_matches = []
    package_pairs = []
    with open('allTheReadMeMatch.txt', 'r') as f:
        package_matches = f.readlines()

    for p in package_matches:
        p.strip()
        p.split('\t')
        perp = pattern.findall(p)[-1].strip()
        victim = pattern.findall(p)[0].strip()
        package_pairs.append([perp, victim])

    return(package_pairs)

def get_package_url(package_name):
    return 'https://replicate.npmjs.com/' + package_name

def get_package_json(url):
    page_text = requests.get(url)
    json_text = json.loads(page_text.text)
    return json_text

def hash_dir(my_dir):
    big_hash = ''
    filenames = glob.glob(my_dir + '/**/*', recursive=True)
    for filename in filenames:
        if not 'package.json' in filename:
            try: 
                with open(filename, 'rb') as inputfile:
                    data = inputfile.read()
                    big_hash += hashlib.md5(data).hexdigest()
            except:
               pass 
    return big_hash


    
cur_dir = '/mnt/c/Users/jam60/OneDrive/Repos/npm-scraping'
packages = get_package_names()
f = open("results.txt", "w")
def download_perp_tars():
    for p in packages:
        perp_package_json = get_package_json(get_package_url(p[0]))
        perp_versions = perp_package_json['versions']
        vict_package_json = get_package_json(get_package_url(p[1]))
        vict_versions = vict_package_json['versions']
        last_name = ''
        for x in perp_versions:
            last_name = x 
        perp_ver_tar_link = perp_versions[last_name]['dist']['tarball']
        tar_file_name = p[0] + '-' + last_name + '.tgz'
        perp_ver_tar_file = urllib.request.urlretrieve(perp_ver_tar_link, './tar_files/' + tar_file_name)
        dir_to_make = cur_dir + '/packages/' + p[0] + last_name
        subprocess.run(['mkdir', dir_to_make])
        subprocess.run(['tar', '-C', cur_dir + '/packages/' + p[0] + last_name, '-xzf', cur_dir + '/tar_files/' + tar_file_name])
        perp_hash = hash_dir(cur_dir + '/packages/' + p[0] + last_name)
        foundMatch = False
        for x in vict_versions:
            perp_ver_tar_link = vict_versions[x]['dist']['tarball']
            tar_file_name = p[1] + '-' + x + '.tgz'
            vict_ver_tar_file = urllib.request.urlretrieve(perp_ver_tar_link, './tar_files/' + tar_file_name)
            dir_to_make = cur_dir + '/packages/' + p[1] + x
            subprocess.run(['mkdir', dir_to_make])
            subprocess.run(['tar', '-C', cur_dir + '/packages/' + p[1] + x, '-xzf', cur_dir + '/tar_files/' + tar_file_name])
            vict_hash = hash_dir(cur_dir + '/packages/' + p[1] + x)
            if vict_hash == perp_hash:
                foundMatch = True
                
                f.write(p[0] + '-' + last_name + ' matches with ' + p[1] + '-' + x)
                print('found match!')
                os.system('cp -R ' + dir_to_make + ' ./hits')
                os.system('cp -R ' + cur_dir + '/packages/' + p[0] + last_name + ' ./hits')

        if not foundMatch:
            os.system('cp -R ' + cur_dir + '/packages/' + p[0] + last_name + ' ./not_hits')
            os.system('rm -rf ' + cur_dir + '/packages/*')

                

download_perp_tars()

f.close()
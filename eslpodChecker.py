#!/usr/bin/env python3

import urllib.request
from bs4 import BeautifulSoup
from os import listdir
from os.path import isfile, join
from os import remove
import re
import logging

FILES_PATH = "/home/tutunak/manuals/english/eslpod"
logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%YY %I:%M:%S %p', filename=FILES_PATH + '/eslcheck.log', level=logging.INFO)

def main(url, lastCount):
    logging.info('Started')
    linkList = []
    html = urllib.request.urlopen(url).read()
    soupPage = BeautifulSoup(html, "lxml")
    tags = soupPage('a')
    for tag in tags:
        link = tag.get('href', None)
        if (re.match("^http.+mp3$", link)) != None:
            linkList.append(link)
            #print(link)
        if len(linkList) >= lastCount: break
    check_files(linkList)


def check_files(linkList):
    files = [f for f in listdir(FILES_PATH) if isfile(join(FILES_PATH, f))]
    fne = {}
    all_files = {}
    for link in linkList:
        filename = re.search("^.+\/(.+mp3$)", link).group(1)
        if filename  not in files:
            logging.info("found new file: " + filename)
            #print("file not exist ", filename)
            fne[filename] = link
        all_files[filename] = link
    files_download(fne)
#    delete_old(files, all_files)


def files_download(download_list):
    for key in download_list:
        urllib.request.urlretrieve(download_list[key], FILES_PATH+"/"+key)
        logging.info("downloaded file: " + download_list[key])

def delete_old(files, download_list):
    for filename in files:
        if filename not in download_list:
            print('deletefile: ', filename)
            remove(FILES_PATH + "/" + filename)

if __name__ == '__main__':
    url = "https://www.eslpod.com/website/show_all.php"
    lastCount = 10
    main(url, lastCount)

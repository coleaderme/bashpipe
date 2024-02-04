#!/usr/bin/env python
# hqp.sh port to python for..well portability.
# easy maintain :)
# less flimsy than sh :)
# less performant than sh :(
from sys import argv
from bs4 import BeautifulSoup
from subprocess import run
import httpx
import re
res = "360" ## change here resolution [360,720,1080]

def getPage(pUrl, res):
    headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'en-US,en;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    }
    ## getting player page url
    with httpx.Client() as client:
        vPage = client.get(pUrl, headers=headers, timeout=5)
        if vPage.status_code != 200:
            print('[-] Unable to reach: ' + pUrl + "\n- check your connection\n- use wireguard/vpn/proxy.")
            return False

        soup = BeautifulSoup(vPage.content, features="lxml")
        videoPageUrl = "https:" + soup.iframe['src']
        print(videoPageUrl) ## tags are objects <a> <header> <div>..

        ## extracting title & casts name from html.
        title = soup.title.string.replace(" - HQporner.com",'')
        print("[+] " + title)
        casting = 'unknown'
        for i in soup.find_all('li'):
            try:
                if "featuring" in i.text:
                    casting = i.text.strip()
                    print("[+] " + casting)
            except:
                pass

        ## url re-construction from player.js
        vPlayer = client.get(videoPageUrl, headers=headers).content

        soup = BeautifulSoup(vPlayer, features="lxml")
        regexStr = soup.find_all("script")[-2].text

        p = re.compile(r'replaceAll\(\"nrpuv\",+\w+\+\"pubs\/\"\+\w+')
        ## .group() is equivalent of --only-matching part.
        v = re.search(p,regexStr).group()[19:]
        r1 = v.split("+")[0]
        r2 = v.split("+")[-1]
        rp1 = re.compile(f'{r1}=\"\/\/+\w+')
        rp2 = re.compile(f'{r2}=\"\w+\.\w+')
        cdn = re.search(rp1,regexStr).group()[-3:]
        uri = re.search(rp2,regexStr).group().split('\"')[-1]
        directUrl = "https://" + cdn + ".bigcdn.cc/pubs/" + uri + "/" + res + ".mp4"
        print(directUrl)
        filename = (title + "-" + casting).replace(' ','_') + '.mp4'

        with open("log.txt", 'a') as log:
            log.write(f'input url: {pUrl}\n')
            log.write(f'player url: {videoPageUrl}\n')
            log.write(f'title: {title}\n')
            log.write(f'casts: {casting}\n')
            log.write(f'filename: {filename}\n')
            log.write(f'direct url: {directUrl}\n')
            log.write('==================================\n')

        run(["aria2c", directUrl, "-o", filename])



## main starts here ##
urlsCollection = []

for url in argv[1:]:
    if ("hqporner" in url) and ("https://" in url) and (".html" in url):
        print("Getting: " + url)
        urlsCollection.append(url)
    else:
        print(":: Invalid url: " + url)

if urlsCollection:
    for url in urlsCollection:
        getPage(url, res)

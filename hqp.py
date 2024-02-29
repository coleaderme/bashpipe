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

res = "360"  ## change here resolution [360,720,1080]


def getPage(pUrl, res):
    headers = {
        "Referer": "https://hqporner.com/?q=a",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    }

    ## getting player page url
    with httpx.Client() as client:
        vPage = client.get(pUrl, headers=headers, timeout=5)
        if vPage.status_code != 200:
            print(
                "[-] Unable to reach: "
                + pUrl
                + "\n- check your connection\n- use wireguard/vpn/proxy."
            )
            return False

        soup = BeautifulSoup(vPage.content, features="lxml")
        videoPageUrl = "https:" + soup.iframe["src"]
        print("[+] From " + videoPageUrl)  ## tags are objects <a> <header> <div>..

        ## extracting title & casts name from html.
        title = soup.title.string.replace(" - HQporner.com", "")
        print("[+] " + title)
        casting = "unknown"
        for i in soup.find_all("li"):
            try:
                if "featuring" in i.text:
                    casting = i.text.strip()
                    print("[+] " + casting)
            except:
                pass

        ## url re-construction from player.js
        vPlayer = client.get(videoPageUrl, headers=headers)
        if vPlayer.status_code != 200:
            print("[-] Couldn't get vPlayer page", vPlayer)
            return False

        p = re.compile(r"\/\/+\w+\.bigcdn\.cc\/pubs\/\w+\.\w+")
        soup = BeautifulSoup(vPlayer.content, features="lxml")
        for s in soup.find_all("script"):
            try:
                v = re.search(p, s.text).group()
                print(f"[+] found{v}")
            except:
                pass

        directUrl = "https:" + v + "/" + res + ".mp4"
        print(directUrl)
        filename = (title + "-" + casting).replace(" ", "_") + ".mp4"

        with open("log.txt", "a") as log:
            log.write(f"input url: {pUrl}\n")
            log.write(f"player url: {videoPageUrl}\n")
            log.write(f"title: {title}\n")
            log.write(f"casts: {casting}\n")
            log.write(f"filename: {filename}\n")
            log.write(f"direct url: {directUrl}\n")
            log.write("==================================\n")

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

#!/usr/bin/env python
# hqp.sh port to python for..well portability.
# easy maintain :)
# less flimsy than sh :)
# less performant than sh :(
# from bs4 import BeautifulSoup
from sys import argv
from selectolax.parser import HTMLParser # pip install selectolax (also cython if required)
from subprocess import run
import httpx
import re

res = "360"  ## change here resolution [360,720,1080]

headers = {
    "Referer": "https://hqporner.com/?q=a",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
}

def getPage(pUrl: str, res: str):
    ## getting player page url
    with httpx.Client(headers=headers,timeout=30) as client:
        vPage = client.get(pUrl,)
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
                    break
            except:  # noqa: E722
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
            except:  # noqa: E722
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

        run(
            [
                "aria2c",
                "--header=User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
                "--header=Referer: https://mydaddy.cc/",
                directUrl,
                "-o",
                filename,
            ]
        )

def main_bs4_method():
    urlsCollection = []
    for url in argv[1:]:
        if (
            (url.startswith("https://"))
            and ("hqporner" in url)
            and url.endswith(".html")
        ):
            print("Getting:: " + url)
            print("resolution: " + res)
            urlsCollection.append(url)
        else:
            print("Invalid url:: " + url)

    if urlsCollection:
        for url in urlsCollection:
            getPage(url, res)

################################## New Method: using Selectolax ##################################


def fetch(url: str, client: httpx.Client)-> dict or bool:
    r = client.get(url)
    if r.status_code != 200:
        print("[-] Unable to reach: "+ url+ "\n- check your connection\n- use wireguard/vpn/proxy.")
        return False
    doc = HTMLParser(html=r.content, detect_encoding=True)
    
    video_page_url = "https:" + doc.css_first("iframe").attributes['src']
    print("[+] " + video_page_url)
    title = doc.css_first("title").text().replace(" - HQporner.com", "")
    print("[+] " + title)
    casting = "unknown"
    for i in doc.css("li"):
        i = i.text().strip()
        try:
            if "featuring" in i:
                casting = i
                print("[+] " + casting)
                break
        except:  # noqa: E722
            pass
    return {'url': video_page_url, 'title': title, 'casting': casting}

def player_js(video_page_url: str, client: httpx.Client)-> str or bool:
    ''' url re-construction from player.js '''
    directUrl = ''
    r = client.get(video_page_url)
    if r.status_code != 200:
        print("[-] Couldn't get player_js page", player_js)
        return False
    p = re.compile(r"\/\/+\w+\.bigcdn\.cc\/pubs\/\w+\.\w+")
    doc = HTMLParser(html=r.content, detect_encoding=True)
    for s in doc.css("script"):
        s = s.text().strip()
        try:
            uri = re.search(p, s).group()
            # print("[+] found " + uri)
            break
        except:  # noqa: E722
            pass
    directUrl = "https:" + uri + "/" + res + ".mp4"
    print("[+] "+directUrl)
    return directUrl

def valid_urls()->list[str]:
    urlsCollection = []
    for url in argv[1:]:
        if (
            (url.startswith("https://"))
            and ("hqporner" in url)
            and url.endswith(".html")
        ):
            print("Getting:: " + url)
            print("resolution: " + res)
            urlsCollection.append(url)
        else:
            print("Invalid url:: " + url)
    return urlsCollection

def main():
    urlsCollection = valid_urls()
    if not urlsCollection:
        print('hqp.py URL URL...')
        return False
    with httpx.Client(headers=headers, timeout=30) as client:
        for url in urlsCollection:
            info = fetch(url, client)
            if info:
                player_url = info['url']
                directUrl = player_js(player_url, client)
            if directUrl:
                title = info['title']
                casting = info['casting']
                filename = (title + "-" + casting).replace(" ", "_").replace("'","_") + ".mp4"
                with open("log.txt", "a") as log:
                    log.write(f"input url: {url}\n")
                    log.write(f"player url: {player_url}\n")
                    log.write(f"title: {title}\n")
                    log.write(f"casts: {casting}\n")
                    log.write(f"filename: {filename}\n")
                    log.write(f"direct url: {directUrl}\n")
                    log.write("==================================\n")
                print('run this command>>')
                print(f'aria2c --header="User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36" --header="Referer: https://mydaddy.cc/" {directUrl} -o "{filename}"')
                # run(
                # [
                #     "aria2c",
                #     "--header=User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
                #     "--header=Referer: https://mydaddy.cc/",
                #     directUrl,
                #     "-o",
                #     filename
                # ]
                # )

if __name__ == "__main__":
    main()

#!/usr/bin/env python

## Objective: port to windows.
## xh: https://github.com/ducaale/xh/releases/download/v0.18.0/xh-v0.18.0-x86_64-pc-windows-msvc.zip
import subprocess
from sys import argv
from datetime import datetime
import json
now = datetime.now()

try:
    url = argv[1]
except Exception as e:
    print("[-] No url entered")
    print("USAGE:\n./jdl YOUR_LINK_HERE\n")
def Downloader(token,title):
    ## expects token and title as input.
    input_url = f"https://www.jiosaavn.com/api.php?__call=webapi.get&token={token}&type=song&includeMetaTags=0&ctx=web6dot0&api_version=4&_format=json&_marker=0"
    print(f"[+] [{now.time()}] Downloading json...")
    ## get encrypted URL
    try:
        result = subprocess.check_output(
        [
            "xh",
            "--pretty=none",
            "--ignore-stdin",
            input_url,
            "user-agent:Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:49.0) Gecko/20100101 Firefox/49.0",
            "cache-control:private, max-age=0, no-cache",
        ],
        text=True,
        stderr=subprocess.STDOUT,  # To capture both stdout and stderr
        )
    except subprocess.CalledProcessError as e:
        print(f"[-] subprocess error:\n{e}")
    print(f"[+] [{now.time()}] Extracting url...")
    # enc_url=$(jq .songs[0].more_info.encrypted_media_url "$token".json) ## read json 
    song_json = json.loads(result) ## .load for file; .loads for string
    enc_url = song_json["songs"][0]["more_info"]["encrypted_media_url"] ## .load for file; .loads for string
    # print(enc_url)
    print(f"[+] [{now.time()}] Decrypting url...")
    try:
        dl_url = subprocess.check_output(["python", "./pyDes.py", enc_url], text=True,stderr=subprocess.STDOUT).strip()
    except subprocess.CalledProcessError as e:
        print(f"[-] [{now.time()}] Decrypting failed:\n{e}")

    print(f"[+] [{now.time()}] Dowloading file...")
    print(dl_url)
    subprocess.run(['wget', dl_url, '-O', f'{title}.m4a'])
    print(f"[+] [{now.time()}] Finished...")

token = 'IQocRkUFdgQ'
title = 'song'
Downloader(token=token, title=title)

#!/usr/bin/env python
## convert headers from wireshark and httptoolkit
## to request(python) compatible.

httptoolkit_h = """
Accept-Encoding:
gzip, deflate, br
Connection:
keep-alive
Host:
rr2---sn-bpb5oupj-qxal.googlevideo.com
User-Agent:
app.revanced.android.youtube/563923541 (Linux; Android 12)
"""

wireshark_h = """
:method: GET
:authority: usercontent.wynk.in
:scheme: https
:path: /usercontent/v4/user/playlists?count=48&offset=0
sec-ch-ua: "Not_A Brand";v="8", "Chromium";v="120"
x-bsy-coo: IN
x-bsy-cid: f303a8
sec-ch-ua-mobile: ?0
x-bsy-coa: IN
user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36
x-bsy-iswap: true
accept: application/json, text/plain, */*
sec-ch-ua-platform: "Linux"
origin: https://wynk.in
sec-fetch-site: same-site
sec-fetch-mode: cors
sec-fetch-dest: empty
referer: https://wynk.in/
accept-encoding: gzip, deflate, br
accept-language: en-US,en;q=0.9
"""


def httptoolkit(headers: str) -> dict:
    py_headers = {}
    # [return >> for loop >> if-else]
    h = [i.strip() for i in headers.split("\n") if i != ""]
    for i, v in enumerate(h):
        # when index equals last item, skip.
        if v.endswith(":"):
            v = v[:-1]  # removes trailing':'
            py_headers[v] = h[i + 1]
            # print(i,v)
            continue
    print(py_headers)
    return py_headers


def wireshark(headers: str) -> dict:
    py_headers = {}
    h = [i.strip() for i in headers.split("\n") if i != ""]
    try:
        url = [i.split(":", 1)[-1].strip() for i in h if "origin" in i][0]
        url = url + [i.split(":")[-1].strip() for i in h if ":path:" in i][0]
        print(f"url: {url}")
    except Exception:
        print("Error: Assembling URL")
    for i in h:
        if i.startswith(":"):
            continue
        k, v = i.split(":", 1)
        py_headers[k.strip()] = v.strip()
    print(py_headers)
    return py_headers


wireshark(wireshark_h)
httptoolkit(httptoolkit_h)

#!/usr/bin/env python
# usage:
# python tags.py simba.m4a data.json

from sys import argv
from mutagen.mp4 import MP4
import html
import json

filename = argv[1]
json_input = argv[2]

with open(json_input) as j_file:
    for j in j_file:
        json_data = json.loads(j)

def addtags(filename, json_data):
    audio = MP4(filename)
    audio['\xa9nam'] = html.unescape(str(json_data["songs"][0]["title"]))
    audio['\xa9ART'] = html.unescape(str(json_data["songs"][0]["more_info"]["artistMap"]["primary_artists"][0]["name"]))
    audio['\xa9alb'] = html.unescape(str(json_data["songs"][0]["more_info"]["album"]))
    audio['aART'] = ", ".join([artist["name"] for artist in json_data["songs"][0]["more_info"]["artistMap"]["primary_artists"]])
    audio['\xa9wrt'] = html.unescape(str(json_data["songs"][0]["more_info"]["music"]))
    audio['desc'] = html.unescape(str("")) ## description is empty for now
    audio['\xa9day'] = html.unescape(str(json_data["songs"][0]["year"]))
    audio['cprt'] = html.unescape(str(json_data["songs"][0]["more_info"]["label"]))
    audio.save()

addtags(filename,json_data)
print(f"[+] {filename} Tagged!")
#!/usr/bin/sh
#
# Usage: ./jdl YOUR_LINK_HERE
[ -z $1 ] && echo "USAGE:\n./jdl YOUR_LINK_HERE\n" && exit
echo "[+] STARTED: `date +%s`"
################### downloader ####################
downloader(){
## expects token and title as input.
token=$1
title=$2
input_url="https://www.jiosaavn.com/api.php?__call=webapi.get&token=$token&type=song&includeMetaTags=0&ctx=web6dot0&api_version=4&_format=json&_marker=0"
echo "[+] [`date +%s`] Downloading/Extracting json"
## get encrypted URL
enc_url=$(xh --pretty=none --ignore-stdin "$input_url" "user-agent:Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:49.0) Gecko/20100101 Firefox/49.0" "cache-control:private, max-age=0, no-cache" | jq .songs[0].more_info.encrypted_media_url)
echo "[+] [`date +%s`] Decrypting url"
dl_url=$(python ../pyDes.py "$enc_url")
echo "[+] [`date +%s`] Dowloading"
wget "$dl_url" -O $title.m4a
echo "[+] [`date +%s`] Downloaded: $title.m4a"
}

################### album songs #################
## Complete album dl:
album_dl(){
echo "[+] Identified: Album"
album=$(echo "$1" | choose -f '/' -2)
mkdir "$album"
cd $album
# $1 is album url
items=$(xh "$1" | htmlq -a href a | rg  "/song")
for i in $items; do
    title=$(echo "$i" | choose -f '/' -2)
    token=$(echo "$i" | choose -f '/' -1)
    ## download in parallel //
    downloader "$token" "$title" &
done
}

################### single #####################
## Quick single dl:
track_dl(){
echo "[+] Identified: Track"
mkdir singles
cd singles
# $1 is song url
title=$(echo "$1" | choose -f '/' -2)
token=$(echo "$1" | choose -f '/' -1)
downloader "$token" "$title"
}

case "$1" in
    *song*) track_dl "$1" ;;
    *album*) album_dl "$1" ;;
    *) echo "[-] unable to identify :/" ;;
esac
echo "[+] FINISHED: `date +%s`" # shell is finished, download still going.
exit
#!/usr/bin/sh
# Pre-requisites:
# xh, rg (ripgrep), htmlq, jq
# easily available on arch linux.

# Usage: ./jdl YOUR_LINK_HERE
[ -z $1 ] && echo "USAGE:\n./jdl YOUR_LINK_HERE\nCan download from urls in input.txt\n./jdl input.txt" && exit
echo "[+] STARTED: `date +%s`"

## Not sure how this function works.
################## Timeout #####################
wait_with_timeout() {
    local timeout=$1
    local start_time=$(date +%s)

    # Wait for background processes
    wait

    local end_time=$(date +%s)
    local elapsed_time=$((end_time - start_time))

    # If the elapsed time exceeds the timeout, kill remaining background processes
    if [ "$elapsed_time" -ge "$timeout" ]; then
        echo "Timeout reached. Killing remaining background processes."
        pkill -P $$  # Kill child processes
    fi
}
################### downloader ####################
downloader(){
## expects token, title and folder as input.
token=$1
title=$2
folder=$3
input_url="https://www.jiosaavn.com/api.php?__call=webapi.get&token=$token&type=song&includeMetaTags=0&ctx=web6dot0&api_version=4&_format=json&_marker=0"
echo "[+] [`date +%s`] Downloading/Extracting json"
## get encrypted URL
enc_url=$(xh --pretty=none --ignore-stdin "$input_url" "user-agent:Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:49.0) Gecko/20100101 Firefox/49.0" "cache-control:private, max-age=0, no-cache" | jq .songs[0].more_info.encrypted_media_url)
echo "[+] [`date +%s`] Decrypting url"
dl_url=$(python pyDes.py "$enc_url")
echo "[+] [`date +%s`] Dowloading"
wget -q -c -w 1 --random-wait --keep-session-cookies --save-cookies wcookies.txt --header='user-agent:Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:49.0) Gecko/20100101 Firefox/49.0' --header='cache-control:private, max-age=0, no-cache' "$dl_url" -O "$folder/$title.m4a"
echo "[+] [`date +%s`] Downloaded: '$folder/$title.m4a'"
}

################### album/playlist songs #################
## Complete album dl:
album_dl(){
echo "[+] Identified: Album"
album=$(echo "$1" | choose -f '/' -2)
mkdir "$album"
# $1 is album url
items=$(xh "$1" | htmlq -a href a | rg  "/song")
max_concurrent=5
bg_counter=0

for i in $items; do
    bg_counter=$(($bg_counter + 1))
    title=$(echo "$i" | choose -f '/' -2)
    token=$(echo "$i" | choose -f '/' -1)
    ## download in parallel //
    downloader "$token" "$title" "$album" &
    if [ "$bg_counter" -eq "$max_concurrent" ]; then
        wait_with_timeout 10
        bg_counter=0
    fi
done
wait_with_timeout 10
}

################ from file ####################
from_file(){
max_concurrent=5
bg_counter=0
echo "[+] Identified: From File"
mkdir custom_dls
# read line and store as variable $url.
while IFS= read -r url
do
    bg_counter=$(($bg_counter + 1))
    title=$(echo "$url" | choose -f '/' -2)
    token=$(echo "$url" | choose -f '/' -1)
    # save in custom_dls folder.
    downloader "$token" "$title" "custom_dls" &
    if [ "$bg_counter" -eq "$max_concurrent" ]; then
        wait_with_timeout 10
        bg_counter=0
    fi
done < $1 # <- input.txt containing urls.
wait_with_timeout 10
}

################### single #####################
## Quick single dl:
track_dl(){
echo "[+] Identified: Track"
mkdir singles
# $1 is song url
title=$(echo "$1" | choose -f '/' -2)
token=$(echo "$1" | choose -f '/' -1)
downloader "$token" "$title" "singles"
}

case "$1" in
    *song*) track_dl "$1" ;;
    *album*) album_dl "$1" ;;
    input*) from_file "$1" ;;
    *featured*) album_dl "$1" ;;
    *) echo "[-] Unable to Identify :/" ;;
esac
echo "[+] FINISHED: `date +%s`" # shell is finished, download still going.
exit

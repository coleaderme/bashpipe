#!/usr/bin/env sh
# downloader for hqp0rn3r dot com
#
# Pre-requisites:
# sudo pacman -S aria2c htmlq ripgrep sd 
# 

helper(){
    printf "USAGE:\n"
    printf "./hqs url <res>  <- default: 360"
    exit
}

Download(){
    ## input : videoUrl, filename, res (default: 360)
    
    ## HTML NAME
    f="$(printf "$1" | cut -d "/" -f5)"
    printf "[+] Getting: $1\n"
    printf "[+] Downloading: $2\n"
    printf "[+] Resoultion: $3\n"

    ## GET HTML (another one)
    aria2c -q --disable-ipv6=true --auto-file-renaming=false --console-log-level=warn --disk-cache=64M --show-console-readout=false --check-certificate=false --file-allocation=none -k 1M "$1" -o "$f.html"

    ## FINDING REGEX
    r=$(cat "$f.html" | rg --only-matching "replaceAll\(\"nrpuv\",+\w+\+\"pubs\/\"\+\w+")

    ## CDN
    r1="$(printf "$r" | choose -f ',' 1 | choose -f '\+' 0)"
    [ -z "$r1" ] && printf "[-] r1 not found\n" && exit || printf "[+] r1: $r1\n"
    cdnRegx="$(cat "$f.html" | rg --only-matching "$r1=\"\/\/+\w+" | sd "$r1=\"" "")"

    ## URI
    r2="$(printf "$r" | choose -f ',' 1 | choose -f '\+' 2)"
    [ -z "$r2" ] && printf "[-] r2 not found\n" && exit || printf "[+] r2: $r2\n"
    cdnRegx2="$(cat "$f.html" | rg --only-matching "$r2=\"\w+.\w+" | sd "$r2=\"" "")"

    ## Complete url
    url="https:$cdnRegx.bigcdn.cc/pubs/$cdnRegx2/$res.mp4"
    printf "[+] direct url: $url\n"
    
    ## Download..
    aria2c --no-conf -c -x 8 -j 8 -s 8 -k 2M \
    --allow-piece-length-change=true \
    --auto-file-renaming=false \
    --check-certificate=false \
    --console-log-level=warn \
    --disable-ipv6=true \
    --disk-cache=64M \
    --file-allocation=falloc \
    --header="Accept: */*" \
    --header="Referer: https://mydaddy.cc/" \
    --header="User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36" \
    "$url" -o "$2.mp4"
}

Extract(){
    ## input: url, res

    ## GET HTML
    htmlFile="$(printf "$1" | cut -d "-" -f 2)"
    aria2c -q --no-conf \
    --allow-piece-length-change=true \
    --auto-file-renaming=false \
    --check-certificate=false \
    --console-log-level=warn \
    --disable-ipv6=true \
    --disk-cache=64M \
    --file-allocation=none \
    --show-console-readout=false \
    --header="Accept: */*" \
    --header="Referer: https://mydaddy.cc/" \
    --header="User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36" \
    "$1" -o "$htmlFile"

    ## INFO
    vPage=$(htmlq -f "$htmlFile" "iframe" | rg --only-matching "video/+\w+/")
    [ -z "$vPage" ] && printf "[-] Unable to extract videoUrl\n" && exit || printf "[+] Extracted videoUrl: https://mydaddy.cc/$vPage\n"
    videoUrl="https://mydaddy.cc/$vPage"
    casting=$(htmlq -t -f "$htmlFile" "header" ".fa-star-o" | sd ' ' '_')
    filename="$(printf "$htmlFile" | cut -d "." -f 1)_$casting"
    printf "[+] Got: '$htmlFile'\n"
    
    Download "$videoUrl" "$filename" "$res"
}

### Starts Here ###
[ -z "$2" ]
case "$2" in
    360) res="$2" ;;
    720) res="$2" ;;
    1080) res="$2" ;;
    *) res="360" ;;
esac
    
[ -z "$1" ] && helper
case "$1" in
    *hqporner*) Extract "$1" "$res" ;;
    *) printf "[-] Invalid url\n" && exit ;;
esac

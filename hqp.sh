#!/usr/bin/env sh
# downloader for hqp0rn3r dot com
#
# Required: xh + aria2c 
# works on termux: pkg install xh aria2
#
helper(){
    printf "USAGE:\n"
    printf "./hqp URL Res  [default: 360]\n"
    exit
}

Download(){
    ## input : url, res (default: 360)
    res="$2"

    ## Name from URL
    f="$(echo "$1" | cut -d "/" -f5 | cut -d "." -f1)"

    printf "[+] Getting: $1\n"
    printf "[+] Resoultion: $2\n"
    
    printf "Getting: $1\n" >> log.txt
    printf "Resoultion: $2\n" >> log.txt

    printf "Getting HTML..\n"
    html="$(xh -F -I -4 --verify=no --timeout=30 --session=hqp --pretty=none "$1" "Referer: https://hqporner.com/?q=asd" "User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36")"
    
    ## Extract player url and casting.
    # rg: -m no. of matches
    printf "[+] Title: $f\n"
    player_url="https://$(echo "$html" | grep -m 1 -o -P "mydaddy\.cc\/video/\w+/")"
    printf "[+] Player Url: $player_url\n"
    casting="$(echo "$html" | grep -o -P "fa-star-o\">featuring <a href=\"\/actress\/[a-z-]+" | cut -d '/' -f3)"
    printf "[+] Featuring: $casting\n"
    

    printf "Player Url: $player_url\n" >> log.txt
    printf "Title: $f\n" >> log.txt
    printf "Featuring: $casting\n" >> log.txt    

    ## Player js html
    ## Get first line: sed "1p;d" 
    url="https:$(xh -F -I -4 --verify=no --timeout=30 --session=hqp --pretty=none "$player_url" "Referer: https://hqporner.com/?q=asd" "User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36" | grep -m 1 -o -P "\/\/+\w+\.bigcdn\.cc\/pubs\/\w+\.\w+" | sed "1p;d")/$res.mp4"
    
    printf "[+] Direct url: $url\n"
    printf "Check out log.txt"
    printf "Direct url: $url\n" >> log.txt
    printf "run command >>\n" >> log.txt
    printf "aria2c --allow-piece-length-change=true --disable-ipv6=true --header=\"Referer: https://mydaddy.cc/\" --header=\"User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36\" \"$url\" -o \"$f.mp4\"\n" >> log.txt
    echo "=============================================================================" >> log.txt
    
    ## Download
    aria2c \
    --allow-piece-length-change=true \
    --console-log-level=warn \
    --disable-ipv6=true \
    --header="Referer: https://mydaddy.cc/" \
    --header="User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36" \
    "$url" -o "$f.mp4"

}

### Starts Here ###

case "$2" in
    360) res="$2" ;;
    720) res="$2" ;;
    1080) res="$2" ;;
    *) res="360" ;;
esac

[ -z "$1" ] && helper
case "$1" in
    *hqporner*) Download "$1" "$res";;
    *) printf "[-] Invalid url\n" && exit ;;
esac

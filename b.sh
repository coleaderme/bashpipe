#!/usr/bin/bash

# ***************************
# Downloader for djsbuzz.in
# ***************************
usage_func(){
  echo ''
  echo -e "USAGE:\n  bash b.sh djsbuzz_url\n ./b.sh bash b.sh djsbuzz_url\n"
  echo "show this message: -h, --help"
  echo ''
}
if [[ $1 == '' || $1 == "--help" || $1 == "-h" ]]
then
  usage_func
  exit
elif [[ $1 != *"https://www.djsbuzz.in/"* ]]
then
  echo "[-] Only 'https://www.djsbuzz.in/*' urls are supported."
  usage_func
  exit
fi

echo "You've made it!"
exit
echo "[+] STAGE 1"
##~ Stage 1: site eXtract
xh "https://www.djsbuzz.in/category/dj-nyk/" | htmlq --attribute href a | rg --only-matching "https://www.djsbuzz.in/[a-z0-9]+-[a-z0-9]+-[a-z0-9].*?/" | uniq - rawUrls.txt

wait


##~ Stage 2: Look for hearthis OR mediafire type urls.
rawExt_func(){
  echo "+1"
  xh -4 -p b "$1" | htmlq --attribute href a | rg --only-matching "https://(hearthis\.at/djsbuzz\.in/|www\.mediafire\.com/file).*" >> pre_final.txt
}

echo "[+] STAGE 2"
echo "Adding to pre_final.txt"
while IFS= read -r url
do
  rawExt_func "$url" &
done < rawUrls.txt

wait

# Our custom download function
cust_func(){
  if [[ $1 == *"https://www.mediafire.com/file/"* ]]
  then
    # saving in file method:
    echo "[+] found mediafire.com url: Saved to real_MF_links.txt"
    xh "$1" -p b | rg --only-matching "https://download.*?\"" >> real_MF_links.txt
    
  else
    echo "[+] found hearthis.at url: downloading..."
    xh -d -4 -p b --follow --pretty=none "$1"
  fi
}

echo "[+] STAGE 3"
##~ Stage 3: Finally! it's download time.
while IFS= read -r url
do
  cust_func "$url" &
done < pre_final.txt
 
wait

echo ""
echo "[**] Downloading real_MF_links.txt"
aria2c --seed-time=0 --summary-interval 5 --user-agent=Mozilla/5.0 --file-allocation=falloc -c -j 6 -x 6 -s 6 -k 1M -i real_MF_links.txt
echo "[+] All files are downloaded."
echo "[+] Clean up:"
mv pre_final.txt pre_final.txt.old 
mv rawUrls.txt rawUrls.txt.old
mv real_MF_links.txt real_MF_links.txt.old
echo "[+] Exiting Gracefully"
#=========================================================
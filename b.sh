#!/usr/bin/bash

# *****************************************************
# Downloader for hearthis.at and Mediafire.com
# *****************************************************

# Our custom function
cust_func(){
  if [[ $1 == *"https://www.mediafire.com/file/"* ]]
  then
    # saving in file method:
    echo "[+] found mediafire.com url: saved to real_MF_links"
    xh "$1" -p b | rg --only-matching "https://download.*?\"" >> real_MF_links
    
    # direct DL method:
    # mfurl=$(xh "$1" -p b | rg --only-matching "https://download.*?\"")

  else
    echo "[+] found hearthis.at url: downloading..."
    xh -d -4 --follow --pretty=none "$1"
    
    # aria2c --seed-time=0 --summary-interval 5 --user-agent=Mozilla/5.0 --file-allocation=falloc -c -j 3 -x 3 -s 3 -k 1M "$1"
  fi
}

while IFS= read -r url
do
  cust_func "$url" &
done < mfdlinks
 
wait
echo ""
echo "[**] Downloading real_MF_links"
aria2c --seed-time=0 --summary-interval 5 --user-agent=Mozilla/5.0 --file-allocation=falloc -c -j 6 -x 6 -s 6 -k 1M -i real_MF_links
echo "All files are downloaded."

# =====================================================
# DJsbuzz links extractor :
# xh "https://www.djsbuzz.in/category/dj-nyk/" | htmlq --attribute href a | rg --only-matching "https://www.djsbuzz.in/[a-z0-9]+-[a-z0-9]+-[a-z0-9].*?/" | uniq - urls.txt
# =====================================================
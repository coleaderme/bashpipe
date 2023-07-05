#!/usr/bin/bash
if [[ $1 == '' ]]
then
  echo -e "usage:\n ./gitbash.sh 'commit message'\n"
  exit
fi
git add .
git commit -m "$1"
git push
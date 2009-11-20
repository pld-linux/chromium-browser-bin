#!/bin/sh                                                             

if [ ""!="$1" ]
then           
  rev=$1       
  fi             

  rev=$(wget -q -O - http://build.chromium.org/buildbot/snapshots/chromium-rel-linux/LATEST)

  echo "Fetching revision $rev"

  wget http://build.chromium.org/buildbot/snapshots/chromium-rel-linux/$rev/chrome-linux.zip -c -O chrome-linux32.zip
  wget http://build.chromium.org/buildbot/snapshots/chromium-rel-linux-64/$rev/chrome-linux.zip -c -O chrome-linux64.zip

#  echo -n "Update revision in spec? (yes, [N]o)? "
#  read ans
#  case "$ans" in
#  [yY]) # y0 mama
#          echo "Ok, updating."
#;;
#          esac

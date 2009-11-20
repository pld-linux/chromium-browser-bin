#!/bin/sh

if [ "$1" ]; then
	rev=$1
	echo "Using $rev..."
else
	echo -n "Fetching latest revno... "
	rev=$(wget -q -O - http://build.chromium.org/buildbot/snapshots/chromium-rel-linux/LATEST)
	echo "$rev"
fi

wget http://build.chromium.org/buildbot/snapshots/chromium-rel-linux/$rev/chrome-linux.zip -c -O chrome-linux32.zip
wget http://build.chromium.org/buildbot/snapshots/chromium-rel-linux-64/$rev/chrome-linux.zip -c -O chrome-linux64.zip

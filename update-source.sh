#!/bin/sh

if [ "$1" ]; then
	rev=$1
	echo "Using $rev..."
else
	echo -n "Fetching latest revno... "
	rev=$(wget -q -O - http://build.chromium.org/buildbot/snapshots/chromium-rel-linux/LATEST)
	echo "$rev"
fi

if [ ! -f chromium-browser32-r$rev.zip ]; then
	wget http://build.chromium.org/buildbot/snapshots/chromium-rel-linux/$rev/chrome-linux.zip -c -O chromium-browser32-r$rev.zip
	upload_32="chromium-browser32-r$rev.zip"
fi
if [ ! -f chromium-browser64-r$rev.zip ]; then
	wget http://build.chromium.org/buildbot/snapshots/chromium-rel-linux-64/$rev/chrome-linux.zip -c -O chromium-browser64-r$rev.zip
	upload_64="chromium-browser64-r$rev.zip"
fi

if [ -x ./dropin ]; then
	dropin=./dropin
elif [ -x ../dropin ]; then
	dropin=../dropin
fi

if [ "$dropin" ] && [ "$upload_32" -o "$upload_64" ]; then
	echo "Uploading to dropin. ^C to abort"
	$dropin $upload_32 $upload_64
fi

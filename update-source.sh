#!/bin/sh
set -e
dropin=0

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

if [ "$dropin" ]; then
	if [ -x ./dropin ]; then
		dropin=./dropin
	elif [ -x ../dropin ]; then
		dropin=../dropin
	fi

	if [ "$upload_32" -o "$upload_64" ]; then
		echo "Uploading to dropin. ^C to abort"
		../dropin $upload_32 $upload_64
	fi
fi

specfile=chromium-browser-bin.spec
oldrev=$(awk '/^%define[ 	]+svnrev[ 	]+/{print $NF}' $specfile)
if [ "$oldrev" != "$rev" ]; then
	# revno => VERSION hint by Caleb Maclennan <caleb#alerque.com>
	wget -q -O VERSION.sh http://src.chromium.org/viewvc/chrome/trunk/src/chrome/VERSION?revision=$rev
	if grep -Ev '^(MAJOR|MINOR|BUILD|PATCH)=[0-9]+$' VERSION.sh >&2; then
		echo >&2 "I refuse to execute grabbed file for security concerns"
		exit 1
	fi
	. ./VERSION.sh
	version=$MAJOR.$MINOR.$BUILD.$PATCH

	echo "Updating $specfile for $version r$rev"
	sed -i -e "
		s/^\(%define[ \t]\+svnrev[ \t]\+\)[0-9]\+\$/\1$rev/
		s/^\(Version:[ \t]\+\)[.0-9]\+\$/\1$version/
	" $specfile
	../builder -ncs -5 $specfile
fi

#!/bin/sh
set -e
dropin=

if [ "$1" ]; then
	rev=$1
	echo "Using $rev..."
else
	echo "Fetching latest revno... "
	rev=$(wget -q -O - http://build.chromium.org/buildbot/continuous/linux/LATEST/REVISION)
	rev64=$(wget -q -O - http://build.chromium.org/buildbot/continuous/linux64/LATEST/REVISION)
	# be sure that we use same rev on both arch
	if [ "$rev" != "$rev64" ]; then
		echo "Current 32bit build ($rev) does not match 64bit build ($rev64)"
		echo "The upstream buildbot probably failed."
		if [ "$rev" -lt "$rev64" ]; then
			echo "Using latest 32bit revision..."
			rev64=$rev
		else
			echo "Using latest 64bit revision..."
			rev=$rev64
		fi
	fi
	echo "$rev"
	# TODO: use release branches instead of trunk. Current release can be looked up like this:
	#linuxdev=$(wget -q -O - http://omahaproxy.appspot.com | grep '^linux,dev' | cut -d, -f3)
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

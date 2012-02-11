#!/bin/sh
# Usage:
# ./update-source.sh [spec|rev]
#     Download latest binary tarball based on latest release from
#     buildbot, current version referenced in spec file, or custom
#     version number.
set -e
dropin=
specfile=chromium-browser-bin.spec

# Work in package dir
dir=$(dirname "$0")
cd "$dir"

if [ "$1" == "spec" ]; then
	rev=$(awk '/^%define.*svnrev/{print $NF}' $specfile)
	echo "Using $rev from spec file"
elif [ "$1" == "trunk" ]; then
	echo "Fetching latest revno... "
	rev=$(wget -q -O - http://commondatastorage.googleapis.com/chromium-browser-continuous/Linux/LAST_CHANGE)
	rev64=$(wget -q -O - http://commondatastorage.googleapis.com/chromium-browser-continuous/Linux_x64/LAST_CHANGE)
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
	echo "Using trunk $rev"
elif [ "$1" ]; then
	rev=$1
	echo "Using $rev..."
else
	contents=$(wget -q -O - "http://omahaproxy.appspot.com/?os=linux&channel=dev")
	rev=$(echo "$contents" | awk -F, '/^linux/{print $7}')
	version=$(echo "$contents" | awk -F, '/^linux/{print $3}')
	echo "Using devel channel $rev..."
fi

if [ ! -f chromium-browser32-r$rev.zip ]; then
	wget http://commondatastorage.googleapis.com/chromium-browser-continuous/Linux/$rev/chrome-linux.zip -c -O chromium-browser32-r$rev.zip

	upload_32="chromium-browser32-r$rev.zip"
fi
if [ ! -f chromium-browser64-r$rev.zip ]; then
	wget http://commondatastorage.googleapis.com/chromium-browser-continuous/Linux_x64/$rev/chrome-linux.zip -c -O chromium-browser64-r$rev.zip
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

oldrev=$(awk '/^%define[ 	]+svnrev[ 	]+/{print $NF}' $specfile)
if [ "$oldrev" != "$rev" ]; then
	if [ -z "$version" ]; then
		wget -q -O VERSION.sh http://src.chromium.org/viewvc/chrome/trunk/src/chrome/VERSION?revision=$rev
		echo REV=$rev >> VERSION.sh
		if grep -Ev '^(MAJOR|MINOR|BUILD|PATCH|REV)=[0-9]+$' VERSION.sh >&2; then
			echo >&2 "I refuse to execute garbled file due security concerns"
			exit 1
		fi
		. ./VERSION.sh
		version=$MAJOR.$MINOR.$BUILD.$PATCH
	fi

	echo "Updating $specfile for $version r$rev"
	sed -i -e "
		s/^\(%define[ \t]\+svnrev[ \t]\+\)[0-9]\+\$/\1$rev/
		s/^\(Version:[ \t]\+\)[.0-9]\+\$/\1$version/
	" $specfile
	../builder -ncs -5 $specfile
fi

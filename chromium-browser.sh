#!/bin/sh

# Copyright (c) 2006-2009 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

# Always use our ffmpeg libs.
# Also symlinks for nss/nspr libs can be found from our dir.
export LD_LIBRARY_PATH=@libdir@${LD_LIBRARY_PATH:+:"$LD_LIBRARY_PATH"}

# for to find xdg-settings
export PATH=@libdir@${PATH:+:"$PATH"}

# chromium needs /dev/shm being mounted
m=$(awk '$2 == "/dev/shm" && $3 == "tmpfs" {print}' /proc/mounts)
if [ -z "$m" ]; then
	cat >&2 <<-'EOF'
	Chromium needs /dev/shm being mounted for Shared Memory access.

	To do so, invoke (as root):
	mount -t tmpfs -o rw,nosuid,nodev,noexec none /dev/shm

	EOF
fi

# Set CHROME_VERSION_EXTRA visible in the About dialog and in about:version
export CHROME_VERSION_EXTRA="PLD Linux"

# Allow $CHROME_DESKTOP to override the built-in value, so that development
# versions can set themselves as the default without interfering with
# non-official, packaged versions using the built-in value.
# https://src.chromium.org/svn/trunk/src/chrome/browser/shell_integration_linux.cc
export CHROME_DESKTOP="chromium-browser-bin.desktop"

exec @libdir@/chromium-browser "$@"

#!/bin/sh

# Copyright (c) 2006-2009 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

# Always use our ffmpeg libs.
# Also symlinkes for nss/nspr libs can be found from our dir.
export LD_LIBRARY_PATH=/usr/lib64/chromium-browser-bin${LD_LIBRARY_PATH:+:"$LD_LIBRARY_PATH"}

# for to find xdg-settings
export PATH=/usr/lib64/chromium-browser-bin${PATH:+:"$PATH"}

exec /usr/lib64/chromium-browser-bin/chromium-browser "$@"

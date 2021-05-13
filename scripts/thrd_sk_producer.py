#! /usr/bin/env python

# prototype / test - for passing commands from Flask server to separate task / process
#
# processes vs threads
# https://stackoverflow.com/questions/3044580/multiprocessing-vs-threading-python
# threads will all run on one core under same GIL
# processes will run on separate cores, are killable
#
#
# difference between threading & multiprocessing MODULES
# https://stackoverflow.com/questions/18114285/what-are-the-differences-between-the-threading-and-multiprocessing-modules

# Example w/ threads
# https://www.geeksforgeeks.org/socket-programming-multi-threading-python/



# VLC remote through http
# https://www.howtogeek.com/117261/how-to-activate-vlcs-web-interface-control-vlc-from-a-browser-use-any-smartphone-as-a-remote/
# Preferences > Interface > Check: Enable HTTP Web interface
# Preferences > Interface > Set Password (optional)
#
# make sure there's a .hosts file present in
# /Applications/VLC.app/Contents/MacOS/share/lua/http
# otherwise won't serve
#
# Open browser: http://localhost:8080/
# if PWD leave user blank
# you now have remote control of VLC through browser.
#
# Where's this interface documented?
# https://wiki.videolan.org/VLC_HTTP_requests/
# and here
# /Applications/VLC.app/Contents/MacOS/share/lua/http/requests/README.txt
# accessing via pyton
# https://gist.github.com/shubhamjain/9809108
# saved to /moviepicker/vlc_http.py

# producing a 'random' numbers that fit a distribution curve
from random import choice
pool = [1.5, 2, 2.0, 3, 3.0, 3.5, 4, 4.0, 4.5]
for i in range(500):
    for n in range(6):
        s = [choice(pool) for i in range(n)]

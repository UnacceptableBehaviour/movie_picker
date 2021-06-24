#! /usr/bin/env python

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# prototyping tests
#
# subprocess
#
# Notes & examples: https://janakiev.com/blog/python-shell-commands/
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
from pprint import pprint
import re
import sys
from pathlib import Path
from time import sleep
import subprocess

# output from
#
# > ping -c 4 python.org
# PING python.org (138.197.63.241) 56(84) bytes of data.
# 64 bytes from 138.197.63.241 (138.197.63.241): icmp_seq=1 ttl=52 time=85.1 ms
# 64 bytes from 138.197.63.241 (138.197.63.241): icmp_seq=2 ttl=52 time=86.7 ms
# 64 bytes from 138.197.63.241 (138.197.63.241): icmp_seq=3 ttl=52 time=83.4 ms
# 64 bytes from 138.197.63.241 (138.197.63.241): icmp_seq=4 ttl=52 time=83.2 ms
#
# --- python.org ping statistics ---
# 4 packets transmitted, 4 received, 0% packet loss, time 7ms
# rtt min/avg/max/mdev = 83.238/84.612/86.742/1.431 ms


# output from this script
#
# > ./scripts/subprocess_test.py
# PING python.org (138.197.63.241) 56(84) bytes of data.
# 64 bytes from 138.197.63.241 (138.197.63.241): icmp_seq=1 ttl=52 time=84.3 ms
# 64 bytes from 138.197.63.241 (138.197.63.241): icmp_seq=2 ttl=52 time=83.5 ms
# 64 bytes from 138.197.63.241 (138.197.63.241): icmp_seq=3 ttl=52 time=83.3 ms
# 64 bytes from 138.197.63.241 (138.197.63.241): icmp_seq=4 ttl=52 time=83.8 ms
#
# --- python.org ping statistics ---
# 4 packets transmitted, 4 received, 0% packet loss, time 8ms
# rtt min/avg/max/mdev = 83.279/83.724/84.343/0.533 ms
#
# RETURN CODE 0

# process = subprocess.Popen(['ping', '-c 4', 'python.org'],   #
#                            stdout=subprocess.PIPE,
#                            universal_newlines=True)
# while True:
#     output = process.stdout.readline()
#     print(output.strip())
#     # Do something else
#     return_code = process.poll()
#     if return_code is not None:
#         print('RETURN CODE', return_code)
#         # Process has finished, read rest of the output
#         for output in process.stdout.readlines():
#             print(output.strip())
#         break

# rund media in a vlc window
# > vlc '/media/pi/time_box_2018/movies/_vlc_test/test_mv_mp4.mp4' --extraintf http
#
# VLC media player 3.0.12 Vetinari (revision 1.0.6-1618-g917488b78)
# [004f4e40] [http] lua interface: Lua HTTP interface
# [0046cb58] main libvlc: Running vlc with the default interface. Use 'cvlc' to use vlc without interface.
# libEGL warning: DRI2: failed to authenticate
# [4fcdd968] mmal_codec decoder: VCSM init succeeded: Legacy
# libEGL warning: DRI2: failed to authenticate
# [6260ce08] mmal_xsplitter vout display error: Failed to open Xsplitter:opengles2 module

cmd = ["vlc" "'/media/pi/time_box_2018/movies/_vlc_test/test_mv_mp4.mp4'"]
# FileNotFoundError: [Errno 2] No such file or directory: "vlc '/media/pi/time_box_2018/movies/_vlc_test/test_mv_mp4.mp4'": "vlc '/media/pi/time_box_2018/movies/_vlc_test/test_mv_mp4.mp4'"

# missing comma from list! doh
cmd = ["vlc", "'/media/pi/time_box_2018/movies/_vlc_test/test_mv_mp4.mp4'"]
# > ./scripts/subprocess_test.py
# VLC media player 3.0.12 Vetinari (revision 1.0.6-1618-g917488b78)
# [006e9e10] [http] lua interface: Lua HTTP interface
# [00661b58] main libvlc: Running vlc with the default interface. Use 'cvlc' to use vlc without interface.
# libEGL warning: DRI2: failed to authenticate
# [62500c10] filesystem stream error: cannot open file /home/pi/repos/mp_lnx/movie_picker/'/media/pi/time_box_2018/movies/_vlc_test/test_mv_mp4.mp4' (No such file or directory)

# dont need the extra inverted commas
cmd = ['vlc', '/media/pi/time_box_2018/movies/_vlc_test/test_mv_mp4.mp4'] # WORKS - FIREs UP media in vcl window!
# $ ./scripts/subprocess_test.py
# VLC media player 3.0.12 Vetinari (revision 1.0.6-1618-g917488b78)
# (venv) pi@rpi-C1:~/repos/mp_lnx/movie_picker $ [01f9fe90] [http] lua interface: Lua HTTP interface
# [01f17b58] main libvlc: Running vlc with the default interface. Use 'cvlc' to use vlc without interface.
# libEGL warning: DRI2: failed to authenticate
# [4fae0708] mmal_codec decoder: VCSM init succeeded: Legacy
# [4fae0708] main decoder error: buffer deadlock prevented
# libEGL warning: DRI2: failed to authenticate
# [61109560] mmal_xsplitter vout display error: Failed to open Xsplitter:opengles2 module

cmd = ['vlc', '/media/pi/time_box_2018/movies/_vlc_test/test_mv_mp4.mp4', '--extraintf http']
# $ ./scripts/subprocess_test.py
# VLC media player 3.0.12 Vetinari (revision 1.0.6-1618-g917488b78)
# vlc: unknown option or missing mandatory argument `--extraintf http'
# Try `vlc --help' for more information.

cmd = ['vlc', '/media/pi/time_box_2018/movies/_vlc_test/test_mv_mp4.mp4', '--extraintf', 'http']
# work too - explicit LUA http interface enable
# $ [01feaf80] [http] lua interface: Lua HTTP interface
# [01f62b58] main libvlc: Running vlc with the default interface. Use 'cvlc' to use vlc without interface.
# libEGL warning: DRI2: failed to authenticate
# [4f9dfa80] mmal_codec decoder: VCSM init succeeded: Legacy
# libEGL warning: DRI2: failed to authenticate
# [62706758] mmal_xsplitter vout display error: Failed to open Xsplitter:opengles2 module
# QObject::~QObject: Timers cannot be stopped from another thread

cmd = ['vlc', '-f', '/media/pi/time_box_2018/movies/_vlc_test/test_mv_mp4.mp4', '--extraintf', 'http']
vlc_process = subprocess.Popen(cmd)




#! /usr/bin/env python

# compare two MMdia paths for duplicates - EG multiple external discs or room remotes

# from pathlib import Path
# from collections import Counter
from pprint import pprint
# import re
from pathlib import Path

import vlc

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# helpers
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

PATH_TO_MKV = Path('/Volumes/Osx4T/tor/_vlc_test/test_mv_mkv.mkv')
PATH_TO_AVI = Path('/Volumes/Osx4T/tor/_vlc_test/test_mv_avi.avi')
PATH_TO_MP4 = Path('/Volumes/Osx4T/tor/_vlc_test/test_mv_mp4.mp4')
PATH_TO_MP3 = Path('/Volumes/Osx4T/tor/_vlc_test/test_mv_mp3.mp3')

def main():
    pass


if __name__ == '__main__':
    from time import sleep


    #media_file = PATH_TO_MKV                # No drawable-nsobject found! - sound works
    media_file = PATH_TO_AVI                #  No drawable-nsobject found! - sound works
    media_file = PATH_TO_MP4                # looks like needs ns_o
    media_file = PATH_TO_MP3                # works fine

    if media_file.exists():                 # path exists
        print(f"FOUND {media_file}")
        mp = vlc.MediaPlayer(media_file)
        print(type(mp))                     # <class 'vlc.MediaPlayer'>
        mp.play()
        while True: # mp.is_playing():
             sleep(1)
    else:
        print(f"FILE NOT FOUND {media_file}")


# Problems & Solutions
# Basically need a display framework/
# https://python-guide-kr.readthedocs.io/ko/latest/scenarios/gui.html
# Shortlist of most cross platform that aren't depracated
# remember target for this is a rpi plugged into a TV!
# Tk
# Qt
# Toga sounds interesting - but not for this



# 1Q. Nothing happens - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Codes exits before vlc has time to play clip
# Add infinite while for test
# mp.play()
# while True:
#     sleep(1)
#
# 2Q. Appears vlc-player doesn't create it's own output window  - - - - - - - - - - - - - - - - - -
# [00007f8c07c879b0] videotoolbox decoder: Using Video Toolbox to decode 'h264'
# [00007f8c07c879b0] videotoolbox decoder: vt cvpx chroma: 420v
#
# [00007f8c07fa88f0] macosx vout display error: No drawable-nsobject nor vout_window_t found, passing over.
# [00007f8c0988faf0] main video output error: video output creation failed
# [00007f8c07c879b0] main decoder error: failed to create video output
# [00007f8c07c879b0] videotoolbox decoder error: decoder failure, Abort.
#
# 2Ai. https://stackoverflow.com/questions/18308384/vlc-mac-python-binding-no-video-output
# Post 9yo - Qt upgardes broken solution - NOT TESTED
# create a window in macosx (using either the native cocoa API or a widget lib like Qt), and pass its reference through the set_nsobject() method
#
# 2Aii. https://www.gitmemory.com/issue/oaubert/python-vlc/91/514010015
# Thank you. That all looks OK. The segmentation fault is due tkvlc.py not passing the correct object to player.set_nsobject() for recent macOS versions. It is unclear at this very moment whether tkvlc.py can be corrected.
# INVESTIGATE THIS - TODO - its seems messy from making installable point of view and it won't run on linux
# Try to install PyCocoa with pip install pycocoa. Also, get a copy of the cocoavlc.py from GitHub and save that in your current directory. Then, run python cocoavlc.py and select a video from the dialog window. Or run python cocoavlc.py <video_file_name>.
# cocoavlc.py here
# https://git.videolan.org/?p=vlc/bindings/python.git;a=tree;f=examples;hb=HEAD
#
# 3Q. Cannot find set_nsobject() or interface for that matter . . .  - - - - - - - - - - - - - - -
# Where is the python-vlc code? venv python_vlc just has distribution info
# file:///Users/simon/a_syllabus/lang/python/repos/movie_picker/venv/lib/python3.7/site-packages/python_vlc-3.0.11115.dist-info
#
# 3A. import vlc interface HERE:
# vlc.py outside folder
# /movie_picker/venv/lib/python3.7/site-packages/vlc.py
# Docs location at begining - https://www.olivieraubert.net/vlc/python-ctypes/
# has runnable example starting at if __name__ == '__main__' see below (line 8543 !)
#
# From https://wiki.videolan.org/Python_bindings
# The vlc.py file also contains a runnable example player application (see code at the end of the file, starting from the line if __name__ == '__main__').
# A set of helper examples examples provide a pyGtk, a pyQt and a pyWx player to ease integration.
# TODO - run example
# python -m vlc '/Volumes/Osx4T/tor/_vlc_test/test_mv_mkv.mkv'
# Fails: AttributeError: type object 'Position' has no attribute 'Bottom'
# Comment out that line and runs (had to kill 2936 to stop it!)
# Fails w/ same issui
# [00007fcbe19161b0] macosx vout display error: No drawable-nsobject nor vout_window_t found, passing over.
# [00007fcbdf0b20f0] main video output error: video output creation failed
# [00007fcbde6ca4d0] main decoder error: failed to create video output


# Search for
# Example code (from vlc.py - https://www.olivieraubert.net/vlc/python-ctypes/)
# Docs API: https://www.olivieraubert.net/vlc/python-ctypes/doc/index.html
# Go through these, theres Qt, Tjk
# https://git.videolan.org/?p=vlc/bindings/python.git;a=tree;f=examples;hb=HEAD

# start w/ pyqt5vlc.py

# Ubuntu VM pass - prozium?

# Geeks for geeks - different setup route
# https://www.geeksforgeeks.org/vlc-module-in-python-an-introduction/

# * * * * * * * FAILURE MODE * * * * * * * *
# .MKV / .AVI / .MP4  all fail same way need a drawable object
# [00007fdd5771f1f0] caopengllayer vout display error: No drawable-nsobject found!
# [00007fdd5771f1f0] macosx vout display error: No drawable-nsobject nor vout_window_t found, passing over.
# [00007fdd598082f0] main video output error: video output creation failed
# [00007fdd59225980] main decoder error: failed to create video output
# [h264 @ 0x7fdd57bb1200] get_buffer() failed
# [h264 @ 0x7fdd57bb1200] thread_get_buffer() failed
# [h264 @ 0x7fdd57bb1200] decode_slice_header error
# [h264 @ 0x7fdd57bb1200] no frame!
# * * * * * * * FAILURE MODE * * * * * * * *




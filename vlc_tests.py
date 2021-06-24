#! /usr/bin/env python

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# prototyping tests
#   how to run control vlc from flask (manage & communicate w/ vlc process)
#
# options investigated - see Select approach to test
#
#   python-vlc  - python binding to vlc - NO work solo! :/
#               - requires a windows framework - working EG examples_pyqt5vlc.py using Qt5
#
#   python_vlc_http - Http Inteface package
#               - couple of bugs so creted an internal module
#               - PULL request submitted
#
#   internal package - using vlc http interface
#               - from moviepicker import vlc_http
#
#   Qt5 example - using python-vlc fires up a samll Qt5 app - examples_pyqt5vlc.py
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# compare two MMdia paths for duplicates - EG multiple external discs or room remotes

# from pathlib import Path
# from collections import Counter
from pprint import pprint
import re
import sys
from pathlib import Path

import vlc

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# helpers
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
import platform
running_os = platform.system()
# AIX: 'aix', Linux:'Linux', Windows: 'win32', Windows/Cygwin: 'ygwin', macOS: 'Darwin'

if running_os == 'Darwin':  # local - osx box
    PATH_TO_MKV = Path('/Volumes/Osx4T/tor/_vlc_test/test_mv_mkv.mkv')
    PATH_TO_AVI = Path('/Volumes/Osx4T/tor/_vlc_test/test_mv_avi.avi')
    PATH_TO_MP4 = Path('/Volumes/Osx4T/tor/_vlc_test/test_mv_mp4.mp4')
    PATH_TO_MP3 = Path('/Volumes/Osx4T/tor/_vlc_test/test_mv_mp3.mp3')
elif running_os == 'Linux':
    PATH_TO_MKV = Path('/media/pi/time_box_2018/movies/_vlc_test/test_mv_mkv.mkv')
    PATH_TO_AVI = Path('/media/pi/time_box_2018/movies/_vlc_test/test_mv_avi.avi')
    PATH_TO_MP4 = Path('/media/pi/time_box_2018/movies/_vlc_test/test_mv_mp4.mp4')
    PATH_TO_MP3 = Path('/media/pi/time_box_2018/movies/_vlc_test/test_mv_mp3.mp3')


def vlc_module(media_file=None):
    # attempt 1 - using plain old vlc module
    if media_file.exists():                 # path exists
        print(f"FOUND {media_file}")
        mp = vlc.MediaPlayer(media_file)
        print(type(mp))                     # <class 'vlc.MediaPlayer'>
        mp.play()               # *** this wont work w/o a drawing context - see examples_pyqt5vlc.py ***
        while True: # mp.is_playing():
             sleep(1)
             # ctrl-C to exit   < < < <
    else:
        print(f"FILE NOT FOUND {media_file}")

import psutil
# make these two functions DRY
def kill_running_vlc():
    # is vlc running yet?  for this # pip install psutil
    # https://thispointer.com/python-get-list-of-all-running-processes-and-sort-by-highest-memory-usage/
    targets = []
    for proc in psutil.process_iter():
        try:
            processName = proc.name()   # get name & id
            processID = proc.pid
            if 'vlc' in processName.lower():
                targets.append(proc)
                print(processName , ' :!: ', processID)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    print(len(targets))
    for p in targets:
        print(f"kill_running_vlc: {p.name()} \t {p.pid} \t {p.create_time}")
        p.kill()

def vlc_is_running():  # is vlc running yet?
    targets = []
    for proc in psutil.process_iter():
        try:
            processName = proc.name()   # get name & id
            processID = proc.pid
            if 'vlc' in processName.lower():
                targets.append(proc)
                print(processName , ' :?: ', processID)
                return True

        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    return False


INSTRUCTION_WAIT = 1
def python_vlc_http_package(media_file=None):
    from python_vlc_http import HttpVLC

    # make sure only single version of vlc running
    kill_running_vlc()

    # start VLC
    # https://wiki.videolan.org/Documentation:Advanced_Use_of_VLC/
    # osx fullscreen
    #movie_process = subprocess.Popen(f"exec /Applications/VLC.app/Contents/MacOS/VLC -f '{media_file}' --extraintf http", shell=True)
    # osx window
    #movie_process = subprocess.Popen(f"exec /Applications/VLC.app/Contents/MacOS/VLC    '{media_file}' --extraintf http", shell=True)

    # on linux window
    # see line 299
    # movie_process = subprocess.Popen(f"vlc '{media_file}' --extraintf http")


    # wait for http interface to come live
    sleep(0.2)
    # connect to VLC
    vlc_client = HttpVLC('http://localhost:8080', '', 'p1')

    # vol 10 % 0-1
    sleep(INSTRUCTION_WAIT)
    print(f"vol: 10")
    vlc_client.set_volume(0.1)

    # vol 90 %
    sleep(INSTRUCTION_WAIT)
    print(f"vol: 90")
    vlc_client.set_volume(0.9)

    # vol 50 %
    sleep(INSTRUCTION_WAIT)
    print(f"vol: 50")
    vlc_client.set_volume(0.5)

    # pause
    sleep(INSTRUCTION_WAIT)
    print(f"vlc: pause")
    vlc_client.pause()

    print(f"VOL:   {vlc_client.volume()}/320")
    print(f"TITLE: {vlc_client.title()}")
    print(f"FILE:  {vlc_client.filename()}")
    print(f"RATE:  {vlc_client.rate()}")
    print(f"FULLSC:{vlc_client.is_fullscreen()}")
    media_length = int(vlc_client.media_length())
    m, s = divmod(media_length, 60)     # / 60 ret div & mod into m, s
    h, m = divmod(m, 60)
    print(f"LEN:   {media_length} - {h}h{m}m")
    pos = vlc_client.position()
    pos_secs = int(media_length * float(pos))
    m, s = divmod(pos_secs, 60)     # / 60 ret div & mod into m, s
    h, m = divmod(m, 60)
    print(f"POS:   {pos} - {h}h{m}m")

    # play
    sleep(INSTRUCTION_WAIT)
    print(f"vlc: play")
    vlc_client.play()

    # ff
    sleep(INSTRUCTION_WAIT)
    print(f"vlc: {vlc_client.rate()}")
    print(f"vlc: FF x2")
    vlc_client.set_rate(2.0)

    # ff
    sleep(INSTRUCTION_WAIT)
    print(f"vlc: {vlc_client.rate()}")
    print(f"vlc: FF x2.5")
    vlc_client.set_rate(2.5)

    # ff
    sleep(INSTRUCTION_WAIT)
    print(f"vlc: {vlc_client.rate()}")
    print(f"vlc: FF x3")
    vlc_client.set_rate(3.0)

    # ff
    sleep(INSTRUCTION_WAIT)
    print(f"vlc: {vlc_client.rate()}")
    print(f"vlc: FF x3.5")
    vlc_client.set_rate(3.5)

    # toggle fullscreen
    sleep(INSTRUCTION_WAIT)
    print(f"vlc: fusllscreen? {vlc_client.is_fullscreen()}")
    vlc_client.toggle_fullscreen()
    sleep(INSTRUCTION_WAIT)
    print(f"vlc: fusllscreen? {vlc_client.is_fullscreen()}")
    vlc_client.toggle_fullscreen()


    vlc_client.set_rate(1)
    # +30sec
    for i in range(10):
        sleep(3)
        pos = vlc_client.position()
        pos_secs = int(media_length * float(pos))
        print(f"vlc: +30 sec")
        vlc_client.seek(pos_secs+200)    #see examples but relative: +secs -sec, absolute: no_of_sec

    for i in range(10):
        sleep(3)
        pos = vlc_client.position()
        pos_secs = int(media_length * float(pos))
        print(f"vlc: -30 sec")
        vlc_client.seek(pos_secs-30)    #see examples but relative: +secs -sec, absolute: no_of_sec

    # NOT WORKING:
    # SEEK
    # SET_RATE

    # open browser while vlc playing
    # enter in address bar:
    # http://127.0.0.1:8080/requests/status.xml?command=pl_stop
    # http interface commands in
    # /Applications/VLC.app/Contents/MacOS/share/lua/http/requests/README.txt

    # SET_RATE - following WORKS
    # ?command=rate&val=1.5
    # http://127.0.0.1:8080/requests/status.xml?command=rate&val=1.5
    # set_rate FIXED missing &val=

    # SEEK ?command=seek&val=<val>  ALSO FIXED
    # examples:
    # 1000 -> seek to the 1000th second
    # +1H:2M -> seek 1 hour and 2 minutes forward
    # -10% -> seek 10% back
    # http://127.0.0.1:8080/requests/status.xml?command=seek&val=10%    NO work!
    # +30s
    # http://127.0.0.1:8080/requests/status.xml?command=seek&val=+30S   works
    # -30s
    # http://127.0.0.1:8080/requests/status.xml?command=seek&val=-30S   works
    # got 1000s
    # http://127.0.0.1:8080/requests/status.xml?command=seek&val=1000   works - bit slow but works

    # COMMENT ABOUT moving to MRL
    # https://en.wikipedia.org/wiki/Media_resource_locator

    # rate report
    while True:
        print(f"vlc: get rate: {vlc_client.rate()}")
        media_length = int(vlc_client.media_length())
        m, s = divmod(media_length, 60)     # / 60 ret div & mod into m, s
        h, m = divmod(m, 60)
        print(f"LEN:   {media_length} - {h}h{m}m")
        pos = vlc_client.position()
        pos_secs = int(media_length * float(pos))
        m, s = divmod(pos_secs, 60)     # / 60 ret div & mod into m, s
        h, m = divmod(m, 60)
        print(f"POS:   {pos} - {h}h{m}m")
        sleep(INSTRUCTION_WAIT)



def vlc_http_py_moviepicker(media_file=None):
    global running_os
    #https://stackoverflow.com/questions/16981921/relative-imports-in-python-3

    #from .moviepicker.vlc_http import vlc_http
    # /Users/simon/a_syllabus/lang/python/movie_picker
    # from ./scripts/vlc_tests.py                   # ImportError: attempted relative import with no known parent package
    # move file
    # /Users/simon/a_syllabus/lang/python/movie_picker
    # from ./vlc_tests.py                           # ImportError: attempted relative import with no known parent package

    #from moviepicker.vlc_http import vlc_http       # works
    # /Users/simon/a_syllabus/lang/python/movie_picker
    # from ./vlc_tests.py                           # ImportError: attempted relative import with no known parent package

    from moviepicker import vlc_http    # works from same dir as moviepicker

    # make sure only single version of vlc running
    kill_running_vlc()

    print(f"vlc_http_py_moviepicker: LOADING {media_file}")
    # start VLC
    # https://wiki.videolan.org/Documentation:Advanced_Use_of_VLC/

    print(f"OS: {running_os}")

    if running_os == 'Darwin':  # local - osx box
        # fullscreen
        #movie_process = subprocess.Popen(f"exec /Applications/VLC.app/Contents/MacOS/VLC -f '{media_file}' --extraintf http", shell=True)
        # window
        movie_process = subprocess.Popen(f"exec /Applications/VLC.app/Contents/MacOS/VLC    '{media_file}' --extraintf http", shell=True)

    elif running_os == 'Linux':
        # on linux window
        #movie_process = subprocess.Popen((f"vlc '{media_file}' --extraintf http").split(), shell=True)
        cmd = ['vlc', media_file,'--extraintf','http'] #
        print(f"Command list: {cmd}")
        print(" - - - starting vlc - - - ")
        #movie_process = subprocess.Popen(cmd, shell=True)
        movie_process = subprocess.Popen(cmd)
        print(" - - - starting vlc started ? - - - ")

    sleep(0.2)
    vlc_http_channel = vlc_http(user='', pwd='p1')

    print(f"vlc_http_channel: {type(vlc_http_channel)}")

    sleep(1)
    print(f"vlc_http_channel: toggle fullscreen - currently fullscree = {vlc_http_channel.is_fullscreen()}")
    vlc_http_channel.toggle_fullscreen()
    sleep(2)
    print(f"vlc_http_channel: toggle fullscreen - currently fullscree = {vlc_http_channel.is_fullscreen()}")
    vlc_http_channel.toggle_fullscreen()

    # +400sec
    # print(f"vlc_http_channel: +400sec")
    # vlc_http_channel.seek(400)
    # sleep(1)

    # pause
    print(f"vlc_http_channel: pause")
    vlc_http_channel.pause()
    sleep(1)

    print(f"vlc_http_channel: VOL:0")
    vlc_http_channel.set_volume(0)
    sleep(1)
    print(f"vlc_http_channel: VOL:100")
    vlc_http_channel.set_volume(100)
    sleep(1)
    print(f"vlc_http_channel: VOL:50")
    vlc_http_channel.set_volume(50)
    sleep(1)

    # play
    print(f"vlc_http_channel: play")
    vlc_http_channel.play()
    sleep(1)

    # # -20sec
    # for i in range(6):
    #     sleep(1)
    #     print(f"vlc_http_channel: -20sec")
    #     #vlc_http_channel.seek(-20)
    #     vlc_http_channel.seek(+20)

    # seek to

    # # ff
    # sleep(INSTRUCTION_WAIT)
    # #print(f"vlc: {vlc_http_channel.rate()}")
    # print(f"vlc: FF x2")
    # vlc_http_channel.set_rate(2.0)
    #
    # # ff
    # sleep(INSTRUCTION_WAIT)
    # #print(f"vlc: {vlc_http_channel.rate()}")
    # print(f"vlc: FF x2.5")
    # vlc_http_channel.set_rate(2.5)
    #
    # # ff
    # sleep(INSTRUCTION_WAIT)
    # #print(f"vlc: {vlc_http_channel.rate()}")
    # print(f"vlc: FF x3")
    # vlc_http_channel.set_rate(3.0)
    #
    # # ff
    # sleep(INSTRUCTION_WAIT)
    # #print(f"vlc: {vlc_http_channel.rate()}")
    # print(f"vlc: FF x3.5")
    # vlc_http_channel.set_rate(3.5)


    # sleep(2)
    # print(f"vlc_http_channel: toggle playback")
    # vlc_http_channel.play_pause()
    # sleep(1)
    #
    # print(f"vlc_http_channel: toggle playback")
    # vlc_http_channel.play_pause()

    sleep(2)
    print(f"vlc_http_channel: get_attributes . . .")
    vlc_state = vlc_http_channel.get_attributes()
    pprint(vlc_state)

    # find volume range as define by vlc attributes
    # while True:
    #     vlc_state = vlc_http_channel.get_attributes()
    #     print(f"vlc_state['volume']: {vlc_state['volume']}")    # 0-320
    #     sleep(1)

    print(f"vlc_http_channel: playback normal - goto 52m 1440secs")
    vlc_http_channel.set_rate(1)
    vlc_http_channel.seek(1440, vlc_http.SEEK_BEGIN) # absolute seek (from beginning)
    sleep(2)
    vlc_http_channel.seek_from_start(2880) # absolute seek (from beginning)
    sleep(2)
    # ff x2 x3 x4
    # seek - position of vol bar
    # goto start
    # goto end

    # rr x2 x3 x4 - periodic -Ns -4sec/sec, -3sec/sec, -2sec/sec - double up /2sec see what works

    print(f"vlc_http_channel: simulate REWIND x4")
    # rr x4
    # works but not a convincing rewind - not obvious its rewinind - big jumps
    # for i in range(20):
    #     sleep(1)
    #     print(f"vlc_http_channel: rr x4")
    #     vlc_http_channel.seek(-30)
    # better but still plays forward for the fraction of time it's playing - odd visual cues
    # this would also be blocking from flask
    for i in range(100):
        sleep(0.1)
        print(f"vlc_http_channel: rr x4")
        vlc_http_channel.seek(-3)


    sleep(2)
    print(f"vlc_http_channel: EXIT")




JUST_VLC_MODULE_SND     = 10
JUST_VLC_MODULE_VID     = 15
PYTHON_VLC_HTTP_PACKAGE = 20
MOVIEPICKER_VLC_HTTP_PY = 30
QT5_APP                 = 40

if __name__ == '__main__':
    from time import sleep
    import subprocess
    # movie_process = subprocess.Popen(f"exec /Applications/VLC.app/Contents/MacOS/VLC -f '{PATH_TO_FILE}' --extraintf http", shell=True)
    # -f = fullscreen
    # --extraintf http = start w/ extra http interface running

    #media_file = PATH_TO_MKV
    media_file = PATH_TO_AVI
    media_file = PATH_TO_MP4
    #media_file = PATH_TO_MP3 # works fine

    # Select approach to test - - - - - - - - comment in!
    #code_base = JUST_VLC_MODULE_SND            # WORKS
    #code_base = JUST_VLC_MODULE_VID            # NO work - requires a canvas to work - see QT5_APP
    #code_base = PYTHON_VLC_HTTP_PACKAGE        # WORKING - couple of patches - enough for full remote - PULL requst commited
    code_base = MOVIEPICKER_VLC_HTTP_PY
    #code_base = QT5_APP

    if code_base == JUST_VLC_MODULE_SND:
        print("running codebase: JUST_VLC_MODULE_SND")
        vlc_module(PATH_TO_MP3)
        # Works fine
        sys.exit(0)

    if code_base == JUST_VLC_MODULE_VID:
        print("running codebase: JUST_VLC_MODULE_VID")
        vlc_module(media_file)
        # TODO -
        # No drawable-nsobject found!
        # Needs to be passed a canvas/screen by the OS
        sys.exit(0)

    # find running VLC tasks

    if code_base == PYTHON_VLC_HTTP_PACKAGE:
        print("running codebase: PYTHON_VLC_HTTP_PACKAGE")
        python_vlc_http_package(media_file)
        # Works fine
        sys.exit(0)

    if code_base == MOVIEPICKER_VLC_HTTP_PY:
        print("running codebase: MOVIEPICKER_VLC_HTTP_PY")
        vlc_http_py_moviepicker(media_file)
        sys.exit(0)

    if code_base == QT5_APP:
        subprocess.Popen(f"exec python ./scripts/examples_pyqt5vlc.py", shell=True)
        print("running codebase: QT5_APP")
        print("vlc_tests.py:  - - BUG: need to resize window so it display corectly")
        print("EXITING: vlc_tests.py")
        # TODO
        # pass resize/any msg to Qt5 app - emulate button press - hooks?
        # get this working w/ sockets maybe?
        # no good as it is.
        sys.exit(0)




# Problems & Solutions
# Basically need a display framework/ - OR start VLC as separate task!!
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

# EG dictionary from vlc_http.get_attributes()
# vlc_state =
# {'apiversion': '3',
#  'aspectratio': 'default',
#  'audiodelay': '0',
#  'audiofilters': {'filter_0': None},
#  'currentplid': '3',
#  'equalizer': None,
#  'fullscreen': 'false',
#  'information': {'Stream 0': {'Buffer dimensions': '1280x544',
#                               'Chroma location': 'Left',
#                               'Codec': 'H264 - MPEG-4 AVC (part 10) (avc1)',
#                               'Decoded format': None,
#                               'Frame rate': '23.976024',
#                               'Orientation': 'Top left',
#                               'Type': 'Video',
#                               'Video resolution': '1280x534'},
#                  'Stream 1': {'Bits per sample': '32',
#                               'Channels': 'Stereo',
#                               'Codec': 'MPEG AAC Audio (mp4a)',
#                               'Sample rate': '48000 Hz',
#                               'Type': 'Audio'},
#                  'meta': {'encoded_by': 'Lavf58.38.100',
#                           'filename': 'test_mv_mp4.mp4'}},
#  'length': '5592',
#  'loop': 'false',
#  'position': '0.00087705912301317',
#  'random': 'false',
#  'rate': '1',
#  'repeat': 'false',
#  'state': 'playing',
#  'stats': {'averagedemuxbitrate': '0',
#            'averageinputbitrate': '0',
#            'decodedaudio': '565',
#            'decodedvideo': '246',
#            'demuxbitrate': '0.28111588954926',
#            'demuxcorrupted': '0',
#            'demuxdiscontinuity': '2',
#            'demuxreadbytes': '1840469',
#            'demuxreadpackets': '0',
#            'displayedpictures': '174',
#            'inputbitrate': '0.21985921263695',
#            'lostabuffers': '0',
#            'lostpictures': '0',
#            'playedabuffers': '282',
#            'readbytes': '6679279',
#            'readpackets': '596',
#            'sendbitrate': '0',
#            'sentbytes': '0',
#            'sentpackets': '0'},
#  'subtitledelay': '0',
#  'time': '4',
#  'version': '3.0.12 Vetinari',
#  'videoeffects': {'brightness': '1',
#                   'contrast': '1',
#                   'gamma': '1',
#                   'hue': '0',
#                   'saturation': '1'},
#  'volume': '160'}

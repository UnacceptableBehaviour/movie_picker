"""Module to use VLC HTTP interface

@author Simon Fernandez

@license MIT License
adapted from from: https://gist.github.com/shubhamjain/9809108
by Shubham Jain <shubham.jain.1@gmail.com>

VLC provides an HTTP interface (by default disabled) at 127.0.0.1:8080.
I have written some basic functions to work on the interface.

Example:

vlc_http_channel = vlc_http(user='', pwd='p1')      # user is blank, pwd is set in vlc
                                                    #   preferences > Interface > Enable HTTP web interface > password
vlc_http_channel.is_fullscreen()                    # check screen state
vlc_http_channel.toggle_fullscreen()                # toggle fullscreen
vlc_http_channel.set_volume(50)                     # set volume 0-100
vlc_http_channel.play()                             # play if not playing - else nothing
vlc_http_channel.pause()                            # pause if not paused - else nothing
vlc_http_channel.set_rate(2.5)                      # set playback speed must be > 0 up to 4
vlc_http_channel.seek(-30)                          # back 30 sec from current position
vlc_http_channel.seek_from_start(2880)              # absolute seek (goto 2880 sec (48 min) from beginning)
vlc_http_channel.seek(2880, vlc_http.SEEK_BEGIN)    # same as seek_from_start < alias
vlc_http_channel.play_pause()                       # toggle play/pause
vlc_state = vlc_http_channel.get_attributes()       # get vlc / media attributes - see comment at bottom for EG
"""

import requests
import urllib
import xml.etree.ElementTree as ET
import os
from time import sleep

from pprint import pprint

# import psutil
# make these two function DRY and integrat into class
# def kill_running_vlc():
#     # is vlc running yet?  for this # pip install psutil
#
#     targets = []
#     for proc in psutil.process_iter():
#         try:
#             processName = proc.name()   # get name & id
#             processID = proc.pid
#             if 'vlc' in processName.lower():
#                 targets.append(proc)
#                 print(processName , ' ::: ', processID)
#         except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
#             pass
#
#     print(len(targets))
#     for p in targets:
#         print(f"kill_running_vlc: {p.name()} \t {p.pid} \t {p.create_time}")
#         p.kill()

# def vlc_is_running():  # is vlc running yet?
#     targets = []
#     for proc in psutil.process_iter():
#         try:
#             processName = proc.name()   # get name & id
#             processID = proc.pid
#             if 'vlc' in processName.lower():
#                 targets.append(proc)
#                 print(processName , ' ::: ', processID)
#                 return True
#
#         except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
#             pass
#
#     return False


class ConnectionProblem(Exception):
    """ There was a problem connecting with VLC localhost control.
        Make sure that VLC is running and port address is correct. """
    pass

class PlaybackRateError(Exception):
    """ Playback rate cannot be NEGATIVE """
    pass

class MediaNotLoaded(Exception):
    """ There must be active media for this to work """
    pass

from requests.exceptions import ConnectionError


class vlc_http:

    SEEK_CUR = 1        # seek from current position
    SEEK_BEGIN = 2      # seek from beginning (absolute val in seconds)

    port = 8080             # port on which player interface exists
    sec_percentage = 0      # what percentage of the media each second represents 100 / media length in seconds
    media_is_loaded = False #

    def __init__(self, user, pwd, port=8080):
        self.port = port
        self.user = user
        self.pwd = pwd

        retries = 0
        while True:
            try:
                page = requests.get('http://localhost:'+str(self.port), auth=(self.user,self.pwd))
            except (ConnectionError, ConnectionRefusedError):
                retries += 1
                print(f"Waiting for vlc hhtp interface - retry: {retries}")
                sleep(0.1)
                if retries > 9: raise ConnectionProblem
                continue
            break

        state = self.get_attributes()
        retries = 0
        while state['state'] == 'stopped':
            retries += 1
            print(f"Waiting for movie to start - retry: {retries}")
            sleep(0.1)
            state = self.get_attributes()

        self.set_sec_percentage()

    def get_attributes( self ):
        """ It parses the VLC status xml file and returns a dictionary of attributes. """
        page = requests.get('http://localhost:'+str(self.port)+'/requests/status.xml', auth=(self.user,self.pwd))

        attributes = {}
        et = ET.fromstring( page.text )

        # It is advised to look at the structure of status.xml to understand this
        for ele in et:
            # If element doesn't have sub elements.
            if len(ele) == 0:
                attributes[ ele.tag ] = ele.text
            else:
                attributes[ ele.tag ] = {}
                for subele in ele:
                    if subele.tag == "category":
                        subattr = attributes[ ele.tag ][ subele.get("name") ] = {}
                        for _subele in subele:
                            subattr[ _subele.get("name")] = _subele.text
                    else:
                        attributes[ ele.tag ][ subele.tag ] = subele.text
        return attributes

    def set_sec_percentage(self):
        """ Calculates and sets how much percentage of media each second represents for the seek() function. """
        attributes = self.get_attributes()

        try:
            media_length = int(attributes["length"])
            self.sec_percentage = 100 / media_length
            self.media_is_loaded = True
        except:
            self.media_is_loaded = False
            raise MediaNotLoaded()

    def send_command(self, command, val=None):
        """ Send commands to VLC http interface - seek, volume, pause/play etc ."""

        if (val == None ):
            requests.get('http://localhost:'+str(self.port)+'/requests/status.xml?command=' + command, auth=(self.user,self.pwd))
        else:
            requests.get('http://localhost:'+str(self.port)+'/requests/status.xml?command=' + command + '&val=' + urllib.parse.quote_plus(str(val)), auth=(self.user,self.pwd) )

##### COMMANDS

# Commands taking arguments.
    def seek_from_start(self, val):
        self.seek(val, self.SEEK_BEGIN)

    def seek(self, val, flag=SEEK_CUR):
        """ Seek the media to value given in seconds. By default, it seeks from current media position.
        Additionaly, flag SEEK_BEGIN can be passed to seek from beginning position."""
        attributes = self.get_attributes()

        if( not("length" in attributes) ):
            raise Exception("No media being played for seek command to work.")

        if( flag == self.SEEK_CUR ):
            seek_offset = float(attributes["position"]) * int(attributes["length"])
        elif( flag == self.SEEK_BEGIN ):
            seek_offset = 0
        else:
            raise Exception("Unknown flag passed.")

        seek_val_sec = seek_offset + val

        seek_percentage = (seek_val_sec / int(attributes["length"])) * 100

        self.send_command("seek", str(seek_percentage) + "%")

    def set_volume(self, val):
        """ Sets the volume of VLC. The interface expects value between 0 and 320
        Here we expect a value of 0-100 so scal to 0-320 """
        if val < 0: val = 0
        if val > 100: val = 100
        self.send_command("volume", 3.2 *  val)

    def set_rate(self, playback_rate=1):
        """ set playback rate. must be > 0 """
        if playback_rate > 0:
            self.send_command("rate", playback_rate)
        else:
            raise PlaybackRateError("Playback rate cannot be NEGATIVE")

    # fix this - also add in vlc process management - TODO
    # def play_file(self, in_file): # TODO - fix / test - in_file vs infile
    #     """ Send the input file to be played. The in_file must be a valid playable resource."""
    #
    #     if( not( os.path.isfile(infile) ) ):
    #         raise Exception("FileNotFound: The file " + infile + " does not exist.")
    #     else:
    #         self.send_command("in_file", "file://" + os.path.abspath(infile) )

# No-argument commands.
    def play(self):
        """ resume playback if paused, else do nothing """
        self.send_command("pl_forceresume")

    def pause(self):
        """ pause playback, do nothing if already paused """
        self.send_command("pl_forcepause")

    def play_pause(self):
        """Toggle between play and pause."""
        self.send_command("pl_pause")

    def stop(self):
        """Stops the player."""
        self.send_command("pl_stop")

    def toggle_fullscreen(self):
        """ Toggle fullscreen."""
        self.send_command("fullscreen")

    def is_fullscreen(self):
        if self.media_is_loaded:
            state = self.get_attributes()
            return(state['fullscreen'] == 'false')
        else:
            raise MediaNotLoaded

    def next(self):
        """ Next media on the playlist. """
        self.send_command("pl_next")

    def previous(self):
        """ Previous media on the playlist. """
        self.send_command("pl_previous")

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


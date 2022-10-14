#! /usr/bin/env python

# youtub
# ./vtdl.py 

# install: setup - TODO add to git
# > curl https://raw.githubusercontent.com/UnacceptableBehaviour/movie_picker/master/scripts/vtdl.py > vtdl.py
# > chmod +x vtdl.py
# > python3 -m venv venv
# > . venv/bin/activate           # or source venv/bin/activate
# > pip install youtube_dl
# > ./vtdl.py                     # update channel downloads
#
'''
# EG text file
# lines that begin with hash/pound sign are ignored
# anything after " #" space hash/pound sign are ignored
'''
# Steps
# Get dict of currently downloaded videos - create if no file exists.
# Load channel/videos list
# Get number of videos / per channel and delta on currently downloaded
# Download delta for each channel, create a copy in channel directory & new videos

from __future__ import unicode_literals
import youtube_dl
import sys
from pathlib import Path
from pprint import pprint
from threading import *

class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def my_hook(d):
    print('> HOOK - - - - - - - - - - - - - - - - - - - - - - - - S')
    
    pprint(d)
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')
    print('> HOOK - - - - - - - - - - - - - - - - - - - - - - - - E')

class Dload(Thread):
    tick = 0
    status = {}

    @staticmethod
    def my_hook(d):
        print('> D.HOOK - - - - - - - - - - - - - - - - - - - - - - - - S')
        pc = int(float(d['_percent_str'].strip().replace('%','')))
        title = (d['filename'][:30] + '..') if len(d['filename']) > 32 else d['filename']
        progress = '#'*pc + '-'*(100-pc)
        Dload.status[d['filename']] = f"|{progress}|{d['_percent_str']} {title}"
        Dload.tick +=1
        if Dload.tick > 102: Dload.tick =0
        print('+'*Dload.tick)
        for f,line in Dload.status.items():
            print(line)
        
        #pprint(d)
        if d['status'] == 'finished':
            print('Done downloading ...')
        print('> D.HOOK - - - - - - - - - - - - - - - - - - - - - - - - E')

    def __init__(self, url_to_fetch, target_dir, ydl_opts=None):
        super().__init__()
        """Create a FileDownloader object with the given options."""
        self.target_dir = target_dir
        self.url_to_fetch = url_to_fetch
        self.ydl_opts = {
            #'format': 'bestaudio/best',
            'outtmpl': f"{self.target_dir}/%(title)s-%(id)s.%(ext)s",
            # 'postprocessors': [{
            #     'key': 'FFmpegExtractAudio',
            #     'preferredcodec': 'mp3',
            #     'preferredquality': '192',
            # }],
            'logger': MyLogger(),
            'progress_hooks': [Dload.my_hook],
        }
        if ydl_opts is None:
            ydl_opts = {}
        self.ydl_opts.update(ydl_opts)
        self.ydl = youtube_dl.YoutubeDL(self.ydl_opts)
    
    def run(self):
        self.ydl.download([self.url_to_fetch])
    




VID_LIST = Path('/Volumes/Osx4T/05_download_tools_open_source/yt_dl/20221013_test.txt')
vids = []
with open(VID_LIST, 'r') as f:
    file_content = f.read()    
    vids = [ url.strip() for url in file_content.split('\n') ]

# create directory for downloads
target_dir = Path(f"./{VID_LIST.stem}")
try:
    Path.mkdir(target_dir, parents=True)
except Exception:
    print(f"** WARNING ** target_dir already created\n{target_dir}")
    # yn = input('Continue (y)/n\n')
    # if yn.strip().lower() == 'n': sys.exit(0)
        
pprint(vids)
# print(VID_LIST.name)
# print(VID_LIST.stem)
# print(VID_LIST.suffix)

#sys.exit(0)
            
ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': f"./{VID_LIST.stem}/%(title)s-%(id)s.%(ext)s",
    # 'postprocessors': [{
    #     'key': 'FFmpegExtractAudio',
    #     'preferredcodec': 'mp3',
    #     'preferredquality': '192',
    # }],
    'logger': MyLogger(),
    'progress_hooks': [my_hook],
}

thread_list = []
for v in vids:
    print(f"Downloading: {v} - - - - - \ ")
    pprint(ydl_opts)
    print(f"Downloading: - - - - - / ")
    # with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    #     ydl.download([v])
    thread_list.append(Dload(v, VID_LIST.stem))
    
for t in thread_list:
    t.start()
    
    

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



class Dload(Thread):
    tick = 0
    status = {}

    @staticmethod
    def prog_hook(d):        
        print("\x1B\x5B1J") # clear screen above the cursor ESC [ 1 J - https://en.wikipedia.org/wiki/ANSI_escape_code
                            # https://ss64.com/ascii.html
        pc = int(float(d['_percent_str'].strip().replace('%','')) / 2)
        title = (d['filename'][:80] + '..') if len(d['filename']) > 82 else d['filename']
        progress = '#'*pc + '-'*(50-pc)
        eta = f"{int(d['eta'] / 60)}m{int(d['eta'] % 60)}".rjust(6, ' ')
        Dload.status[d['filename']] = [f"|{progress}|{d['_percent_str']} {d['_total_bytes_str'].rjust(10, ' ')} {eta} {title}", d]
        Dload.tick +=1
        if Dload.tick > 102: Dload.tick =0
        print('+'*Dload.tick)
        for f,line in Dload.status.items():
            print(line[0])
        
        pprint(d)
        if d['status'] == 'finished':
            print('Done downloading ...')
        #print('> D.HOOK - - - - - - - - - - - - - - - - - - - - - - - - E')

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
            'progress_hooks': [Dload.prog_hook],
        }
        if ydl_opts is None:
            ydl_opts = {}
        self.ydl_opts.update(ydl_opts)
        self.ydl = youtube_dl.YoutubeDL(self.ydl_opts)
    
    def run(self):
        self.ydl.download([self.url_to_fetch])


VID_LIST = Path('/Volumes/Osx4T/05_download_tools_open_source/yt_dl/20221014_test.txt')
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
    
    

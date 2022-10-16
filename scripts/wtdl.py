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
#from threading import * # causes enumerate() takes 0 positional arguments but 1 was given
import threading

class MyLogger(object):
    logged_errors = []
    log_lock = threading.Lock()
    
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        with MyLogger.log_lock:
            MyLogger.logged_errors.append(msg)
        print("> - - - - - - ERROR LOGGED")
        #print(msg)
    
    @staticmethod
    def dump_logs():        
        for cnt, e in enumerate(MyLogger.logged_errors):
            print('eLOG: {cnt} - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -')
            print(e)
        return MyLogger.logged_errors
        
    



class Dload(threading.Thread):
    tick = 0                      # # #
    prog_dict = {}                    #
    all_done = False                  #
    total_bandwidth_use = 0           #
    prog_lock = threading.Lock()  # # #
    
    
    
    @staticmethod
    def prog_hook(dl_data):        
        #print("\x1B\x5B1J") # clear screen above the cursor ESC [ 1 J - https://en.wikipedia.org/wiki/ANSI_escape_code
                            # https://ss64.com/ascii.html
        if '_percent_str' in dl_data:
            pc = int(float(dl_data['_percent_str'].strip().replace('%','')) / 2)
            pc_str = dl_data['_percent_str']
        else:
            pc = 0
            pc_str = '  0.0%'
            
            
        title = (dl_data['filename'][:80] + '..') if len(dl_data['filename']) > 82 else dl_data['filename']
        progress = '#'*pc + '-'*(50-pc)
        eta = 9999
        try:
            eta = f"{int(dl_data['eta'] / 60)}m{int(dl_data['eta'] % 60)}".rjust(6, ' ')
        except Exception:
            # print('> prog_hook - - - - - - - - - - - - - - - S')
            # pprint(dl_data)                
            # print('> prog_hook - - - - - - - - - - - - - - - E')
            if dl_data['status'] == 'finished':
                with Dload.prog_lock:
                    if dl_data['filename'] in Dload.prog_dict:
                        del Dload.prog_dict[dl_data['filename']]                
                print(f"FINISHED: {dl_data['filename']}")
                return

        with Dload.prog_lock:            
            Dload.prog_dict[dl_data['filename']] = { 'p_bar': f"|{progress}|{pc_str} {dl_data['_total_bytes_str'].rjust(10, ' ')} {eta} {title} {dl_data['status']}",
                                                     'stats': dl_data }
        
        Dload.tick +=1
        if Dload.tick > 102: Dload.tick =0
        print('+'*Dload.tick)

        with Dload.prog_lock:
            for f, info in Dload.prog_dict.items():
                print(info['p_bar'])     
        
        #pprint(dl_data)
        print(Dload.combine_stats(dl_data)['formatted'])

    @staticmethod
    def combine_stats(caller_data):
        report = ''
        all_done = True
        download_count = 0
        total_bandwidth_use = 0
        
        with Dload.prog_lock:  
            for f, info in Dload.prog_dict.items():
                dl_data = info['stats']
                if not ((dl_data['status'] == 'finished') or (dl_data['_percent_str'] == '100.0%')):
                    all_done = False
                    if dl_data['speed']: total_bandwidth_use += dl_data['speed']
                    download_count += 1
        
            Dload.total_bandwidth_use = total_bandwidth_use
            Dload.all_done = all_done
            
        if total_bandwidth_use < 1024:
            bandwidth_str = f"Total download rate: {int(total_bandwidth_use):.2f} B/s"
        elif total_bandwidth_use/1024 < 1024:
            bandwidth_str = f"Total download rate: {int(total_bandwidth_use/1024):.2f} KiB/s"
        elif total_bandwidth_use/(1024*1024) < 1024:
            bandwidth_str = f"Total download rate: {int(total_bandwidth_use/(1024*1024)):.2f} MiB/s"
        else:
            bandwidth_str = f"Total download rate: {int(total_bandwidth_use/(1024*1024*1024)):.2f} GiB/s"
        
        report = f"\n{bandwidth_str}\nDownloads: {download_count}\nThreads: {threading.active_count()}\n"
        
        return {'formatted' : report, 'status': all_done}



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
        # TODO wait on bandwidth available
        self.ydl.download([self.url_to_fetch])
        # TODO check bandwidth & notify on exit


VID_LIST = Path('/Volumes/Osx4T/05_download_tools_open_source/yt_dl/20221016_test.txt')
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
    print(f"Queueing: {v} for download.")
    thread_list.append(Dload(v, VID_LIST.stem))
    
for t in thread_list:
    t.start()

# TODO
# pass file to process as argv
# remove commented files from list of files to dload
# pause thread when tot_dload_band > 2MiB / sec
#   add notify to end of download

#! /usr/bin/env python

# youtub
# ./vtdl.py 

# install: setup - TODO add to git, EDIT THESE INSTRUCTIONS
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
import json
import re
from pprint import pprint
import threading
import time
from datetime import datetime       # datetime.now().timestamp() = 1666356102.098952

# file IO helpers - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \
#
def load_dict_data_from_DB(cDB, db_path):
    '''
    load dict info from text file - json format
    '''

    if db_path.exists():
        with open(db_path, 'r') as f:
            json_db = f.read()
            db = json.loads(json_db)
            print(f"Database dict LOADED ({len(db)})")

        for i in db.keys():
            cDB[i] = db[i]

        print(f"Dict to json > objects COMPLETE ({len(cDB)})")
        return 0

    else:
        db = {}  # create a blank file
        commit_dict_to_DB(db, db_path)
        return -1

def commit_dict_to_DB(commit_db, db_path):
    '''
    commit dict info to text file - json format
    '''

    with open(db_path, 'w') as f:
        #pprint(commit_db)
        db_as_json = json.dumps(commit_db)
        f.write(db_as_json)
        
def get_urls_from_file(filename):
    with open(filename, 'r') as f:
        content = f.read()

    url_list = []
    for line in content.split('\n'):
        if len(line.strip()) == 0: continue
        if re.findall('^#', line): continue
        if '#' in line:
            line = line.split('#')[0]
        url_list.append(line)   # maybe add regex to check valid url

    return url_list
#
# file IO helpers - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - /

#
# subscriptions - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \
channel_DB = {}
CHANNEL_DB_FILE = Path('/Volumes/Osx4T/05_download_tools_open_source/yt_dl/vtdl/channel_downloads.json')
load_dict_data_from_DB(channel_DB, CHANNEL_DB_FILE)
NO_OF_ITEMS_PER_CHAN = 40
playlist_items = f"1-{NO_OF_ITEMS_PER_CHAN}"

def get_playlist_update(cDB, chan_key, group_dir, pl_url, ydl_opts_pass={}):
    print(f"Getting PL from: {pl_url}")
    play_list = {}
    new_vid_entries = {}
    
    ydl_opts = {'quiet':True,
                'playlistreverse':True,
                'ignoreerrors':True}
    
    ydl_opts.update(ydl_opts_pass)
    
    if chan_key not in cDB.keys(): ydl_opts['playlist_items'] = None   # download everything
    pprint(ydl_opts)

    ydl = youtube_dl.YoutubeDL(ydl_opts)

    with ydl:
        result = ydl.extract_info(pl_url, download=False) 
    
        if 'entries' in result:
            videos = result['entries']           # list of dict            

            for i, video in enumerate(videos):
                # see Osx4T/05_download_tools_open_source/yt_dl/vtdl/video.json for object info
                try:
                    if video == None:
                        print(f"{(i):03}: K: -- -- - * * * * Download not available * * * *")
                        continue
                    else:
                        print(f"{(i):03}: K:{video['webpage_url_basename']} {video['webpage_url']} - {video['title']}")   # {i:03} left pad n with 0's 3 digits
                        play_list[video['webpage_url_basename']] = { 'src_url': video['webpage_url'],
                                                                     'group_dir': None,
                                                                     'target_dir': chan_key,                                                                     
                                                                     'pos': i,
                                                                     'idx': video['playlist_index'],
                                                                     'title': video['title'],
                                                                     'downloaded': False,
                                                                     'url_basename': video['webpage_url_basename']}            
                except Exception as e:
                    print(f"> get_playlist - Error <{i}>")
                    pprint(e)

    if chan_key in cDB.keys():
        vid_pos = None
        for k, video in play_list.items():
            if k in cDB[chan_key].keys():
                vid_pos = cDB[chan_key][k]['pos']
                print(f"P:{(video['pos']):04} K:{k} {video['src_url']} - {video['title']}")
                      # P-resent video
            if k not in cDB[chan_key].keys():
                new_vid_entries[k] = video
                vid_pos += 1
                new_vid_entries[k]['pos'] = vid_pos
                print(f"N:{(video['pos']):04} K:{k} {video['src_url']} - {video['title']}")
                      # N-ot present video
        
        return new_vid_entries
    
    return play_list

# subscriptions - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - /
#


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
    def num_of_errors():
        return( len(MyLogger.logged_errors) )
    
    @staticmethod
    def dump_logs():        
        for cnt, e in enumerate(MyLogger.logged_errors):
            print('eLOG: {cnt} - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -')
            print(e)
        return MyLogger.logged_errors
        
    

class DloadProgressDisplay(threading.Thread):    
    def __init__(self):
        super().__init__()
        
    def updateProgress(self):
        with Dload.prog_lock:            
            Dload.tick +=1
            if Dload.tick > 102: Dload.tick =0
            print('+'*Dload.tick)
            
            dump = None
            for f, info in Dload.prog_dict.items():
                dump = info
                print(info['p_bar'])     
        
        print(Dload.combine_stats())
        #print(f"{datetime.now().timestamp()} - {len(Dload.prog_dict)}")
        #pprint(dump)     
        
    def run(self):
        print("STARTED . . . DloadProgressDisplay . . waiting for downloads to start")
                
        while (Dload.registrations == 0):   # WAITING_FOR_DOWLOANDS_TO_START
            time.sleep(1)
        
        time.sleep(1) # (Allow Dload.all_done to change to False)
        
        while (Dload.all_done == False):
            self.updateProgress()
            time.sleep(1)            

        print("ALL DONE . . .")
        sys.exit(0)
    

class Dload(threading.Thread):
    tick = 0                      # # #
    prog_dict = {}                    #
    registrations = 0                 #
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
            if dl_data['status'] == 'finished':
                with Dload.prog_lock:
                    if dl_data['filename'] in Dload.prog_dict:
                        del Dload.prog_dict[dl_data['filename']]                
                print(f"FINISHED: {dl_data['filename']}")
                return

        with Dload.prog_lock:            
            Dload.prog_dict[dl_data['filename']] = { 'p_bar': f"|{progress}|{pc_str} {dl_data['_total_bytes_str'].rjust(10, ' ')} {eta} {title} {dl_data['status']}",
                                                     'stats': dl_data }
            if Dload.registrations < len(Dload.prog_dict): Dload.registrations = len(Dload.prog_dict)
        

    @staticmethod
    def combine_stats():
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
        
        report = f"\n{bandwidth_str}\nDownloads: {download_count}\nThreads: {threading.active_count()}\nErrors: {MyLogger.num_of_errors()}"
        
        return report



    def __init__(self, url_to_fetch, base_dir, group_dir, target_dir, ydl_opts=None):
        super().__init__()
        """Create a FileDownloader object with the given options."""
        print(f"output_template: {base_dir}, {group_dir}, {target_dir}")
        self.url_to_fetch = url_to_fetch
        self.base_dir = base_dir.strip('/')
        self.group_dir = group_dir.strip('/')
        self.target_dir = target_dir.strip('/')
        output_template =  f"{self.base_dir}/"   if self.base_dir else ''
        output_template += f"{self.group_dir}/"  if self.group_dir else ''
        output_template += f"{self.target_dir}/" if self.target_dir else ''
        output_template += "%(title)s-%(id)s.%(ext)s"
        print(f"output_template: {output_template}")
        self.ydl_opts = {
            #'format': 'bestaudio/best',
            'outtmpl': output_template,
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



# ytdl will create any directories necessary
# TODO - REMOVE
# VID_ROOT = Path('/Volumes/Osx4T/05_download_tools_open_source/yt_dl/')
# # create directory for downloads
# target_dir = Path(VID_ROOT, f"./{VID_LIST.stem}")
# try:
#     print(f"Creating: {target_dir}")
#     Path.mkdir(target_dir, parents=True)
# except Exception:
#     print(f"** WARNING ** target_dir already created\n{target_dir}")
#     # yn = input('Continue (y)/n\n')
#     # if yn.strip().lower() == 'n': sys.exit(0)


def create_dld_thread_info( details={} ):
    thread_info =  { 'downloaded': False,
                    'base_dir': 'vtdl',
                    'group_dir': '',
                    'target_dir': '',
                    'idx': None,
                    'pos': None,
                    'src_url': '',
                    'title': '' }
    thread_info.update(details)
    #pprint(thread_info)
    return thread_info


# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
# ENTRY POINT __main__
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =


# ALL files to be downloaded in this session
DLOAD_SESSION_DB = Path('vtdl/dl_session.json')
download_thread_info_dict = {}

if DLOAD_SESSION_DB.exists():
    load_dict_data_from_DB(download_thread_info_dict, DLOAD_SESSION_DB)
    print("* * * * Previous download session exists CONTINUE downloads? * * * *")
    # TODO implement persistence flow
    

if '-f' in sys.argv:
    option_f_index = sys.argv.index('-f')
    dload_file = sys.argv[option_f_index+1] # VID_LIST
    if Path(dload_file).exists():
        dload_file = Path(dload_file)
        vid_url_list = get_urls_from_file(dload_file)
        
        download_thread_info_dict[dload_file.stem] = []
        
        for v_url in vid_url_list:
             download_thread_info_dict[dload_file.stem].append(create_dld_thread_info({
                'downloaded': False,
                'base_dir': 'vtdl',
                'group_dir': 'url_file',
                'target_dir': dload_file.stem,
                'idx': None,
                'pos': None,
                'src_url': v_url,
                'title': '' }))
        
        del(sys.argv[option_f_index+1])
        del(sys.argv[option_f_index])
    else:
        print(f"* * * WARNING * * *\nFile spcified by option -f\nNOT FOUND:{dload_file} <")


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# update subscriptions
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
CHANNEL_VIDEOS_FILE = Path('./vtdl/vtdl_video_channel_list.txt')
video_channel_urls = get_urls_from_file(CHANNEL_VIDEOS_FILE)

# r - reload - load all video info if channel doesn't exist, build list of new entries if it does
# u - update DB - LIVE!
download_targets_all = {}
if '-r' in sys.argv:        # - - - - - - - - - - - - - - - - - - - - - - - - RELOAD (-r) & RECORD NEW (-u)
    for channel_url in video_channel_urls:
        print(f"URL: {channel_url}")
        channel_key = channel_url.replace('https://www.youtube.com/c/','').replace('https://www.youtube.com/user/','').replace('https://www.youtube.com/channel/','').replace('/videos','') 
        print(f"channel_key: {channel_key}")
        video_dict = None
        recent_chan_vid_info = None
        group_dir = None
        try:
            if channel_key not in channel_DB:
                video_dict = get_playlist_update(channel_DB, channel_key, group_dir, channel_url, {'quiet':False, 'verbose':True, 'forceurl':True})
            else:
                recent_chan_vid_info = get_playlist_update(channel_DB, channel_key, group_dir, channel_url, {'playlist_items': playlist_items, 'verbose':True, 'forceurl':True})
        except BaseException as e:
            print('> - Error getting PLay List Info')
            pprint(e)            
        finally:            
            if ('-u' in sys.argv) and (video_dict or recent_chan_vid_info):
                print('> - SAVING DATA')
                if channel_key in channel_DB:
                    channel_DB[channel_key].update(recent_chan_vid_info)
                else:
                    channel_DB[channel_key] = video_dict
                commit_dict_to_DB(channel_DB, CHANNEL_DB_FILE)
        
        vid_info = video_dict if video_dict else recent_chan_vid_info
        
        print(f"> - - - - - - - - Downloaded video info for {channel_key} - - - - - - - - <")
        pprint(vid_info)
        download_targets_all[channel_key] = []
        
        if vid_info:
            for k, video in vid_info.items():
                download_targets_all[channel_key].append(video)        
        print("     > - - - - - - - - - - - - Channel END - - - - - - - - - - - - <\n\n\n\n")


print(f"> - - - - - - - - Downloaded video info for ALL channels - - - - - - - - <")
pprint(download_targets_all)
print("     > - - - - - - - - - - - - PASS to threads - - - - - - - - - - - <\n\n\n\n")


# create thread info dict for downloads
for target_dir, vid_list in download_targets_all.items():
    if len(vid_list) == 0: continue
    if target_dir not in download_thread_info_dict: download_thread_info_dict[target_dir] = []
    for dload_target_info in vid_list:
        thread_info = create_dld_thread_info(dload_target_info)   # fill in gaps in thread dict
        download_thread_info_dict[target_dir].append(thread_info)

pprint(download_thread_info_dict)
#sys.exit(0)

# AFTER ALL OPTIONS PROCESSED SAVE DLOAD SESSION INFO as JSON        
commit_dict_to_DB(download_thread_info_dict, DLOAD_SESSION_DB)
# sys.exit(0)


thread_list = []
for target_dir, vid_list in download_thread_info_dict.items():
    for thread_info in vid_list:
        print(f"Queueing: {thread_info['src_url']} for download.")
        #def __init__(self, url_to_fetch, base_dir, group_dir, target_dir, ydl_opts=None):
        thread_list.append(Dload(thread_info['src_url'], thread_info['base_dir'], thread_info['group_dir'], thread_info['target_dir']))
    
for t in thread_list:
    print(f"{t.native_id} start:{t.target_dir} - {t.url_to_fetch})")
    t.start()

DloadProgressDisplay().start()



sys.exit(0) # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# VID_LIST = Path('/Volumes/Osx4T/05_download_tools_open_source/yt_dl/20221021_5mins_long.txt')
# vids = get_urls_from_file(VID_LIST)
# 
# pprint(vids)
# 
# thread_list = []
# for v in vids:
#     print(f"Queueing: {v} for download.")
#     #def __init__(self, url_to_fetch, base_dir, group_dir, target_dir, ydl_opts=None):
#     thread_list.append(Dload(v, 'vtdl', 'url_file', VID_LIST.stem))
#     
# for t in thread_list:
#     print(f"{t.native_id} start:{t.target_dir} - {t.url_to_fetch})")
#     t.start()
# 
# DloadProgressDisplay().start()

# TODO
# pause thread when tot_dload_band > 2MiB / sec
# update DLOAD_SESSION_DB at end - or DELETE!

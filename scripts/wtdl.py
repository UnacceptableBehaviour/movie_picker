#! /usr/bin/env python

# youtube
# ./wtdl.py 

# install: setup - TODO add to git, EDIT THESE INSTRUCTIONS
# > curl https://raw.githubusercontent.com/UnacceptableBehaviour/movie_picker/master/scripts/wtdl.py > wtdl.py
# > chmod +x wtdl.py
# > python3 -m venv venv
# > . venv/bin/activate           # or source venv/bin/activate
# > pip install youtube_dl
# > ./wtdl.py                     # update channel downloads
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
import atexit
from pprint import pprint
import threading
import time
from datetime import datetime       # datetime.now().timestamp() = 1666356102.098952

import traceback


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
            print(f"Database dict [{db_path.stem}] LOADED ({len(db)})")

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
    # TODO create dir if it doesn't exist
    print(f"COMMIT: {db_path}", end='')
    
    with open(db_path, 'w') as f:
        #pprint(commit_db)
        db_as_json = json.dumps(commit_db)
        f.write(db_as_json)

    print(' - DONE:')


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

@atexit.register                # smae as atexit.register(write_state_to_disk)
def write_state_to_disk():
    download_thread_info_remaining = {}
    for channel,dloads in download_thread_info_dict.items():
        if len(dloads) > 0: download_thread_info_remaining[channel] = download_thread_info_dict[channel]
    
    if len(download_thread_info_remaining) > 0: 
        commit_dict_to_DB(download_thread_info_remaining, Dload.DLOAD_SESSION_DB)
    else:
        print('DOWNLOADS COMPLETED - NO ERRORS')
        Path.unlink(Dload.DLOAD_SESSION_DB)

    commit_dict_to_DB(channel_DB, CHANNEL_DB_FILE)

#
# file IO helpers - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - /

#
# subscriptions - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \
channel_DB = {}
CHANNEL_DB_FILE = Path('./chanDloads/channel_downloads.json')
load_dict_data_from_DB(channel_DB, CHANNEL_DB_FILE)
NO_OF_ITEMS_PER_CHAN = 20
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

    # download play list whole if new or in part if updating
    ydl = youtube_dl.YoutubeDL(ydl_opts)

    # gather relevant info about playlist items
    with ydl:
        result = ydl.extract_info(pl_url, download=False) 
    
        if 'entries' in result:
            videos = result['entries']           # list of dict            

            for i, video in enumerate(videos):
                # see Osx4T/05_download_tools_open_source/yt_dl/chanDloads/video.json for object info
                try:
                    if video == None:
                        print(f"{(i):03}: K: -- -- - * * * * Download not available * * * *")
                        pprint(video)
                        continue
                    else:
                        print(f"P:{(i):04} I:{(video['playlist_index']):04} K:{video['webpage_url_basename']} {video['webpage_url']} - {video['title']}")   # {i:03} left pad n with 0's 3 digits
                        play_list[video['webpage_url_basename']] = { 'src_url': video['webpage_url'],
                                                                     'group_dir': '',
                                                                     'target_dir': chan_key,                                                                     
                                                                     'pos': i,
                                                                     'idx': video['playlist_index'],
                                                                     'title': video['title'],
                                                                     'downloaded': False,
                                                                     'url_basename': video['webpage_url_basename']}            
                except Exception as e:
                    print(f"> get_playlist - Error <{i}>")
                    pprint(e)

    # return entries not in the download DB
    if chan_key in cDB.keys():
        print(f"Finding new entries in > {chan_key} <")
        vid_pos = None
        
        for k, video in play_list.items():
            print('- - - - - - - - - - - - - \ ')
            pprint(video)
        
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
        
        while (len(Dload.prog_dict) == 0) and (Dload.dloads_complete < 1):   # WAITING_FOR_DOWLOANDS_TO_START
            time.sleep(1)
        
        time.sleep(1) # (Allow Dload.all_done to change to False)
        
        while (Dload.all_done == False):
            self.updateProgress()
            time.sleep(1)            

        print("ALL DONE . . .")
        sys.exit(0)



# TODO - move into class?
download_thread_info_dict = {}      # Stored DLOAD_SESSION_DB

class Dload(threading.Thread):
    tick = 0                                # # #
    prog_dict = {}                              # use for registrations
    dloads_complete = 0                         #
    all_done = False                            #
    total_bandwidth_use = 0                     #
    DLOAD_SESSION_DB = Path('./chanDloads/dl_session.json')  # ALL files to be downloaded in this session
    dload_session_db_lock = threading.Lock()    #
    prog_lock = threading.Lock()            # # #
    
    @staticmethod
    def prog_hook(dl_data):
        # dl_data - - - - - - - - - - \     # TODO - REMOVE
        # {'_elapsed_str': '01:16:58',
        # '_total_bytes_str': '203.44MiB',
        # 'downloaded_bytes': 213327478,
        # 'elapsed': 4618.32977104187,
        # 'filename': 'chanDloads/chan/@LivBoeree/14-The Future of Humanity _ Anders '
        #             'Sandberg and Liv Boeree-crFk-fDBu6A.mp4',
        # 'status': 'finished',
        # 'total_bytes': 213327478}
        # dl_data - - - - - - - - - - /     
        #     
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
        except Exception as err: # TODO - specify Exception
            print(f"# # > ETA except:{err} < <        -        -        - <<")
            if dl_data['status'] == 'finished':
                with Dload.prog_lock:
                    print('dl_data - - - - - - - - - - \ ') # TODO remove
                    pprint(dl_data)
                    print('dl_data - - - - - - - - - - / ')
                    if dl_data['filename'] in Dload.prog_dict:
                        del Dload.prog_dict[dl_data['filename']]
                    Dload.dloads_complete += 1
                
                with Dload.dload_session_db_lock: # mark as downloaded
                    chan_or_file_dir = chan_or_file_name = title = url_basename = None
                    m = re.search(r'chanDloads\/(.*?)\/(.*?)\/\d+-(.*?)-([a-zA-Z0-9\-_]{11})\.', dl_data['filename'])
                    if m:
                        chan_or_file_dir  = m.group(1)
                        chan_or_file_name = m.group(2)
                        title             = m.group(3)
                        url_basename      = m.group(4)
                    # move out of download_thread_info_dict
                    # add filename
                    # mark as downloaded
                    # move into channel_DB, 
                    print(f"\nurl_basename:{url_basename} - {chan_or_file_dir}/{chan_or_file_name} - {title}")
                    for dlt_chan_name,dlt_list in download_thread_info_dict.items():
                        if dlt_chan_name == chan_or_file_name:
                            for i, dlt in enumerate(dlt_list):
                                if url_basename in dlt['src_url']:
                                    print(f"FOUND: {url_basename} @ {i}")
                                    dlt['downloaded'] = True
                                    dlt['url_basename'] = url_basename
                                    if dlt_chan_name in channel_DB.keys():
                                        channel_DB[dlt_chan_name][url_basename] = dlt
                                    else:
                                        channel_DB[dlt_chan_name] = { url_basename: dlt }
                                    print('dlt - - - - - - - - - - \ ')
                                    pprint(dlt)
                                    print('dlt - - - - - - - - - - / ')
                                    del(dlt_list[i]) # dlt
                                    print(f"-*- DEL:{i}")
                                    commit_dict_to_DB(download_thread_info_dict, Dload.DLOAD_SESSION_DB)
                                    break



                print(f"FINISHED: {dl_data['filename']}")
                return

        with Dload.prog_lock:            
            Dload.prog_dict[dl_data['filename']] = { 'p_bar': f"|{progress}|{pc_str} {dl_data['_total_bytes_str'].rjust(10, ' ')} {eta} {title} {dl_data['status']}",
                                                     'stats': dl_data }


# Update this at the end of each thread
# Semtake on fileLock:
# with Dload.dload_session_db_lock:
#   update download_thread_info_dict    (saved later) commit_dict_to_DB(download_thread_info_dict, Dload.DLOAD_SESSION_DB)
#       remove the download. 
#       -([a-zA-Z0-9\-_]{11})\.    
# 
# Add to channel_DB as downloaded
#   Commit that to file
#   
#     
# dictof 
#     key = target_dir
#         LIST
#         src_url
#         target_dir

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
        
        report = f"\n{bandwidth_str}\nDownloads: {download_count}\nThreads: {threading.active_count()}\nErrors: {MyLogger.num_of_errors()}\nAll done flag: {all_done}"
        
        return report



    def __init__(self, pos, url_to_fetch, base_dir, group_dir, target_dir, ydl_opts=None):
        super().__init__()
        """Create a FileDownloader object with the given options."""
        print(f"output_template: {base_dir}, {group_dir}, {target_dir}")
        self.url_to_fetch = url_to_fetch
        self.base_dir = base_dir.strip('/') if base_dir else ''
        self.group_dir = group_dir.strip('/') if group_dir else ''
        self.target_dir = target_dir.strip('/') if target_dir else ''
        output_template =  f"{self.base_dir}/"   if self.base_dir else ''
        output_template += f"{self.group_dir}/"  if self.group_dir else ''
        output_template += f"{self.target_dir}/" if self.target_dir else ''
        output_template += f"{pos:02}-%(title)s-%(id)s.%(ext)s"
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



def create_dld_thread_info( details={} ):
    thread_info =  { 'downloaded': False,
                    'base_dir': 'chanDloads',
                    'group_dir': '',
                    'target_dir': '',
                    'idx': None,
                    'pos': None,
                    'src_url': '',
                    'title': '',
                    'url_basename': '' }
    
    thread_info.update(details)
    #pprint(thread_info)
    return thread_info

def print_download_intent(download_thread_info_dict):
    #pprint(download_thread_info_dict)
    for chan, info in download_thread_info_dict.items():
        print(f"\n# # # # #   Chan: {chan} ({len(info)})  - Dir: base/group/chan")        
        if len(info) > 0: pprint(info[0])
    



# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
# ENTRY POINT __main__
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

if Dload.DLOAD_SESSION_DB.exists():
    load_dict_data_from_DB(download_thread_info_dict, Dload.DLOAD_SESSION_DB)
    
file_dload_only = False
file_channel = None
if ('-f' in sys.argv) or ('-fo' in sys.argv):    
    if ('-f' in sys.argv): option_f_index = sys.argv.index('-f')
    if ('-fo' in sys.argv):
        option_f_index = sys.argv.index('-fo')
        file_dload_only = True
    dload_file = sys.argv[option_f_index+1] # VID_LIST
    if Path(dload_file).exists():
        print(f"PROCESSING File:{dload_file} <")
        dload_file = Path(dload_file)
        vid_url_list = get_urls_from_file(dload_file)
        
        if dload_file.stem not in download_thread_info_dict: download_thread_info_dict[dload_file.stem] = []
        file_channel = dload_file.stem
        
        vid_pos_in_list = 1
        for v_url in vid_url_list:
            download_thread_info_dict[dload_file.stem].append(create_dld_thread_info({
                'downloaded': False,
                'base_dir': 'chanDloads',
                'group_dir': 'nonSub',
                'target_dir': dload_file.stem,
                'idx': None,
                'pos': vid_pos_in_list,
                'src_url': v_url,
                'title': '' }))
            pprint(len(download_thread_info_dict[dload_file.stem])-1)
            pprint(download_thread_info_dict[dload_file.stem][len(download_thread_info_dict[dload_file.stem])-1])
            vid_pos_in_list += 1
        
        del(sys.argv[option_f_index+1])
        del(sys.argv[option_f_index])
    else:
        print(f"\n\n* * * WARNING * * *\nFile spcified by option -f/fo\nNOT FOUND:{dload_file} <\n\n")
        sys.exit(0)


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# update subscriptions
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
CHANNEL_VIDEOS_FILE = Path('./chanDloads/video_channel_list.txt')
video_channel_urls = get_urls_from_file(CHANNEL_VIDEOS_FILE)

# r - reload - load all video info if channel doesn't exist, build list of new entries if it does
# u - update DB - LIVE!
download_targets_all = {}
if '-r' in sys.argv:        # - - - - - - - - - - - - - - - - - - - - - - - - RELOAD (-r) & RECORD NEW (-u)
    for channel_url in video_channel_urls:
        print(f"URL: {channel_url}")
        channel_key = channel_url.replace('https://www.youtube.com/','').replace('/videos','') 
        print(f"channel_key: {channel_key}")
        video_dict = None
        recent_chan_vid_info = None
        group_dir = 'chan'
        try:
            if channel_key not in channel_DB:
                video_dict = get_playlist_update(channel_DB, channel_key, group_dir, channel_url, {'quiet':False, 'verbose':True, 'forceurl':True})
            else:
                recent_chan_vid_info = get_playlist_update(channel_DB, channel_key, group_dir, channel_url, {'playlist_items': playlist_items, 'verbose':True, 'forceurl':True})
        except BaseException as e:
            print('> - Error getting PLay List Info')
            print(traceback.format_exc())
            print('-')
            pprint(e)
            print('==')
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

# TODO add cron option to skip this
if len(download_thread_info_dict) > 0:
    print_download_intent(download_thread_info_dict)
    print('')
    pprint(sys.argv)
    print('')
    if file_dload_only: print(f"File download ONLY:{file_dload_only}") 
    yn = input('Continue (y)/n\n')
    if yn.strip().lower() == 'n': sys.exit(0)


# save the intent for the download session
commit_dict_to_DB(download_thread_info_dict, Dload.DLOAD_SESSION_DB)

thread_list = []
for target_dir, vid_list in download_thread_info_dict.items():
    if (file_dload_only) and (file_channel != target_dir): continue 
    for thread_info in vid_list:
        print(f"Queueing: {thread_info['src_url']} for download.")
        if thread_info['group_dir'] == '': thread_info['group_dir'] = 'chan' # TODO - REMOVE
        #def __init__(self, url_to_fetch, base_dir, group_dir, target_dir, ydl_opts=None):
        thread_list.append(Dload(thread_info['pos'], thread_info['src_url'], thread_info['base_dir'], thread_info['group_dir'], thread_info['target_dir']))
    
for t in thread_list:
    print(f"{t.native_id} start:{t.target_dir} - {t.url_to_fetch}")
    t.start()

if '-i' in sys.argv:
    print(f"\n> Dload Info [{len(download_thread_info_dict)}]: - - - - - - - - - - - <")
    if len(download_thread_info_dict):
        pprint(next(iter(download_thread_info_dict)))   # dump an item
        pprint(download_thread_info_dict[next(iter(download_thread_info_dict))])
        for chan,vid_list in download_thread_info_dict.items():
            print(f"C: {chan} - {len(vid_list)}") 
        
    print(f"\nDload dict download_thread_info_dict size: {len(download_thread_info_dict)}")
    print(f"Thread list size: {len(thread_list)}")
    print(f"\n> Channel Subscriptions [{len(video_channel_urls)}]: - - - - - - - - - - - <")

if len(thread_list) > 0:
    DloadProgressDisplay().start()
else:
    print('\nNothing scheduled for download\nUse -h for help')


# atexit: write_state_to_disk()
sys.exit(0) # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


# TODO
# H - - - - - - - 
# Add help with option info & examples
# Add -i option: DB info dump
# assess / sort channel function items

# M - - - - - - - 
# Add video name after URL in file - simplify inspection
# search for TODO add o this list

# L - - - - - - - 
# pause thread when tot_dload_band > 3.8Mb/s - EASY QUICK 
# Suppressing errors to screen and logging them in the logger


# To sort - - - - - - - 
# add debug thread info to DloadProgressDisplay - find uncaught finished downloads (Logger needs work!)
# add commit_dict_to_DB to EXIT HOOK to ensure persistence across exec runs (Logger needs work!)
# add cron option to skip interactive elements
#
# channel function
# when checking playlists for new content check 10,20,40,80,160,320 until caught up 
# update Dload.DLOAD_SESSION_DB at end - or DELETE or rename for history / end of week compiliation
# store this weeks new content in one folder for transfer to other devices
# get X back cataloque downloads per week - add setting


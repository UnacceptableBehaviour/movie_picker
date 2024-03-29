#! /usr/bin/env python

# Download new videos from YT channels
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

import sys

from pathlib import Path
import re
from pprint import pprint
import youtube_dl

# - - - simplest persistence code possible - - - -
import json
TEST = Path('/Volumes/Osx4T/05_download_tools_open_source/yt_dl/vtdl/test_load.json')
CHANNEL_DB_FILE = Path('/Volumes/Osx4T/05_download_tools_open_source/yt_dl/vtdl/channel_downloads.json')
DLOAD_ROOT = Path('/Volumes/Osx4T/05_download_tools_open_source/yt_dl/vtdl/chan')
#CHANNEL_DB_FILE = TEST
channel_DB = {}
download_targets_by_channel = {}

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

#sys.exit(0)

CHANNEL_VIDEOS_FILE = Path('./vtdl/vtdl_video_channel_list.txt')
video_channel_urls = get_urls_from_file(CHANNEL_VIDEOS_FILE)

print('>> video_channel_urls - - - - S')
for c in video_channel_urls:
    print(c)
print('>> video_channel_urls - - - - E')

sep_length = 100
print("\n" + "*" * sep_length + "\n")               # - - - - - - - - - - - - - - - - - 
print(' - - CURRENT STORED PLAYLISTS - - ') 
print("\n" + "*" * sep_length + "\n")               # - - - - - - - - - - - - - - - - - 

load_dict_data_from_DB(channel_DB, CHANNEL_DB_FILE) # - - - - - - - - - - - - - - - - -#
pprint(channel_DB.keys())                                                              #
# pprint(channel_DB)
# sys.exit(0)
NO_OF_ITEMS_PER_CHAN = 40                                                              #
delete = []
no_to_del = 2
delete_active = False       # TO DELETE THE LAST no_to_del ENTRIES set to True
playlist_items = f"1-{NO_OF_ITEMS_PER_CHAN}"                                           #
for channel, content in channel_DB.items():                                            #
    chan_url = f"https://www.youtube.com/c/{channel}/videos"                           #
    chan_title = f"> {channel} {chan_url} - - - - - - - <"                             #
    print('-' * len(chan_title))                                                       #
    print(f"> {channel} {chan_url} - - - - - - - <")                                   #
    print('-' * len(chan_title))                                                       #
    item_count = 0                                                                     #
    rev_content = dict(reversed(list(content.items())))                                # DUMP channel info
    delete = []
    for v_id, vid_data in rev_content.items():                                         #
        print(f"{v_id}: {(vid_data['pos']):04} {vid_data['title']}")                   #
        if item_count < no_to_del: delete.append(v_id)
        item_count += 1                                                                #        
        if item_count > NO_OF_ITEMS_PER_CHAN:                                          #
            print(v_id)
            pprint(vid_data)                                                           #
            for v in delete:
                if delete_active:
                    print(f"D - - -> c:{channel}-o-{v}<")
                    print(channel_DB[channel][v])
                    channel_DB[channel].pop(v)            
                    print('-')                    
            break                                                                      #
if delete_active: commit_dict_to_DB(channel_DB, CHANNEL_DB_FILE)
print("\n" + "*" * sep_length + "\n")               # - - - - - - - - - - - - - - - - -#

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


if '-c' in sys.argv:
    VID_ROOT = Path('/Volumes/Osx4T/05_download_tools_open_source/yt_dl/')
    TEST_CHAN_URL = 'https://www.youtube.com/c/DryBarComedy/videos'
    CHAN_KEY = TEST_CHAN_URL.replace('https://www.youtube.com/c/','').replace('https://www.youtube.com/user/','').replace('/videos','')
            
    #recent_chan_vid_info = get_playlist_update(TEST_CHAN_URL, {'playlist_items': '1-20', 'verbose':True}) # nor very verbosE!
    recent_chan_vid_info = get_playlist_update(channel_DB, CHAN_KEY, TEST_CHAN_URL, {'playlist_items': '1-20'})
    print('THESE videos are new addition to the channel')
    
    for k, video in recent_chan_vid_info.items():
        print(f"P:{(video['pos']):04} K:{k} {video['src_url']} - {video['title']}")


# youtube_dl info
#
# result['entries'][i]['webpage_url']     #url of video
# result['entries'][i]['title']           #title of video
# result['entries'][i]['uploader']        #username of uploader
# result['entries'][i]['playlist']        #name of the playlist
# result['entries'][i]['playlist_index']  #order number of video

# Entry
# {'_type': 'playlist',
#  'entries': [{'abr': 127.06,
#               'acodec': 'mp4a.40.2',
#               'age_limit': 0,
#               'average_rating': 4.9635315,
#               'categories': ['Education'],
#               'channel': 'MIT OpenCourseWare',
#               'channel_id': 'UCEBb1b_L6zDS3xTUrIALZOw',
#               'channel_url': 'https://www.youtube.com/channel/UCEBb1b_L6zDS3xTUrIALZOw',
#               'description': 'MIT 6.851 Advanced Data Structures, Spring 2012\n'
#                              'View the complete course: '
#                              'http://ocw.mit.edu/6-851S12\n'
#                              'Instructor: Erik Demaine\n'
#                              '\n'
#                              '"Persistence" - remembering all past versions of '
#                              'a data structure ("partial persistence"), being '
#                              'able to modify them - forking off new ones '
#                              '("full persistence"), and  merging different '
#                              'versions into one ("confluent persistence").\n'
#                              '\n'
#                              'License: Creative Commons BY-NC-SA\n'
#                              'More information at http://ocw.mit.edu/terms\n'
#                              'More courses at http://ocw.mit.edu',
#               'dislike_count': 19,
#               'display_id': 'T0yzrZL1py0',
#               'duration': 5023,
#               'ext': 'webm',
#               'extractor': 'youtube',
#               'extractor_key': 'Youtube',
#               'format': '247 - 1280x720 (720p)+140 - audio only (tiny)',
#               'format_id': '247+140',
#               'formats': [{'abr': 50.067,
#                            'acodec': 'opus',
#                            'asr': 48000,
#                            'container': 'webm_dash',
#                            'downloader_options': {'http_chunk_size': 10485760},
#                            'ext': 'webm',
#                            'filesize': 31438931,
#                            'format': '249 - audio only (tiny)',
#                            'format_id': '249',
#                            'format_note': 'tiny',
#                            'fps': None,
#                            'height': None,
#                            'http_headers': {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#                                             'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
#                                             'Accept-Encoding': 'gzip, deflate',
#                                             'Accept-Language': 'en-us,en;q=0.5',
#                                             'User-Agent': 'Mozilla/5.0 '
#                                                           '(Windows NT 10.0; '
#                                                           'Win64; x64) '
#                                                           'AppleWebKit/537.36 '
#                                                           '(KHTML, like Gecko) '
#                                                           'Chrome/74.0.3713.3 '
#                                                           'Safari/537.36'},
#                            'protocol': 'https',
#                            'quality': 0,
#                            'tbr': 50.067,
#                            'url': 'https://r5---sn-cu-cime7.googlevideo.com/videoplayback?expire=1627163547&ei=Ozf8YMGzGda_mLAPzYi7-AE&ip=146.200.4.51&id=o-AB4TcEni60C1mVJG-1sxbLXOOU9idssMIZqhVvANgWNQ&itag=249&source=youtube&requiressl=yes&mh=3h&mm=31%2C29&mn=sn-cu-cime7%2Csn-cu-c9il&ms=au%2Crdu&mv=m&mvi=5&pl=25&initcwndbps=1013750&vprv=1&mime=audio%2Fwebm&ns=I_lhVItqsCVhuli_0uCNtvgG&gir=yes&clen=31438931&dur=5023.461&lmt=1541987094373032&mt=1627141724&fvip=5&keepalive=yes&fexp=24001373%2C24007246&c=WEB&txp=5411222&n=yskZJLFstthnB5&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cvprv%2Cmime%2Cns%2Cgir%2Cclen%2Cdur%2Clmt&sig=AOq0QJ8wRQIgZJk5vKcuJE_wgTCpio5mzO-MEFIr8IOJEpOUgWOyrksCIQDOCpgGhfjWRKVM0WvFSTCnUwdfWTRufnCdEWXxduU2qA%3D%3D&lsparams=mh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Cinitcwndbps&lsig=AG3C_xAwRQIhANII7bZEZZRm8K1etj0jGVmm8P8HWYNhMhVvA7F0Hf9SAiBWt8-YGozy6damrciVha7ZQ10MABib9pwBZYzMh4hJcQ%3D%3D',
#                            'vcodec': 'none',
#                            'width': None},

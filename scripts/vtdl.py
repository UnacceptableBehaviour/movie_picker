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

def load_dict_data_from_DB(cDB):
    '''
    load stored channel info from text file - json format
    '''

    if CHANNEL_DB_FILE.exists():
        with open(CHANNEL_DB_FILE, 'r') as f:
            json_db = f.read()
            db = json.loads(json_db)
            print(f"Channel database LOADED ({len(db)})")

        for i in db.keys():
            cDB[i] = db[i]

        print(f"Channel database json > objects COMPLETE ({len(cDB)})")
        return 0

    else:
        db = {}  # create a blank file
        commit_dict_to_DB(db)
        return -1


def commit_dict_to_DB(commit_db):
    '''
    commit channel info to text file - json format
    '''

    with open(CHANNEL_DB_FILE, 'w') as f:
        #pprint(commit_db)
        db_as_json = json.dumps(commit_db)
        f.write(db_as_json)


# load_dict_data_from_DB(channel_DB)
# pprint(channel_DB)

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

def get_video_dict_from_channel(videos_url, quiet_mode=True, reverseMode=True):
    return get_playlist(videos_url, quiet_mode, reverseMode)

# TODO deprecated use playlist_update
def get_playlist(pl_url, quiet_mode=True, reverseMode=False):
    print(f"Getting PL from: {pl_url}")
    play_list = {}
    play_list_entries = []
    channel_name = ''

    ydl = youtube_dl.YoutubeDL({'quiet':quiet_mode})

    with ydl:
        #result = ydl.extract_info(pl_url, download=False, { #We just want to extract the info
        result = ydl.extract_info(pl_url, download=False, extra_info={
                #'playliststart': 2,
                #'playlistend':   4,
                'playlist_items': '2,4,7-9,11'
            }) 
            # playliststart:     Playlist item to start at.
            # playlistend:       Playlist item to end at.
            # playlist_items:    Specific indices of playlist to download.
            # playlistreverse:   Download playlist items in reverse order.
            # playlistrandom:    Download playlist items in random order.
        # 'n_entries': 10,
        # 'playlist_index': 8,
        # 'playlist': 'David Sinclair - Videos',
        # 'playlist_id': 'UCwD5YYkbYmN2iFHON9FyDXg',
        # 'channel': 'David Sinclair',
        # 'channel_id': 'UCwD5YYkbYmN2iFHON9FyDXg',
        # 'channel_url': 'https://www.youtube.com/channel/UCwD5YYkbYmN2iFHON9FyDXg',
        # 'tags': 'Lifespan','aging','what is aging','how do we age'
        # 'webpage_url': 'https://www.youtube.com/watch?v=wD8reCw3Kls',
        # 'webpage_url_basename': 'wD8reCw3Kls',
        # 'id': 'wD8reCw3Kls',
        # 'subtitles': {'en': [{'ext': 'srv1',
        #                       'url': 'https://www.youtube.com/api/timedtext?v=wD8reCw3Kls&caps=asr&xoaf=5&hl=en&ip=0.0.0.0&ipbits=0&expire=1665365119&sparams=ip%2Cipbits%2Cexpire%2Cv%2Ccaps%2Cxoaf&signature=6499802713B9F79238D8BC253603B93BD8BB251E.944F5FCFA5CAD67518061EF0C50636C305BEE844&key=yt8&lang=en&fmt=srv1'},
        # 'thumbnails': [{'height': 94,
        #                  'id': '0',
        #                  'resolution': '168x94',
        #                  'url': 'https://i.ytimg.com/vi/wD8reCw3Kls/hqdefault.jpg?sqp=-oaymwEbCKgBEF5IVfKriqkDDggBFQAAiEIYAXABwAEG&rs=AOn4CLD1pYNbOiTSzXope4ecIB8SyHM3pA',
        #                  'width': 168},    
        #
        # extracting partial PL
        # https://askubuntu.com/questions/1074697/how-can-i-download-part-of-a-playlist-from-youtube-with-youtube-dl
    
        if 'entries' in result:
            if reverseMode:
                result['entries'].reverse()
            # Can be a playlist or a list of videos
            videos = result['entries']           # list of dict            

            #loops entries to grab each video_url
            for i, video in enumerate(videos):
                # see Osx4T/05_download_tools_open_source/yt_dl/vtdl/video.json
                # for object info
                print(f"{(i+1):03}: K:{video['webpage_url_basename']} {video['webpage_url']} - {video['title']}")   # {i:03} left pad n with 0's 3 digits
                play_list[video['webpage_url_basename']] = { 'src_url': video['webpage_url'],
                                                             'pos': i,
                                                             'idx': video['playlist_index'],
                                                             'title': video['title'],
                                                             'downloaded': False 
                                                             }
                play_list_entries.append(video['n_entries']) # debug this should all be the same
                channel_name = video['webpage_url_basename']
                
            print(f"Channel: {channel_name} . . entries:")
            pprint(play_list_entries)
            
    return play_list

#
#
# # # # #
def get_playlist_update(cDB, chan_key, pl_url, ydl_opts_pass={}):
    print(f"Getting PL from: {pl_url}")
    play_list = {}
    new_vid_entries = {}
    
    ydl_opts = {'quiet':True,
                'playlistreverse':True }    
    ydl_opts.update(ydl_opts_pass)    
    pprint(ydl_opts)

    ydl = youtube_dl.YoutubeDL(ydl_opts)

    with ydl:
        result = ydl.extract_info(pl_url, download=False) 
    
        if 'entries' in result:
            videos = result['entries']           # list of dict            

            for i, video in enumerate(videos):
                # see Osx4T/05_download_tools_open_source/yt_dl/vtdl/video.json for object info
                print(f"{(i+1):03}: K:{video['webpage_url_basename']} {video['webpage_url']} - {video['title']}")   # {i:03} left pad n with 0's 3 digits
                
                play_list[video['webpage_url_basename']] = { 'src_url': video['webpage_url'],
                                                             'pos': i,
                                                             'idx': video['playlist_index'],
                                                             'title': video['title'],
                                                             'downloaded': False 
                                                             }

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

#sys.exit(0)

CHANNEL_VIDEOS_FILE = Path('./vtdl/vtdl_video_channel_list.txt')

video_channel_urls = get_urls_from_file(CHANNEL_VIDEOS_FILE)
video_channel_keys = []
video_list = []

print('>> video_channel_urls - - - - S')
for c in video_channel_urls:
    print(c)
print('>> video_channel_urls - - - - E')

sep_length = 100
print("\n" + "*" * sep_length + "\n")               # - - - - - - - - - - - - - - - - - - - - - - - - 
print(' - - CURRENT STORED PLAYLISTS - - ') 
print("\n" + "*" * sep_length + "\n")               # - - - - - - - - - - - - - - - - - - - - - - - - 

load_dict_data_from_DB(channel_DB)
NO_OF_ITEMS_PER_CHAN = 5
for channel, content in channel_DB.items():
    chan_url = f"https://www.youtube.com/c/{channel}/videos"
    print(f"> {channel} {chan_url} - - - - - - - <")
    item_count = 0
    rev_content = dict(reversed(list(content.items())))
    for v_id, vid_data in rev_content.items():
        print(f"{v_id}: {(vid_data['pos']):04} {vid_data['title']}")        
        item_count += 1
        if item_count > NO_OF_ITEMS_PER_CHAN:
            pprint(vid_data)
            break

print("\n" + "*" * sep_length + "\n")               # - - - - - - - - - - - - - - - - - - - - - - - - 

# r - reload
# u - update DB
if '-r' in sys.argv:
    for url in video_channel_urls:
        print(f"URL: {url}")
        #print(url.replace('https://www.youtube.com/c/','').replace('/videos',''))
        channel_key = url.replace('https://www.youtube.com/c/','').replace('https://www.youtube.com/user/','').replace('/videos','')
        print(f"channel_key: {channel_key}")
        video_channel_keys.append(channel_key)
        video_dict = None
        try:
            if channel_key not in channel_DB:
                video_dict = get_video_dict_from_channel(url, quiet_mode=False, reverseMode=True)
        except BaseException as e:
            print('> - - - - - BALLS')
            pprint(e)
        finally:
            print('> - - - - - SAVING DATA')
            if ('-u' in sys.argv) and video_dict:
                if channel_key in channel_DB:
                    channel_DB[channel_key].update(video_dict)
                    # TODO - add difference to download list
                else:
                    channel_DB[channel_key] = video_dict
                    # TODO - add to download list
                commit_dict_to_DB(channel_DB)
                
        print(f"Downloaded video info for {channel_key}")
        pprint(video_dict)
        # for k, video in video_dict.items():
        #     print(f"\n{k}")
        #     pprint(video)
        
        print("> - - - - - - - Channel END")





VID_ROOT = Path('/Volumes/Osx4T/05_download_tools_open_source/yt_dl/')
TEST_CHAN_URL = 'https://www.youtube.com/c/DryBarComedy/videos'
CHAN_KEY = TEST_CHAN_URL.replace('https://www.youtube.com/c/','').replace('https://www.youtube.com/user/','').replace('/videos','')
        
#recent_chan_vid_info = get_playlist_update(TEST_CHAN_URL, {'playlist_items': '1-20', 'verbose':True}) # nor very verbosE!
recent_chan_vid_info = get_playlist_update(channel_DB, CHAN_KEY, TEST_CHAN_URL, {'playlist_items': '1-20'})
print('THESE videos are new addition to the channel')

for k, video in recent_chan_vid_info.items():
    print(f"P:{(video['pos']):04} K:{k} {video['src_url']} - {video['title']}")

# comparison update - yield missing items from updates playlists & download them
# if '-u' in sys.argv:
#     commit_dict_to_DB(channel_DB)


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

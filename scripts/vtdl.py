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


from pathlib import Path
import re
from pprint import pprint
import youtube_dl


def get_urls_from_file(filename):
    with open(filename, 'r') as f:
        content = f.read()

    url_list = []
    for line in content.split('\n'):
        if len(line.strip()) == 0: continue
        if re.findall('^#', line): continue
        url_list.append(line)   # maybe add regex to check valid url

    return url_list

def get_video_list_from_channel(videos_url):
    get_playlist(videos_url, True, True)


def get_playlist(pl_url, quiet_mode=True, reverseMode=False):
    play_list = pl_url
    print(f"Getting PL from: {pl_url}")

    ydl = youtube_dl.YoutubeDL({'quiet':quiet_mode})

    with ydl:
        result = ydl.extract_info(pl_url, download=False) #We just want to extract the info

        #pprint(result)
        #if result['_type'] == 'playlist':

        if 'entries' in result:
            if reverseMode:
                result['entries'].reverse()
            # Can be a playlist or a list of videos
            video = result['entries']           # list of dict
            play_list = []

            #loops entries to grab each video_url
            for i, item in enumerate(video):
                # print(f"= = = i: {i}")
                # print(f"= = = = item = = =S \ ")
                # #pprint(item)
                # print(f"item['webpage_url']: {item['webpage_url']}")
                # print(f"index - item['title']: {(i+1):03} - {item['title']}")   # {i:03} left pad n with 0's 3 digits
                print(f"{item['webpage_url']} - {(i+1):03} - {item['title']}")   # {i:03} left pad n with 0's 3 digits
                # print(f"item['uploader']: {item['uploader']}")
                # print(f"item['playlist']: {item['playlist']}")
                # print(f"item['playlist_index']: {item['playlist_index']}")
                # #print(f"item['']: {item['']}")
                # print(f"= = = = item = = =E / ")
                video = result['entries'][i]
                play_list.append(item['webpage_url'])

            # print('get_playlist - - dbg S')
            # print(f"reverseMode: {reverseMode}")
            # pprint(play_list)
            # if reverseMode:
            #     play_list.reverse()
            # print('-')
            # pprint(play_list)
            # print('get_playlist - - dbg E')

    return play_list

CHANNEL_VIDEOS_FILE = Path('./vtdl/vtdl_video_channel_list.txt')
channel_video_downloads = {}


video_channel_urls = get_urls_from_file(CHANNEL_VIDEOS_FILE)
video_channel_keys = []
video_list = []

for url in video_channel_urls:
    #print(f"{url}")
    #print(url.replace('https://www.youtube.com/c/','').replace('/videos',''))
    channel_key = url.replace('https://www.youtube.com/c/','').replace('/videos','')
    video_channel_keys.append(channel_key)
    video_list = get_video_list_from_channel(url)
    channel_video_downloads[channel_key] = {}
    for video in video_list:
        print(url.replace('https://www.youtube.com/watch?v=',''))
    break
    

pprint(video_channel_keys)
print(' - - - - - - - ')
pprint(video_list)


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

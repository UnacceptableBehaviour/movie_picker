#! /usr/bin/env python

# Download video URLs

# setup
# > curl https://raw.githubusercontent.com/UnacceptableBehaviour/movie_picker/master/scripts/ytdl.py > ytdl.py
# > chmod +x ytdl.py
# > python3 -m venv venv
# > . venv/bin/activate           # or source venv/bin/activate
# > pip install youtube_dl
# > ./ytdl.py ./20210811_fun_stuff.txt      # dowload all URLs in text file
#                       ^
#                     place a list of video urls in a text file
#
# File: 20210811_fun_stuff.txt
# # this is a comment - will be ignored
# # Geometric DL lectures
# https://www.youtube.com/watch?v=PtA0lg_e5nA&list=PLn2-dEmQeTfQ8YVuHBOvAhUlnIPYxkeu3
# # Wah?
# https://www.youtube.com/watch?v=MmG2ah5Df4g
# # Growing food PL
# https://www.youtube.com/c/UrbanFarmerCurtisStone/videos
#
# Files will be store in a directory of the same name as the text file (no extension) in
# target_base_dir = same directory as the text file
#
# downloads will be numbered in the order they are in the list - or decompressed playlist

# NEXT - TODO
# how to get feedback from the process - parse it's stdout ?
#   NO there a callback HOOK use that to get progress (& download speed)
#
# get DL speed - kill it if it drops below threshold
#   then restart it

# More on youtube-dl
# https://www.programcreek.com/python/example/98358/youtube_dl.YoutubeDL

import sys                          # argv - cli args
from pathlib import Path
import itertools                    # flatten

# Use a Pool:
import multiprocessing.dummy
import subprocess
import os
import re

import youtube_dl
from pprint import pprint

# def is_play_list(url):
#     ytdl = youtube_dl.YoutubeDL() #{'outtmpl': '%(id)s%(ext)s', 'quiet':True,})
#
#     result = ytdl.extract_info(url, download=False) # just video meta data
#
#     #pprint(result)
#     return ((result['_type'] == 'playlist'), result)


# youtub-dl pararmeters
arr = [
    {'vpath': 'example/%(title)s.%(ext)s', 'url': 'https://www.youtube.com/watch?v=BaW_jenozKc'},
    {'vpath': 'example/%(title)s.%(ext)s', 'url': 'http://vimeo.com/56015672'},
    {'vpath': '%(playlist_title)s/%(title)s-%(id)s.%(ext)s',
     'url': 'https://www.youtube.com/playlist?list=PLLe-WjSmNEm-UnVV8e4qI9xQyI0906hNp'},
]

# def download(v):
#     subprocess.check_call([
#         'echo', 'youtube-dl',
#         '-u', email, '-p', password,
#         '-o', v['vpath'], '--', v['url']])

def download(v):
    subprocess.check_call([
        'youtube-dl', '--no-playlist',
        '-o', v['vpath'], '--', v['url']])

# current CLI command execute
# youtube-dl
    # -o '/Volumes/Osx4T/05_download_tools_open_source/yt_dl/20210705_quick_grab/%(playlist)s/%(playlist_index)s #%(autonumber)03d - %(title)s.%(ext)s'
    # -a ./20210705_quick_grab/20210705_quick_grab.txt

# - - - - Pseudo / Steps
# load text file of links - [TODO - how to get list from favourites]
# create directory based on filename
# number each file based on position in the file
# dload into directory

# flatten stable recursive
def flatten_stable(nested_arrays, d=0):
    ret_list = []
    for i in nested_arrays:
        #tab = '  '*d
        #print(f"{tab}{d}: {i} {nested_arrays}")
        if type(i) == list:
            ret_list = ret_list + flatten_stable(i, d+1)
        else:
            ret_list.append(i)
    return ret_list

def get_playlist(pl_url, quiet_mode=True):
    play_list = pl_url
    print(f"Getting PL from: {pl_url}")

    ydl = youtube_dl.YoutubeDL({'quiet':quiet_mode})

    with ydl:
        result = ydl.extract_info(pl_url, download=False) #We just want to extract the info

        #pprint(result)
        #if result['_type'] == 'playlist':

        if 'entries' in result:
            # Can be a playlist or a list of videos
            video = result['entries']           # list of dict
            play_list = []

            #loops entries to grab each video_url
            for i, item in enumerate(video):
                # print(f"= = = i: {i}")
                # print(f"= = = = item = = =S \ ")
                # #pprint(item)
                print(f"item['webpage_url']: {item['webpage_url']}")
                print(f"item['title']: {item['title']}")
                # print(f"item['uploader']: {item['uploader']}")
                # print(f"item['playlist']: {item['playlist']}")
                # print(f"item['playlist_index']: {item['playlist_index']}")
                # #print(f"item['']: {item['']}")
                # print(f"= = = = item = = =E / ")
                video = result['entries'][i]
                play_list.append(item['webpage_url'])

            # print('get_playlist - - dbg S')
            # pprint(play_list)
            # print('get_playlist - - dbg E')

    return play_list


def get_urls_from_file(filename):
    with open(filename, 'r') as f:
        content = f.read()

    url_list = []
    for line in content.split('\n'):
        if len(line.strip()) == 0: continue
        if re.findall('^#', line): continue
        url_list.append(line)   # maybe add regex to check valid url

    return url_list


def append_commented_urls_to_file(filepath, file_list):
    text_content = ''
    for line in file_list:
        text_content = text_content + f"# {line}\n"

    text_content = text_content + '# -'
    print(text_content)

    with open(filepath, 'a') as f:
        f.write(text_content)



if __name__ == '__main__':

    downloads_filename = None
    # get file from command line
    if len(sys.argv) > 1 and Path(sys.argv[1]).exists():
        downloads_filename = Path(sys.argv[1])

        file_urls = get_urls_from_file(downloads_filename)
        pprint(file_urls)

        replace_targets = {}
        for possible_play_list in file_urls:

            expanded_into_urls = get_playlist(possible_play_list, False)

            if possible_play_list != expanded_into_urls:
                replace_targets[possible_play_list] = expanded_into_urls
                # replace play list with expanded single items

        print('replace_targets - - dbg S')
        pprint(replace_targets)
        print('replace_targets - - dbg E')

        for pl, pl_items in replace_targets.items():
            # print(f"pl - {pl}")
            # print(f"file_urls.index(pl) - {file_urls.index(pl)}")
            # print(f"pl_items - {pl_items}")
            file_urls[file_urls.index(pl)] = pl_items
            file_urls = flatten_stable(file_urls) # - return out of order list

        # print('file_urls:')
        # pprint(file_urls)

    else:
        print(Path(__file__).name)
        print(f"\n*** Usage:\n\t> {Path(__file__).name} url_plalists.txt \n\tTarget filename required")
        sys.exti(0)

    append_commented_urls_to_file(downloads_filename, file_urls)

    target_base_dir = downloads_filename.parent
    target_dir = Path(target_base_dir,downloads_filename.name.split('.')[0]) # url_file name w/o extension

    # create directory for downloads
    try:
        Path.mkdir(target_dir, parents=True)
    except Exception:
        print(f"** WARNING ** target_dir already created\n{target_dir}")
        yn = input('Continue (y)/n\n')
        if yn.strip().lower() == 'n': sys.exit(0)

    arr = []
    play_list_pos = 0
    for line in file_urls:
        play_list_pos += 1
        print(Path(target_dir,str(play_list_pos).zfill(2)))
        entry = {'vpath': f"{Path(target_dir,str(play_list_pos).zfill(2))} - %(title)s.%(ext)s", 'url': f"{line}" }
        print(entry)
        arr.append(entry)

    p = multiprocessing.dummy.Pool(8) # number of threads
    p.map(download, arr)


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

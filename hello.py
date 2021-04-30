#! /usr/bin/env python

# buil a simple movie DB using
# https://www.google.com/search?q=list+of+movies+w%2F+expired+copyrights&oq=list+of+movies+w%2F+expired+copyrights&aqs=chrome..69i57.10974j0j7&sourceid=chrome&ie=UTF-8

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
from flask import Flask, render_template, request, jsonify, make_response
app = Flask(__name__)
import json                         # JSON tools

# debug
from pprint import pprint           # giza a look
import inspect                      # inspect.getmembers(object[, predicate])



#        dir        file
# this causes __init_.py to execute
from moviepicker import MMediaLib,MMedia,REVERSE,FORWARD
from moviepicker import PICKLED_MEDIA_LIB_FILE_V2_TIMEBOX,PICKLED_MEDIA_LIB_FILE_V2_F500,PICKLED_MEDIA_LIB_FILE_REPO
from moviepicker import PICKLED_MEDIA_LIB_FILE_OSX4T, KNOWN_PATHS
from pathlib import Path
import random
import re                                                               # regex
import socket
import copy

import sys
from collections import Counter

import subprocess
from time import sleep
import vlc
from moviepicker import vlc_http, kill_running_vlc    # needs an instance of vlc running

vlc_http_channel = None
movie_process = None
media_lib = None


# load info if 1st time round
# media_lib = MMediaLib(PICKLED_MEDIA_LIB_FILE_V2_TIMEBOX)
#
# check for available discs and merge them
#
# if MMediaLib.exists(PICKLED_MEDIA_LIB_FILE_V2_F500):
#     media_lib.join(MMediaLib(PICKLED_MEDIA_LIB_FILE_V2_F500))
default_library_name = 'medialib2.pickle'

volume_checklist = KNOWN_PATHS
test_mode_library_name = Path('/Users/simon/a_syllabus/lang/python/movie_picker/movies/__media_data2/medialib2.pickle')

import platform
running_os = platform.system()
# AIX: 'aix', Linux:'linux', Windows: 'win32', Windows/Cygwin: 'cygwin', macOS: 'darwin'
running_os_release = platform.release()

# hostname = socket.gethostname()
# print("Your Computer Name is:" + hostname)
# IPAddr = socket.gethostbyname(hostname)
# print("Your Computer IP Address is:" + IPAddr)
# print(f"OS: {running_os} - {running_os_release}")
IPAddr = '192.168.1.13' # TODO FIX - aBOVE
hostname = 'dtk.health'

if IPAddr == '192.168.1.13':    # local - osx box
    REMOTE_LINUX = Path('/Volumes/Home Directory/MMdia/__media_data2/medialib2.pickle')

    # vcl = []
    # for path in volume_checklist:
    #     full_path = Path('Volumes', path)
    #     vcl.append(full_path) if full_path.exists()
    # load medialibs & merge TODO

    for media_path in volume_checklist:
        if media_path.exists():
            media_lib = MMediaLib(media_path)
            #media_lib = MMediaLib(PICKLED_MEDIA_LIB_FILE_V2_F500)
            #media_lib = MMediaLib(PICKLED_MEDIA_LIB_FILE_REPO)
            #media_lib = MMediaLib(REMOTE_LINUX)
            #media_lib.rebase_media_DB('/Volumes/FAITHFUL500/','/Volumes/Home Directory/MMdia/')
            #media_lib = MMediaLib(PICKLED_MEDIA_LIB_FILE_OSX4T)
            if media_path == PICKLED_MEDIA_LIB_FILE_OSX4T:
                media_lib.rebase_media_DB('/Volumes/meep/temp_delete/','/Volumes/Osx4T/')

    # local disc - small library - export FLASK_ENV=development
    #media_lib = MMediaLib(test_mode_library_name)   < DOESNT exit & files too small to recreate!

elif IPAddr == '192.168.1.16':  # remote - linux box
    LOCAL_LINUX = Path('/home/pi/MMdia/','__media_data2/medialib2.pickle')
    media_lib = MMediaLib(LOCAL_LINUX)
    media_lib.rebase_media_DB('/Volumes/FAITHFUL500/','/home/pi/MMdia/')

if not media_lib:
    print("EXITIING - NO media libraries were found")
    sys.exit(0)

LOCAL_IMAGE_CACHE = Path('./static/covers')
LOCAL_IMAGE_CACHE.mkdir(parents=True, exist_ok=True)

media_lib.cache_images_locally(LOCAL_IMAGE_CACHE)
print(f"LOADED: {len(media_lib)}")
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# users / prefs proto - move into module
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
USER_DB_FILE = Path('./moviepicker/userDB.json')
user_device_DB = {}

# TODO mov into exceptions
class UserUuidMismatch(Exception): #UserUuidMismatch(MMediaLibError):
    '''could not update user with prefs_info UUID does NOT match'''
    pass

class UserPrefs:
    fingerprints = {}

    def __init__(self, uuid, name=None, info={}):
        self.prefs_info = {'uuid':'uu_id',
                           'name':'user_name',
                           'fingerprints':[],
                           'short_list':[],
                           'seen_list':[],
                           'ni_list':[],
                           'ratings':{},
                           'prefs_genre': {'neg':[],
                                          #"genres_all":["History","War","Sci-Fi","Music","Sport","Romance","Adventure","Action","Mystery","Thriller","Documentary","Musical","Biography","News","Fantasy","Animation","Family","Crime","Drama","Comedy","Horror","Western"],
                                          'pos':[]},
                           'prefs_actors':{'neg':[],
                                          'pos':[]},
                           'current_user': False
                           }
        self.prefs_info.update(info)
        print(type(info))
        print(type(self.prefs_info))

        self.prefs_info['uuid'] = uuid
        if name: self.prefs_info['name'] = name

    # deprecated - find uses - change TODO
    def get_prefs(self):
        return self.prefs_info

    def update_prefs(self, new_prefs):
        if new_prefs['uuid'] == self.prefs_info['uuid']:
            print("UserPrefs.update_prefs succeed")
            self.prefs_info.update(new_prefs)
        else:
            raise UserUuidMismatch

    # @property
    # def prefs_info(self):
    #     return self.prefs_info
    #
    # @prefs_info.setter
    # def prefs_info(self, ):
    #     pass



    def uuid(self):
        return self.prefs_info['uuid']

    @property
    def name(self):
        return self.prefs_info['name']

    @name.setter
    def name(self, name):
        self.prefs_info['name'] = name


    def add_fingerprint(self, fingerprint):
        if fingerprint not in self.prefs_info['fingerprints']:
            self.prefs_info['fingerprints'].append(fingerprint)

    #
    # TODO adapt interface so its update on change - also bake in order based on ratings
    #
    def filter_list(self, movie_list):
        scored_and_sorted_movies = []
        #print(f"UserPrefs.filter_list: {len(movie_list)}")
        #movie_list[20]['prefScore'] = 10000
        #pprint( movie_list[20] )
        for m in movie_list:
            m['prefScore'] = 10000
            # add 100 pointe per positive genre match in movie
            pos = len(list( set(m['genres']) & set(self.prefs_info['prefs_genre']['pos']) )) * 500
            neg = len(list( set(m['genres']) & set(self.prefs_info['prefs_genre']['neg']) )) * 500
            m['prefScore'] += pos
            m['prefScore'] -= neg
            if m['id'] in self.prefs_info['seen_list']: m['prefScore'] -= 250
            if m['id'] in self.prefs_info['ni_list']: m['prefScore'] -= 750

        scored_and_sorted_movies  = sorted(movie_list, key=lambda k: k['prefScore'], reverse=True)

        # for m in scored_and_sorted_movies :
        #     print(f"score:{m['prefScore']} - {m['file_title']}")


        return scored_and_sorted_movies
        # allocate score of 10K points as baseline
        # for each genre neg - 100 points
        # for each genre pos + 100 points






def load_dict_data_from_DB(uDB):
    '''
    load user & device data from text file - json format
    '''

    if USER_DB_FILE.exists():
        with open(USER_DB_FILE, 'r') as f:
            json_db = f.read()
            db = json.loads(json_db)
            print(f"USER database LOADED ({len(db)})")

        for i in db.keys():
            uDB[i] = UserPrefs(i,info=db[i])

        print(f"USER database json > objects COMPLETE ({len(uDB)})")
        return 0

    else:
        db = {}  # create a blank file
        commit_dict_to_DB(db)
        return -1



def commit_dict_to_DB(commit_db):
    '''
    commit user & device data to text file - json format
    '''
    db = {}
    for i in commit_db.keys():
        db[i] = commit_db[i].get_prefs()

    with open(USER_DB_FILE, 'w') as f:
        #pprint(db)
        db_as_json = json.dumps(db)
        f.write(db_as_json)


load_dict_data_from_DB(user_device_DB)

import uuid
print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - JSON DB - S")
new_uuid = str(uuid.uuid4())
new_uuid = list(user_device_DB.keys())[3]     # dont add any more users!
current_user = None
print("users:")
for k in user_device_DB.keys():
    user = user_device_DB[k]
    print(f"u: {user.uuid()} n:{user.name} t:{type(user)}")

print(f"New UUID: {new_uuid}")

if new_uuid not in user_device_DB:
    u = UserPrefs(new_uuid, f"U{len(user_device_DB.keys())}")
    user_device_DB[u.uuid()] = u
    pprint(user_device_DB)
    commit_dict_to_DB(user_device_DB)
else:
    print(f"FOUND USER: {new_uuid}")
    pprint(user_device_DB[new_uuid].get_prefs())
    # user_device_DB[new_uuid].prefs_info['current_user'] = True
    # commit_dict_to_DB(user_device_DB)

for usr_id,usr in user_device_DB.items():
    print(f"u: {usr_id} n:{usr.name} t:{type(usr)} current:{usr.prefs_info['current_user']}")
    if usr.prefs_info['current_user']: current_user = usr



print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - JSON DB - E")


#commit_dict_to_DB(user_device_DB)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


# each app.route is an endpoint

#<a href="{{url_for('/', user_id=u['user_uuid'])}}">{{ u['usr'] }}</a>

#@app.route('/<user_id>', methods=["GET", "POST"])
@app.route('/', methods=["GET", "POST"])
def movie_gallery_home():
    global current_user
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    # reset vlc process                                                                             #
    #                                                                                               #
    # catch this in JS land - if multiple devices connect                                           #
    # TODO - think through multiuser use cases                                                      #
    # back to selections menu - kill movie window                                                   #
    global movie_process                                                                            #
    global vlc_http_channel                                                                         #
                                                                                                    #
    # TODO - is this used anymore? or is it just kill_running_vlc()                                 #
    # REMOVE?                                                                                       #
    if movie_process:                                                                               #
        # record movie and place in movie - if reselected restart where left off!! MVTODO           #
        movie_process.kill()                                                                        #
        movie_process = None                                                                        #
                                                                                                    #
    kill_running_vlc()                                                                              #
    vlc_http_channel = None                                                                         #
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #


    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -#
    # processing incoming msgs                                                                     #
    # https://stackoverflow.com/questions/10434599/get-the-data-received-in-a-flask-request
    sort_by = 'year'
    chosen_sort = {
        'year':     media_lib.sorted_by_year,
        'rating':   media_lib.sorted_by_rating,
        'title':    media_lib.sorted_by_title,
        'added':    media_lib.sorted_by_rating                   # TODO - return to correct sort
        #'added':    media_lib.sorted_by_most_recently_added     # TODO - fix this sort
    }

    print(f"\nmovie_gallery_home: - - - - - - - - debug - - - - - - - - - - - - - - - - S\n")          #
    if request.method == 'POST':                                                                   #
        if request.is_json:
            print("movie_gallery_home: request.method == 'POST_JSON'")
            settings = request.get_json() # parse JSON into DICT
            pprint(settings)

            if settings != None  and 'prefs_info' in settings:
                try:
                    user_device_DB[settings['prefs_info']['uuid']].update_prefs(settings['prefs_info'])
                    commit_dict_to_DB(user_device_DB)
                    # return all good
                    return json.dumps({}), 201 # created
                except (UserUuidMismatch, KeyError):
                    # return - couldnt find user_info!??
                    return json.dumps({}), 404

            if settings != None  and 'new_id' in settings:  # user id
                try:
                    last_user = current_user
                    current_user = user_device_DB[settings['new_id']]
                    current_user.prefs_info['current_user'] = True
                    if current_user != last_user: last_user.prefs_info['current_user'] = False
                    commit_dict_to_DB(user_device_DB)
                    return json.dumps({}), 201 # user changed
                except KeyError:
                    # return - couldnt find user_info!??
                    return json.dumps({}), 404

            if settings != None  and 'mov_id_prefs' in settings:
                print("'mov_prefs' in settings - - - S")
                button = re.sub('mov_prefs_','', settings['button']) # which movie pref button?
                mov_id = settings['mov_id_prefs']
                rating = settings['rating']
                print(f"mov_prefs clicked: {button}")
                if button == 'sl':
                    if mov_id not in current_user.prefs_info['short_list']: current_user.prefs_info['short_list'].append(mov_id)
                    commit_dict_to_DB(user_device_DB)
                    return json.dumps({}), 201
                elif button == 'ni':
                    if mov_id not in current_user.prefs_info['ni_list']: current_user.prefs_info['ni_list'].append(mov_id)
                    commit_dict_to_DB(user_device_DB)
                    return json.dumps({}), 201
                elif button == 'rate':
                    if (rating != -1) and (mov_id not in current_user.prefs_info['ratings']):
                        current_user.prefs_info['ratings'][mov_id] = rating
                        commit_dict_to_DB(user_device_DB)
                        return json.dumps({}), 201
                    return json.dumps({}), 404
                elif button == 'seen':
                    if mov_id not in current_user.prefs_info['seen_list']: current_user.prefs_info['seen_list'].append(mov_id)
                    commit_dict_to_DB(user_device_DB)
                    return json.dumps({}), 201
                print("'mov_prefs' in settings - - - E")

        else:
            print("movie_gallery_home: request.method == 'POST' - NOT json ")

            print("\nrequest.args - - - - <")
            pprint(request.args)
            for key in request.args.keys():                                                            #
                print(f"{key} - {request.args[key]}")                                                  #

            print("\nrequest.form - - - - <")
            pprint(request.form)
            # cycle through form items
            for key, val in request.form.items():
                print(f"{key} - {val}")
                if 'change_genre' == key:       # easier to do this in JS land and post new prefs No?
                    selected_genre = request.form['change_genre']
                    if selected_genre in current_user.prefs_info['prefs_genre']['neg']:
                        # del from neg move to pos
                        current_user.prefs_info['prefs_genre']['neg'].remove(selected_genre)
                        current_user.prefs_info['prefs_genre']['pos'].append(selected_genre)

                    elif selected_genre in current_user.prefs_info['prefs_genre']['pos']:
                        # del from pos move to don't care (not in either)
                        current_user.prefs_info['prefs_genre']['pos'].remove(selected_genre)

                    elif request.form['change_genre'] not in (current_user.prefs_info['prefs_genre']['neg'] +
                                                            current_user.prefs_info['prefs_genre']['pos']):
                        # move to neg
                        current_user.prefs_info['prefs_genre']['neg'].append(selected_genre)

                if 'sort_type' == key:
                    if request.form['sort_type'] in chosen_sort:
                        sort_by = request.form['sort_type']



    else:                                                                                          #
        print(f"movie_gallery_home: request.method == {request.method}")                           #
        #pprint(request)                                                                            #
    print(f"\nmovie_gallery_home: - - - - - - - - debug - - - - - - - - - - - - - - - - E\n")          #
    #                                                                                              #
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -#

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # generate galery sorted by request
    #
    test_version = '0.0.0'
    print(f"Vs: {test_version}")
    headline_py = "movies"
    movies = [] # load jsonfile
    all_movies = []
    bad_labels = []
    genres = set()


    # by year, name, most recent etc
    for count, movie in enumerate(chosen_sort[sort_by]()):
        #if count >= 10: break
        #print(movie)
        genres.update(movie.info['genres'])
        if movie.info['title'] == 'And Then There Were None':
            bad_labels.append(movie)
        else:
            if movie.info['hires_image'] == None: movie.info['hires_image'] = 'movie_image_404.png'
            movie.info['hires_image'] = str(Path(movie.info['hires_image']).name)   # convert full path to name
            all_movies.append(movie.info)

    # choose a small random set of movies - for quick debug
    # num_of_random_movies = 10
    # start_from = random.randint(0, len(all_movies)-11)
    # for i in range(start_from, start_from + num_of_random_movies):
    #     movies.append(all_movies[i])


    movies = current_user.filter_list(all_movies)[0:9]

    # print("Incorrectly classified:")
    # for movie in bad_labels:
    #     print(Path(movie.info['file_path']).name)
    #
    # pprint(movies[9])
    # print(" - - - - ")
    print("Genres encountered:")
    print(','.join(genres))
    print("= = = \n")

    #prefs_info = current_user.prefs_info  # TODO make property
    prefs_info = current_user.get_prefs()
    pprint(prefs_info)
    users_nav_bar = []
    pprint(user_device_DB)
    for key_uuid,user_prefs in user_device_DB.items():
        users_nav_bar.append({'usr':user_prefs.name, 'user_uuid':key_uuid})


    return render_template('gallery_grid.html', movies=movies, prefs_info=prefs_info, users_nav_bar=users_nav_bar, genres=genres)




@app.route('/play_movie/<movie_id>', methods=["GET", "POST"])
def play_movie(movie_id):
    # copy so as not to change objects in media lib to strings
    movie = copy.copy(media_lib.media_with_id(movie_id))
    movie['cast'] = [ str(mv) for mv in movie['cast'] ]
    movie['file_path'] = str(movie['file_path'])
    movies = [movie]

    global vlc_http_channel
    global movie_process

    # fire up VLC and a connection to it
    if movie_process == None:
        print(f"\n\n\n-=-=-=-=- STARTING MOVIE -=-=-=-=-\n")
        movie_process = subprocess.Popen(f"exec /Applications/VLC.app/Contents/MacOS/VLC -f '{movie['file_path']}' --extraintf http", shell=True)
        # how to get a callback on processed termination
        # https://wiki.videolan.org/Documentation:Advanced_Use_of_VLC/
        # how to open in full screen mode - need to check first? & toggle
        # direct command better
        sleep(0.5)
        print(f"\n-=-=-=-=- STARTING MOVIE -=-=-=-=-\n\n\n")

    if vlc_http_channel == None:
        print(f"\n\n\n-=-=-=-=- CONNECTING -=-=-=-=-\n")
        vlc_http_channel = vlc_http(user='', pwd='p1')
        print(type(vlc_http_channel))
        print(f"\n-=-=-=-=- CONNECTING -=-=-=-=-\n\n\n")


    # https://pythonise.com/series/learning-flask/flask-and-fetch-api
    if request.method == 'POST':
        print("play_movie: request.method == 'POST'")
        req = request.get_json()
        print(req)
        print('- - - - PLAYING')
        print(f"vlc_http_channel PRESENT?: {type(vlc_http_channel)} <")
        print(f"media file path: { req['path'] } <")
        print(f"file exists: { Path(req['path']).exists() } <")

        if vlc_http_channel != None and Path(req['path']).exists():
            if req['cmd'] == 'start':
                print('--: start: goto begining after opening sequences')
                vlc_http_channel.seek_from_start(210) # got 3m30

            if req['cmd'] == 'bak30s':
                print('--: bak30s')
                vlc_http_channel.seek(-30)

            if req['cmd'] == 'play':
                print('--: play')
                vlc_http_channel.play()

            if req['cmd'] == 'pause':
                print('--: pause')
                vlc_http_channel.pause()

            if req['cmd'] == 'fwd30s':
                print('--: fwd30s')
                vlc_http_channel.seek(30)


# vlc_http_channel.media_length()         # length =  '5592',
# vlc_http_channel.rate()                 # rate = '1',
# vlc_http_channel.pos()                  # position = '0.00087705912301317'
# vlc_http_channel.api_v()                # apiversion = '3'
# vlc_http_channel.is_fullscreen()        # fullscreen = 'false'
# vlc_http_channel.volume()               # volume =  '160'

            if req['cmd'] == 'end':
                print('--: end: button Goto END before credits')
                movie_length = vlc_http_channel.media_length()
                near_end_of_flick = movie_length - 360
                vlc_http_channel.seek_from_start(near_end_of_flick) # got end - 6m

            if req['cmd'] == 'bak4x':
                print('--: bak2x - NOT IMPLEMENTED')
                #vlc_http_channel.set_rate(-4.0)

            if req['cmd'] == 'vol':
                # 0-100
                new_vol = int(req['vol'])
                print(f'--: vol:{new_vol}')
                vlc_http_channel.set_volume(new_vol)

            if req['cmd'] == 'fwd2x':       # if click second time return to normal speed
                if vlc_http_channel.rate() > 3.5:
                    print('--: fwd4x - playback NORMAL')
                    vlc_http_channel.set_rate(1)
                else:
                    print('--: fwd4x - playback x4')
                    vlc_http_channel.set_rate(4.0)

            if req['cmd'] == 's1':
                print('--: s1')

            if req['cmd'] == 's2':
                print('--: s2')


            print(f"CMD: {req['cmd']}")
            #print(f"VOL:   {vlc_http_channel.volume()}")  # TODO implement functionality
            #print(f"TITLE: {vlc_http_channel.title()}")
            #print(f"FILE:  {vlc_http_channel.filename()}")
            #print(f"RATE:  {vlc_http_channel.rate()}")
            # print(f"FULLSC:{vlc_http_channel.is_fullscreen()}")
            # secs = int(vlc_http_channel.media_length())
            # m, s = divmod(secs, 60)     # / 60 ret div & mod into m, s
            # h, m = divmod(m, 60)
            # print(f"LEN:   {secs} - {h}h{m}m")
            # pos = vlc_http_channel.position()
            # pos_secs = int(secs * float(pos))
            # m, s = divmod(pos_secs, 60)     # / 60 ret div & mod into m, s
            # h, m = divmod(m, 60)
            # print(f"POS:   {pos} - {h}h{m}m")

            #print(f" {vlc_http_channel.}")

        res = make_response(jsonify({"message": "OK"}), 200)
        return res

    else:
        print(f"play_movie: request.method == {request.method}")

    print(f"play_movie: movie ID:{movie_id}")

    users_nav_bar = []
    for key_uuid,user_prefs in user_device_DB.items():
        users_nav_bar.append({'usr':user_prefs.name, 'user_uuid':key_uuid})

    return render_template('play_movie.html', movies=movies, users_nav_bar=users_nav_bar)


@app.route('/short_list', methods=["GET", "POST"])
def short_list():
    print(f"\nshort_list: - - - - - - - - debug - - - - - - - - - - - - - - - - S\n")
    if request.method == 'POST':
        if request.is_json:
            print("short_list: request.method == 'POST_JSON'")
            settings = request.get_json() # parse JSON into DICT
            pprint(settings)

            if settings != None  and 'mov_id_prefs' in settings:
                print("'mov_prefs' in settings - - - S")
                button = re.sub('mov_prefs_','', settings['button']) # which movie pref button?
                mov_id = settings['mov_id_prefs']
                rating = settings['rating']
                print(f"mov_prefs clicked: {button}")
                if button == 'sl':      # REMOVE button
                    print(f"short_list: REMOVE - mov_id:{mov_id}")
                    print(current_user.prefs_info['seen_list'])
                    print(current_user.prefs_info['short_list'])
                    if mov_id in current_user.prefs_info['short_list']: current_user.prefs_info['short_list'].remove(mov_id)
                    commit_dict_to_DB(user_device_DB)
                    return json.dumps({}), 201
                elif button == 'rate':
                    if (rating != -1) and (mov_id not in current_user.prefs_info['ratings']):
                        current_user.prefs_info['ratings'][mov_id] = rating
                        commit_dict_to_DB(user_device_DB)
                        return json.dumps({}), 201
                    return json.dumps({}), 404
                elif button == 'seen':
                    print(f"short_list: seen - mov_id:{mov_id}")
                    print(current_user.prefs_info['seen_list'])
                    print(current_user.prefs_info['short_list'])
                    if mov_id not in current_user.prefs_info['seen_list']: current_user.prefs_info['seen_list'].append(mov_id)
                    if mov_id in current_user.prefs_info['short_list']: current_user.prefs_info['short_list'].remove(mov_id)
                    commit_dict_to_DB(user_device_DB)
                    return json.dumps({}), 201
                print("'mov_prefs' in settings - - - E")
    else:
        print(f"short_list: request.method == {request.method}")
    print(f"\nshort_list: - - - - - - - - debug - - - - - - - - - - - - - - - - E\n")

    movies = [media_lib.media_with_id(mov_id) for mov_id in current_user.prefs_info['short_list']]

    prefs_info = current_user.get_prefs()
    pprint(prefs_info)

    users_nav_bar = []
    # for key_uuid,user_prefs in user_device_DB.items():
    #     users_nav_bar.append({'usr':user_prefs.name, 'user_uuid':key_uuid})

    title = f"{prefs_info['name']}'s movie shortlist . . ."
    return render_template('shortlist.html', movies=movies, prefs_info=prefs_info, users_nav_bar=users_nav_bar, title=title)




@app.route('/combined_short_list', methods=["GET", "POST"])
def combined_short_list():
    # filter out duplicates and order most frequent first!

    print("- - - combo SL - - - S")
    pprint(user_device_DB)
    # combine all users shortlists
    movies = []
    for usr_uuid,usr in user_device_DB.items():
        pprint(usr.prefs_info['short_list'])
        movies = movies + usr.prefs_info['short_list']

    movies_ids_ordered_by_frequency = [ mov for mov,count in Counter(movies).most_common() ]
    pprint(movies_ids_ordered_by_frequency)

    movies = [media_lib.media_with_id(mov_id) for mov_id in movies_ids_ordered_by_frequency]
    for m in movies:
        #pprint(m)
        print(m['title'])


    prefs_info = []
    # prefs_info = current_user.get_prefs()
    # pprint(prefs_info)

    users_nav_bar = []
    for key_uuid,user_prefs in user_device_DB.items():
        users_nav_bar.append({'usr':user_prefs.name, 'user_uuid':key_uuid})

    print("- - - combo SL - - - E")

    title = "combined movie shortlists . . ."
    return render_template('shortlist.html', movies=movies, prefs_info=prefs_info, users_nav_bar=users_nav_bar, title=title)




@app.route('/tile_view', methods=["GET", "POST"])
def tile_view():
    headline_py = "tile_view.html"
    movies = []
    return render_template('tile_view.html', movies=movies)



@app.route('/settings', methods=["GET", "POST"])
def settings():
    headline_py = "Settings"
    movies = []
    return "SETTINGS route unimplemented <a href='/'>HOME</a>" #render_template('spare_route.html', movies=movies)

@app.route('/spare_route', methods=["GET", "POST"])
def spare_route():
    headline_py = "spare_route"
    movies = []
    return "SPARE route unimplemented <a href='/'>HOME</a>" #render_template('spare_route.html', movies=movies)



if __name__ == '__main__':
    # setup notes:
    # http://flask.pocoo.org/docs/1.0/config/
    # export FLASK_ENV=development add to ~/.bash_profile
    #app.run(host='0.0.0.0', port=52001)
    #hostname = socket.gethostname()
    print("Your Computer Name is:" + hostname)
    #IPAddr = socket.gethostbyname(hostname)
    print("Your Computer IP Address is:" + IPAddr)

    if IPAddr == '192.168.1.13':
        #app.run(host='192.168.1.13', port=52001)
        app.run(host='0.0.0.0', port=52001)

    elif IPAddr == '192.168.1.16':
        app.run(host='192.168.1.16', port=52001)

    else:
        pprint(IPAddr)
        print("WARNING unknown host . . . bailing")
        sys.exit(0)

    # check this forum - VLC remote contol
    # https://forum.videolan.org/viewtopic.php?f=11&t=148606
    # add control interface for post movies select

    #
    #
    #
    #  have a look at source code for https://pypi.org/project/black/
    #
    #  Can run as script or module - w/ options
    #
    #  > black {source_file_or_directory}           # To get started right away with sensible defaults
    #
    # > python -m black {source_file_or_directory}  # You can run Black as a package if running it as a script doesn't work:
    #
    #
    #

    # media_lib = MMediaLib()
    #
    # ten_movies = ''
    # for count, movie in enumerate(media_lib.sorted_by_year(REVERSE)):
    #     #print(movie)
    #     #print(movie.as_json)
    #     t = movie.info['title']
    #     y = movie.info['year']
    #     print(f"'{t} ({y} film)',")
    #     if count >= 20: break


# EG movie:
# <class 'movie_info_disk.MMdia'>.movie_data
# {'cast': ["Chris Hemsworth",
#           <Person id:0788335[http] name:_Michael Shannon_>,
#           <Person id:0671567[http] name:_Michael Pena_>,
#               .
#               .
#           <Person id:1041023[http] name:_Navid Negahban_>,
#           <Person id:7540945[http] name:_Matthew Velez_>,
#           <Person id:8918749[http] name:_Sandra L. Velez_>,
#           <Person id:8642817[http] name:_David White_>,
#           <Person id:9001165[http] name:_Sarrett Williams_>],
#  'fav': False,
#  'file_name': '12.Strong.2018.1080p.BluRay.mp4',
#  'file_path': PosixPath('/Volumes/FAITHFUL500/15_rpi_shortlist/12 Strong (2018) [BluRay] [1080p]/12.Strong.2018.1080p.BluRay.mp4'),
#  'file_stats': os.stat_result(st_mode=33279, st_ino=29718973, st_dev=16777232, st_nlink=1, st_uid=501, st_gid=20, st_size=4096, st_atime=1593471600, st_mtime=1583265248, st_ctime=1583265248),
#  'file_title': '12 Strong',
#  'genres': ['Action', 'Drama', 'History', 'War'],
#  'hires_image': PosixPath('12_Strong_poster.jpg'),
#  'id': '1413492',
#  'image_url': 'https://m.media-amazon.com/images/M/MV5BNTEzMjk3NzkxMV5BMl5BanBnXkFtZTgwNjY2NDczNDM@._V1_SY150_CR0,0,101,150_.jpg',
#  'kind': 'movie',
#  'movie_data_loaded': True,
#  'rating': 6.6,
#  'runtime_hm': '2h10m',
#  'runtime_m': '130',
#  'seen': False,
#  'synopsis': 'Mitch Nelson, a US Army Captain with Green Berets Operational '
#               .
#               .
#              'alongside Northern Alliance leader Abdul Rashid Dostum..',
#  'title': '12 Strong',
#  'when_added': None,
#  'year': '2018'}

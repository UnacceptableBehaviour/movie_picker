#! /usr/bin/env python

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
from flask import Flask, render_template, request
app = Flask(__name__)
#        dir        file
# this causes __init_.py to execute
from moviepicker import MMediaLib,MMedia,REVERSE,FORWARD
from moviepicker import PICKLED_MEDIA_LIB_FILE_V2_TIMEBOX,PICKLED_MEDIA_LIB_FILE_V2_F500,PICKLED_MEDIA_LIB_FILE_REPO, PICKLED_MEDIA_LIB_FILE_OSX4T
from pathlib import Path
import re                                                               # regex
import socket    

print(dir())

# load info if 1st time round
# media_lib = MMediaLib(PICKLED_MEDIA_LIB_FILE_V2_TIMEBOX)
#
# check for available discs and merge them
#
# if MMediaLib.exists(PICKLED_MEDIA_LIB_FILE_V2_F500):
#     media_lib.join(MMediaLib(PICKLED_MEDIA_LIB_FILE_V2_F500))
default_library_name = 'medialib2.pickle'
volume_checklist = ['/time_box_2018/movies/__media_data2/medialib2.pickle',
 '/Osx4T/tor/__media_data2/medialib2.pickle',
 '/FAITHFUL500/__media_data2/medialib2.pickle']


import platform
running_os = platform.system()
# AIX: 'aix', Linux:'linux', Windows: 'win32', Windows/Cygwin: 'cygwin', macOS: 'darwin'
running_os_release = platform.release()

hostname = socket.gethostname()    
IPAddr = socket.gethostbyname(hostname)    
print("Your Computer Name is:" + hostname)    
print("Your Computer IP Address is:" + IPAddr)
print(f"OS: {running_os} - {running_os_release}")


if IPAddr == '192.168.1.13':    # local - osx box
    REMOTE_LINUX = Path('/Volumes/Home Directory/MMdia/__media_data2/medialib2.pickle')
    
    # vcl = []
    # for path in volume_checklist:
    #     full_path = Path('Volumes', path)
    #     vcl.append(full_path) if full_path.exists()        
    # load medialibs & merge TODO
    
    #media_lib = MMediaLib(PICKLED_MEDIA_LIB_FILE_V2_F500)
    #media_lib = MMediaLib(PICKLED_MEDIA_LIB_FILE_REPO)    
    #media_lib = MMediaLib(REMOTE_LINUX)
    #media_lib.rebase_media_DB('/Volumes/FAITHFUL500/','/Volumes/Home Directory/MMdia/')
    media_lib = MMediaLib(PICKLED_MEDIA_LIB_FILE_OSX4T)

elif IPAddr == '192.168.1.16':  # remote - linux box    
    LOCAL_LINUX = Path('/home/pi/MMdia/','__media_data2/medialib2.pickle')    
    media_lib = MMediaLib(LOCAL_LINUX)
    media_lib.rebase_media_DB('/Volumes/FAITHFUL500/','/home/pi/MMdia/')


LOCAL_IMAGE_CACHE = Path('./static/covers')
LOCAL_IMAGE_CACHE.mkdir(parents=True, exist_ok=True)

media_lib.cache_images_locally(LOCAL_IMAGE_CACHE)
print(f"LOADED: {len(media_lib)}")
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


# debug
from pprint import pprint           # giza a look
import inspect


# each app.route is an endpoint
@app.route('/')
def db_hello_world():
    test_version = '0.0.0'
    print(f"Vs: {test_version}") 
    headline_py = "movies"
    movies = [] # load jsonfile
     
    bad_labels = []
    genres = set()

    for count, movie in enumerate(media_lib.sorted_by_year(REVERSE)):
    #for count, movie in enumerate(media_lib.sorted_by_most_recently_added(REVERSE)):        
        print(movie)
        genres.update(movie.info['genres'])
        if movie.info['title'] == 'And Then There Were None':
            bad_labels.append(movie)
        else:            
            if movie.info['hires_image'] == None: movie.info['hires_image'] = 'movie_image_404.png'
            movie.info['hires_image'] = str(Path(movie.info['hires_image']).name)   # convert full path to name
            movies.append(movie.info)
        #if count >= 10: break  
    
    print("Incorrectly classified:")
    for movie in bad_labels:
        print(Path(movie.info['file_path']).name)
    
    pprint(movies[33])
    print("Genres encountered:")
    pprint(genres)
    print("= = = \n")
    
    return render_template('gallery.html', movies=movies)

@app.route('/db_movie_page', methods=["GET", "POST"])
def db_movie_page():        
    movies = []
    return render_template('index.html', movies=movies)

@app.route('/css_course_1', methods=["GET", "POST"])
def css_course_1():
    headline_py = "css_course_1"
    movies = []
    return render_template('css_course_1.html', movies=movies)

@app.route('/css_course_2', methods=["GET", "POST"])
def css_course_2():
    headline_py = "css_course_2"
    movies = []
    return render_template('css_course_2.html', movies=movies)

@app.route('/settings', methods=["GET", "POST"])
def settings():
    headline_py = "Settings"
    movies = []
    return render_template('index.html', movies=movies)

@app.route('/spare_route', methods=["GET", "POST"])
def spare_route():
    headline_py = "spare_route"
    movies = []
    return render_template('index.html', movies=movies)

@app.route('/buttons_inputs', methods=["GET", "POST"])
def buttons_inputs():
    headline_py = "buttons_inputs"
    movies = []
    return render_template('index.html', movies=movies)


if __name__ == '__main__':
    # setup notes:
    # http://flask.pocoo.org/docs/1.0/config/
    # export FLASK_ENV=development add to ~/.bash_profile    
    #app.run(host='0.0.0.0', port=52001)
    hostname = socket.gethostname()    
    IPAddr = socket.gethostbyname(hostname)    
    print("Your Computer Name is:" + hostname)    
    print("Your Computer IP Address is:" + IPAddr)
    
    if IPAddr == '192.168.1.13':
        app.run(host='192.168.1.13', port=52001)
    
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
# {'cast': [<Person id:1165110[http] name:_Chris Hemsworth_>,
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
    

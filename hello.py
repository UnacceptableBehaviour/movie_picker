#! /usr/bin/env python

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
from flask import Flask, render_template, request
app = Flask(__name__)
#        dir        file
# this causes __init_.py to execute
from moviepicker import MMediaLib,MMedia,REVERSE,FORWARD
from moviepicker import PICKLED_MEDIA_LIB_FILE_V2_TIMEBOX,PICKLED_MEDIA_LIB_FILE_V2_F500,PICKLED_MEDIA_LIB_FILE_REPO
from pathlib import Path
import re                                                               # regex

print(dir())

# load info if 1st time round
# media_lib = MMediaLib(PICKLED_MEDIA_LIB_FILE_V2_TIMEBOX)
# 
# if MMediaLib.exists(PICKLED_MEDIA_LIB_FILE_V2_F500):
#     media_lib.join(MMediaLib(PICKLED_MEDIA_LIB_FILE_V2_F500))

#media_lib = MMediaLib(PICKLED_MEDIA_LIB_FILE_V2_F500)
media_lib = MMediaLib(PICKLED_MEDIA_LIB_FILE_REPO)
LOCAL_IMAGE_CACHE = Path('./static/covers')
media_lib.cache_images_locally(LOCAL_IMAGE_CACHE)
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
    app.run(host='192.168.1.13', port=52001)
    
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
    

#! /usr/bin/env python

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
from flask import Flask, render_template, request
app = Flask(__name__)
#        dir        file
from moviepicker.moviepicker import MMediaLib,MMedia,REVERSE,FORWARD    # WORKS w/o __init__.py
from pathlib import Path
import re                                                               # regex

# load info if 1st time round
media_lib = MMediaLib()
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

#import sys
#print(f"Modules searched for here:{sys.path}")
# print(dir())            # current name table
# ['FORWARD', 'Flask', 'MMedia', 'MMediaLib', 'REVERSE', '__annotations__', '__builtins__', '__cached__',
#  '__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__', 'app', 'render_template', 'request', 'sys']
# print(__name__) # __main__
# print(__file__) # ./hello.py

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
            movies.append(movie.info)
        #if count >= 10: break  
    
    print("Incorrectly classified:")
    for movie in bad_labels:
        print(Path(movie.info['file_path']).name)
    
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
    app.run(host='0.0.0.0', port=52001)
    
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
# { "id": "0139809",
#   "title": "The Thirteenth Floor",
#   "synopsis": "Computer scientist Hannon Fuller has discovered something extremely important. He's about to tell the
#               discovery to his colleague, Douglas Hall, but knowing someone is after him, the old man leaves a letter in the
#               computer generated parallel world his company has created (which looks like the 30's with seemingly real people
#                                                                          with real emotions). Fuller is murdered in our real
#               world the same night, and his colleague is suspected. Douglas discovers a bloody shirt in his bathroom and he
#               cannot recall what he was doing the night Fuller was murdered. He logs into the system in order to find the
#               letter, but has to confront the unexpected. The truth is harsher than he could ever imagine...::Danny
#               Rosenbluth",
#   "year": "1999",
#   "cast": ["Craig Bierko","Armin Mueller-Stahl", "Gretchen Mol", "Vincent D'Onofrio", "Dennis Haysbert", "Steven Schub",
#            "Jeremy Roberts", "Rif Hutton","Leon Rippy", "Janet MacLachlan", "Brad William Henke", "Burt Bulos",
#            "Venessia Valentino", "Howard S. Miller","Tia Texada", "Shiri Appleby", "Bob Clendenin"],
#   "runtime_m": "100",
#   "runtime_hm": "1h40m",
#   "rating": 7.1,
#   "genres": ["Mystery", "Sci-Fi", "Thriller"],
#   "kind": "movie",
#   "seen": false,
#   "fav": false,
#   "image_url": "https://m.media-amazon.com/images/M/MV5BODYxZTZlZTgtNTM5MC00N2RhLTg3MjUtNGVkMDJjMGY3YzA5L2ltYWdlL2ltYWdlXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_SX101_CR0,0,101,150_.jpg",
#   "hires_image": null,
#   "file_path": "/Volumes/time_box_2018/movies/The Thirteenth Floor (1999) [1080p]/The.Thirteenth.Floor.1999.1080p.BluRay.x264.YIFY.mp4",
#   "file_stats": null,
#   "file_name": null,
#   "file_title": "The Thirteenth Floor",
#   "when_added": null,
#   "movie_data_loaded": true}
    

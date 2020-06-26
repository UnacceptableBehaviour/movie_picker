#! /usr/bin/env python

from flask import Flask, render_template, request
app = Flask(__name__)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
import sys
print(f"Modules searched for here:{sys.path}")

#        dir        file
from moviepicker.moviepicker import MMediaLib,MMedia,REVERSE,FORWARD
#from moviepicker import MMediaLib,MMedia,REVERSE,FORWARD               # NO work

import moviepicker
print("dir(moviepicker):")
print(dir(moviepicker))
# ['__doc__', '__file__', '__loader__', '__name__', '__package__', '__path__', '__spec__',
#  'helpers', 'moviepicker', 'mp_exceptions']

print(__name__) # __main__
print(__file__) # ./hello.py

print(dir(moviepicker.mp_exceptions))
#['IncorrectSortAttributeError', 'MMediaLibError', 'NoDBFileFound', 'NoRootDirectoryOrDBFound',
# '__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__']

from pprint import pprint           # giza a look
import re                           # regex


# each app.route is an endpoint
@app.route('/')
def db_hello_world():
    test_version = '0.0.0'
    print(f"Vs: {test_version}") 
    headline_py = "movies"
    movies = [] # load jsonfile
 
    # load info if 1st time round
    if len(movies) == 0:
        fs_tor = MMediaLib()    
        #display_list = []
        count = 0
        for movie,media in fs_tor['video'].items():
            count += 1
            if count > 1: break
            file_size = round(fs_tor['video'][movie].file_stat.st_size / (1024 * 1024),1)
            if file_size > 400:
                print(f"\n> - - - - - - - - -  - - - - \ \n{movie}\nfs_tor:{fs_tor['video'][movie]}\n{file_size}MB\n\n")
                print(type(media))
                pprint(media.movie_data)
                movies.append(media.movie_data)
                print('--')   
 
    
    return render_template('gallery.html', movies=movies)


@app.route('/settings', methods=["GET", "POST"])
def buttons_inputs():
    headline_py = "Settings"
    movies = {}
    return render_template('index.html', movies=movies)


if __name__ == '__main__':
    # setup notes:
    # http://flask.pocoo.org/docs/1.0/config/
    # export FLASK_ENV=development add to ~/.bash_profile
    #app.run(host='0.0.0.0', port=52001)
    
    media_lib = MMediaLib()
    # print("Lib LOADED, sorted lists:")
    # media_lib.sorted_lists()    
    # print("END, sorted lists:")
    
    ten_movies = ''
    for count, movie in enumerate(media_lib.sorted_by_year(REVERSE)):
    #for count, movie in enumerate(media_lib):
        if count > 10: break
        print(movie)
          

# EG:
# <class 'movie_info_disk.MMdia'>.movie_data
#{"id": "0139809", "title": "The Thirteenth Floor", "synopsis": "Computer scientist Hannon Fuller has discovered something extremely important. He's about to tell the discovery to his colleague, Douglas Hall, but knowing someone is after him, the old man leaves a letter in the computer generated parallel world his company has created (which looks like the 30's with seemingly real people with real emotions). Fuller is murdered in our real world the same night, and his colleague is suspected. Douglas discovers a bloody shirt in his bathroom and he cannot recall what he was doing the night Fuller was murdered. He logs into the system in order to find the letter, but has to confront the unexpected. The truth is harsher than he could ever imagine...::Danny Rosenbluth", "year": "1999", "cast": ["Craig Bierko", "Armin Mueller-Stahl", "Gretchen Mol", "Vincent D'Onofrio", "Dennis Haysbert", "Steven Schub", "Jeremy Roberts", "Rif Hutton", "Leon Rippy", "Janet MacLachlan", "Brad William Henke", "Burt Bulos", "Venessia Valentino", "Howard S. Miller", "Tia Texada", "Shiri Appleby", "Bob Clendenin"], "runtime_m": "100", "runtime_hm": "1h40m", "rating": 7.1, "genres": ["Mystery", "Sci-Fi", "Thriller"], "kind": "movie", "seen": false, "fav": false, "image_url": "https://m.media-amazon.com/images/M/MV5BODYxZTZlZTgtNTM5MC00N2RhLTg3MjUtNGVkMDJjMGY3YzA5L2ltYWdlL2ltYWdlXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_SX101_CR0,0,101,150_.jpg", "hires_image": null, "file_path": "/Volumes/time_box_2018/movies_Chris/__for_chris/movies_recomended/The Thirteenth Floor (1999) [1080p]/The.Thirteenth.Floor.1999.1080p.BluRay.x264.YIFY.mp4", "file_stats": null, "file_name": null, "file_title": "The Thirteenth Floor", "when_added": null, "movie_data_loaded": true}
    

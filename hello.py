#! /usr/bin/env python

from flask import Flask, render_template, request
app = Flask(__name__)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

from movie_info_disk import get_MMdia_lib, MMdia #, MMdia_lib

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
        fs_tor = get_MMdia_lib()    
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
    
    fs_tor = get_MMdia_lib()    
    display_list = []
    count = 0
    for movie,media in fs_tor['video'].items():
        count += 1
        if count > 10: break
        file_size = round(fs_tor['video'][movie].file_stat.st_size / (1024 * 1024),1)
        if file_size > 400:
            print(f"\n> - - - - - - - - -  - - - - \ \n{movie}\nfs_tor:{fs_tor['video'][movie]}\n{file_size}MB\n\n")
            print(type(media))
            pprint(media.movie_data)
            display_list.append(movie)
            print('- - - - - - - - - - - - - - / \n')
          
    print(len(display_list))
    print(f"fs_tor: {type(fs_tor)}")

# EG:
# <class 'movie_info_disk.MMdia'>.movie_data
# {'cast': [<Person id:1165110[http] name:_Chris Hemsworth_>,
#           <Person id:0788335[http] name:_Michael Shannon_>,
#                       .
#                       .
#           <Person id:9128965[http] name:_Arshia Mandavi_>,
#           <Person id:0665235[http] name:_Elsa Pataky_>],
#  'fav': False,
#  'file_name': PosixPath('/Volumes/time_box_2018/movies/12 Strong (2018) [BluRay] [1080p] [YTS.AM]/12.Strong.2018.1080p.BluRay.x264-[YTS.AM].mp4'),
#  'file_title': '12 Strong',
#  'genres': ['Action', 'Drama', 'History', 'War'],
#  'id': '1413492',
#  'image_url': 'https://m.media-amazon.com/images/M/MV5BNTEzMjk3NzkxMV5BMl5BanBnXkFtZTgwNjY2NDczNDM@._V1_SY150_CR0,0,101,150_.jpg',
#  'kind': 'movie',
#  'rating': 6.5,
#  'runtime_hm': '2h10m',
#  'runtime_m': '130',
#  'seen': False,
#  'synopsis': 'Mitch Nelson, a US Army Captain with Green Berets Operational '
#              'Detachment Alpha (ODA) 595, is moving into a new home with his '
#              'wife and daughter on September 11, 2001, after receiving an '
#              'assignment to staff duty under LTC Bowers. As news of the '
#              'devastating terrorist attacks that day break, Nelson volunteers '
#              'to lead 595 into Afghanistan. Bowers initially refuses, but '
#              'veteran soldier CW5 Hal Spencer, previously scheduled to retire, '
#              'persuades Bowers to give Nelson command of 595 again, as well as '
#              'volunteering himself for the deployment. After leaving their '
#              'families, 595 travels to Uzbekistan on October 7, 2001. After '
#              'being briefed and evaluated by COL Mulholland, Commander of 5th '
#              'Special Forces Group, Nelson and 595 are picked to fight '
#              'alongside Northern Alliance leader Abdul Rashid Dostum..',
#  'title': '12 Strong',
#  'year': '2018'}
    

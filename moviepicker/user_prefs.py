'''
UserPrefs
State / Filtering functionality
'''

from pprint import pprint
from .helpers import hr_readable_from_nix_no_space

import json
from pathlib import Path
USER_DB_FILE = Path('./moviepicker/userDB.json')

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
                           'chosen_sort':'year',
                           'prefs_genre': {'neg':[],
                                          #"genres_all":["History","War","Sci-Fi","Music","Sport","Romance","Adventure","Action","Mystery","Thriller","Documentary","Musical","Biography","News","Fantasy","Animation","Family","Crime","Drama","Comedy","Horror","Western"],
                                          'pos':[]},
                           'prefs_actors':{'neg':[],
                                          'pos':[]},
                           'current_user': False
                           }
        self.prefs_info.update(info)

        self.prefs_info['uuid'] = uuid
        if name: self.prefs_info['name'] = name


    def update_prefs(self, new_prefs):
        if new_prefs['uuid'] == self.prefs_info['uuid']:
            print("UserPrefs.update_prefs succeed")
            self.prefs_info.update(new_prefs)
        else:
            raise UserUuidMismatch

    @property
    def info(self):
        return self.prefs_info

    @info.setter
    def info(self, info):
        self.prefs_info.update(info)

    def uuid(self):
        return self.prefs_info['uuid']

    @property
    def name(self):
        return self.prefs_info['name']

    @name.setter
    def name(self, name):
        self.prefs_info['name'] = name

    @property
    def sort_by(self):
        return self.prefs_info['chosen_sort']

    @sort_by.setter
    def sort_by(self, sort_by):
        self.prefs_info['chosen_sort'] = sort_by


    def add_fingerprint(self, fingerprint):
        if fingerprint not in self.prefs_info['fingerprints']:
            self.prefs_info['fingerprints'].append(fingerprint)

    #
    # TODO adapt interface so its update on change - also bake in order based on ratings
    #
    def filter_list(self, movie_list):
        '''
        List order
                Mayor Sort              Minor sort      8 digits should do:
        Rating  0 <= n < 1 ..2,3,4      genre           XXRRGGGG        G - Genre
        Year    year                    genre           YYYYGGGG        R - Rating 0-10 no decimal
        Title   title only              none            NA              Y - Year
        Added   title only              none            YYYYMMDD        M/D Month / Day

        Push major for up by orders of magnitude
            for rating you need 2 digits 0-10
            for year you need 4 - 1981
            for Added YYYYMMDD so 8 digits - absolute sort genre not relevant
            for title simple sort by title
            Remove NI/seen from list before sorting
            For Genre say up to 100 (currently 25, plus user additions) 10x = 1000,  double for -ve & +ve 2000
                Start the genre @ 1000 +1 for green, +0 for grey, -1 for red
                Since we're using 4 digits might as well start in the middle 5000.
        '''
        GENRE_BASELINE = 5000
        scored_and_sorted_movies = []
        print(f"UserPrefs.filter_list: {len(movie_list)}")
        for m in movie_list:
            if m['id'] in self.prefs_info['seen_list']: continue        # don't show
            if m['id'] in self.prefs_info['ni_list']: continue
            if m['id'] in self.prefs_info['short_list']: continue

            if self.info['chosen_sort'] != 'title':
                genre_score = GENRE_BASELINE
                    # genres         in movie               in prefs pos / neg
                pos = len(list( set(m['genres']) & set(self.prefs_info['prefs_genre']['pos']) ))
                neg = len(list( set(m['genres']) & set(self.prefs_info['prefs_genre']['neg']) ))
                genre_score += pos
                genre_score -= neg

                if self.info['chosen_sort'] == 'year':
                    year = int(m['year']) * 10000
                    m['prefScore'] = year + genre_score
                elif self.info['chosen_sort'] == 'rating':
                    rating = int(str(m['rating']).split('.')[0]) * 10000        # push to top 4 digits
                    m['prefScore'] = rating + genre_score
                if self.info['chosen_sort'] == 'added':
                    # mv_ctime = m['file_stats'].st_ctime
                    # hr_mv = hr_readable_from_nix(mv_ctime)
                    # print(f"file_stats: {mv_ctime} - {hr_mv} - st_a:{hr_readable_from_nix(m['file_stats'].st_atime)} - st_m:{hr_readable_from_nix(m['file_stats'].st_mtime)}\nadded:{m['when_added']}\n")
                    if m['when_added'] == None:
                        m['prefScore'] = int(hr_readable_from_nix_no_space(m['file_stats'].st_ctime))
                    else:
                        m['prefScore'] = int(m['when_added'])
                else:
                    m['prefScore'] = genre_score

                scored_and_sorted_movies.append(m)
                scored_and_sorted_movies  = sorted(scored_and_sorted_movies, key=lambda k: k['prefScore'], reverse=True)
            else:
                scored_and_sorted_movies = movie_list

        pprint( scored_and_sorted_movies[0] )
        pprint( self.info )

        return scored_and_sorted_movies






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
        db[i] = commit_db[i].info

    with open(USER_DB_FILE, 'w') as f:
        #pprint(db)
        db_as_json = json.dumps(db)
        f.write(db_as_json)


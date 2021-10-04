'''
UserPrefs
State / Filtering functionality
'''

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

    # deprecated - find uses - change TODO
    def get_prefs(self):
        return self.prefs_info

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
            if m['id'] in self.prefs_info['seen_list']: m['prefScore'] -= 2500
            if m['id'] in self.prefs_info['ni_list']: m['prefScore'] -= 2500
            if m['id'] in self.prefs_info['short_list']: m['prefScore'] -= 2000 # dont't bubble to top if shortlisted

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


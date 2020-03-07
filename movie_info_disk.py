#! /usr/bin/env python
from pathlib import Path
from collections import Counter
from pprint import pprint
import re
import json
import imdb    
import urllib.request

class MMdia:
  # choose order by most frequently occuring
  AUDIO_EXTS = [ '.mp3', '.ac3' ]                   
  VIDEO_EXTS = [ '.mp4', '.avi', '.mkv', '.m4a' ]
  JSON_DUMP = './scratch/media.json'
  __badly_formatted_names = []

  media_files_count = { 'video': Counter(),   # no need to initialise, and will find duplicates
                        'audio': Counter() }

  media_files = { 'video': {},
                  'audio': {} }
  
  other_files = []
  
  def __init__( self, file_path ):
    self.full_path = Path(file_path)
    self.filename = self.full_path.name
    self.location = self.full_path.parent
    self.file_stat = Path(file_path).stat()
    self.movie_data = {
      'id': None,
      'title': '',
      'synopsis': '',
      'year': 0,
      'cast': [],
      'runtime_m': 0,
      'runtime_hm': 0,
      'rating':0,
      'genres':[],
      'kind':[],
      'seen': False,
      'fav':False,
      'image_url':None,
      'file_name': self.full_path,
      'file_title': None
    }
    self.get_media_name_and_year_from_disc()
    self.query_imdb_for_movie_info()
    #st_size

  def to_s(self):
    print

  # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
  # USING imdb module
  # Usage (keys): https://imdbpy.readthedocs.io/en/latest/usage/movie.html#movies
  # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
  def query_imdb_for_movie_info(self):
    # self.movie_data = {
    #   'id': None,
    #   'title': '',
    #   'synopsis': '',
    #   'year': 0,
    #   'cast': [],
    #   'runtime': 0,
    #   'rating':0,
    #   'genres':[],
    #   'kind':[],
    #   'seen': False,
    #   'fav':False
    # }
    ia = imdb.IMDb()      # instantiation cost?
    query = f"{self.movie_data['file_title']} {self.movie_data['year']}"    
    print(f"\n\n\n")
    print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
    print(f"Retieving info from IMDB\nSearching for: {query} <")
    print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
    results = ia.search_movie(query)

    chosen = 0
    
    print("Found:")
    for i,m in enumerate(results):
      print(i, m, m['kind'])
      if m['kind'] == 'movie':
        chosen = i
        break
    
    # chosen = input(f"Select result from 0 - {len(results)-1} (default 0):")
    # if chosen == '' : chosen = 0    
    # chosen = int(chosen)
      
    # return result with highest Doc Distance with search
    #movie = results[chosen]
    self.movie_data['id'] = results[chosen].movieID
    
    m = ia.get_movie(results[chosen].movieID)
    #print(ia.get_movie_infoset())
    
    print(f"ID: {m.movieID}")
    print(f"Title: {m['title']}")
    try:
      self.movie_data['title'] = m['title']
    except:
      print(">> - - - - - > WARNING: no m['title']")
    
    print(f"Rating: {m['rating']}")
    try:
      self.movie_data['rating'] = m['rating']
    except:
      print(">> - - - - - > WARNING: no m['rating']")      
    
    print(f"Runtimes: {m['runtimes']} or {int(m['runtimes'][0])%60}h{int(m['runtimes'][0])%60}m")
    print(m.current_info)
    try:
      self.movie_data['runtime_m'] = m['runtimes'][0]
      self.movie_data['runtime_hm'] = f"{int(m['runtimes'][0])%60}h{int(m['runtimes'][0])%60}m"
    except:
      print(">> - - - - - > WARNING: no m['runtimes']")
      
    # m.get('plot') - list of str (7 in this case all diffferent)
    plot_size = 0
    for synopsis in m.get('plot'):
      # caballo grande ande on no ande!
      if plot_size < len(synopsis):
        plot_size = len(synopsis)
        self.movie_data['synopsis'] = synopsis
        print(f"SYNOPSIS:\n{synopsis}")
      
    print(f"\nSYNOPSIS PICKED:\n{synopsis}")        
    
    
    # this is actually the plot - massive
    # print(f"\nSYNOPSIS:\n{m.get('synopsis')}")
    
    print(f"GENRES?: {'genres' in m}")
    if 'genres' in m: print(m['genres'])
    print(f"KIND: {m['kind']}")
    try:
      self.movie_data['genres'] = m['genres']
      self.movie_data['kind'] = m['kind']
    except:
      print(">> - - - - - > WARNING: no m['genres'] or ['kind'] ?")      
    
    print(f"CAST:")    
    #for index, member in enumerate(m['cast']):
    #  print(member, member['id'])
    
    index = 0
    for member in m['cast']:
      print(member)
      if index > 10: break
      index+=1
      
    # this retreives low quality cover art
    #
    # https://m.media-amazon.com/images/M/MV5BNGVjNWI4ZGUtNzE0MS00YTJmLWE0ZDctN2ZiYT...
    # ...k2YmI3NTYyXkEyXkFqcGdeQXVyMTkxNjUyNQ@@._V1_SY150_CR0,0,101,150_.jpg
    #
    # Change ending @@._V1_SY300_CR0,0,201,300_.jpg
    #                    size ^    x,y,x1, y1
    print(f"COVER ART: {m['cover url']}")
    try:
      self.movie_data['image_url'] = m['cover url']
      url = self.movie_data['image_url']
    except:
      print(">> - - - - - > WARNING: no m['genres'] or ['kind'] ?")
      
    # url = urllib.parse.quote(url, safe='/:')  # replace spaces if there are any - urlencode
    # print(url)    
    local_file_name = Path(self.location, f"{self.full_path.stem}.jpg")
    print(f"STORING IMAGE TO:\n{local_file_name}")
    #urllib.request.urlretrieve(url, local_file_name)
    urllib.request.urlretrieve(url, Path('./scratch', f"{self.full_path.stem}.jpg"))
    
    # from scrape
    # https://www.imdb.com/title/tt7286456/mediaviewer/rm3353122305
    #                          ID: 7286456
    #                       Title: Joker

    
    

  def get_media_name_and_year_from_disc(self):
    #if self.is_video(self.filename):
    if self.obj_is_video():
      # movies
      # looking for: name followed by year or (year) or [year] resolution bla bla .ext
      # r'[\(\)\[\]]?\d\d\d\d[\(\)\[\]]?[\.\b]' - 4 digit year followed by . or word boundary      
      match = re.search(r'(.*?)[\(\)\[\]]?(\d\d\d\d)[\(\)\[\]]?[\.\b]', self.filename, re.I )
      if match:
        self.movie_data['year'] = match.group(2)
        dirty_title = match.group(1)
        dirty_title = re.sub(r'^[\W_]*','',dirty_title)     # remove leading non word
        dirty_title = re.sub(r'[\W_]*$','',dirty_title)     # remove trailing non word
        dirty_title = re.sub(r'[\._]',' ',dirty_title)      # replace . and underscore with space
        self.movie_data['file_title'] = dirty_title
        
      else:
        self.__badly_formatted_names.append(self.full_path)
    
    elif self.obj_is_audio():
      pass
    
    else:
      pass

  def obj_is_audio(self):
    return Path(self.filename).suffix in MMdia.AUDIO_EXTS

  def obj_is_video(self):
    return Path(self.filename).suffix in MMdia.VIDEO_EXTS
  
  @staticmethod
  def is_audio(filename):
    return Path(filename).suffix in MMdia.AUDIO_EXTS

  @staticmethod
  def is_video(filename):
    return Path(filename).suffix in MMdia.VIDEO_EXTS
        
  @staticmethod
  def refresh_media_files_information(root_dir):
    
    # iterate through all paths found - p
    for p in root_dir.glob('**/*'):
      
      if MMdia.is_audio(p):
        MMdia.media_files_count['audio'][p.name.lower()] += 1
        MMdia.media_files['audio'][p.name.lower()] = MMdia(p)

      elif MMdia.is_video(p):
        MMdia.media_files_count['video'][p.name.lower()] += 1
        MMdia.media_files['video'][p.name.lower()] = MMdia(p)

      else:
        MMdia.other_files.append(p)
            
      #print(p.name.lower())
      
    return MMdia.media_files
  
  @staticmethod
  def dump_bad_names():
    print("= = = = = = = = = = = = = = = = = = = = POOR NAMING CONVENTIONS = = = = = = = = = = = = = = = = = = = = = = = = ")
    print("= = = = = = = = = = = = = = = = = = = = POOR NAMING CONVENTIONS = = = = = = = = = = = = = = = = = = = = = = = = ")
    for n in MMdia.__badly_formatted_names:
      print(f"\n\n{n.name}\n{n.parent}")
    print("= = = = = = = = = = = = = = = = = = = = POOR NAMING CONVENTIONS = = = = = = = = = = = = = = = = = = = = = = = = ")
    print("= = = = = = = = = = = = = = = = = = = = POOR NAMING CONVENTIONS = = = = = = = = = = = = = = = = = = = = = = = = ")
                


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# helpers
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
mmdia_root = Path('/Volumes/FAITHFUL500')
def get_list_of_file_extensions(root_dir = mmdia_root):
  extensions = Counter()
  
  for p in root_dir.glob('**/*'):
    extensions[p.suffix.lower()] += 1
    
  return extensions

  

def main():
  pass


if __name__ == '__main__':
        
    #pprint(get_list_of_file_extensions())
    # pathlib example - use

    media_lib = MMdia.refresh_media_files_information(mmdia_root)
    
    print(f"SIZE: {media_lib['video'].keys()} - {len(media_lib['video'].keys())} - {type(media_lib)}")
    
    #pprint(media_lib['video'])
    #pprint(media_lib['audio'])
    ##MMdia.dump_bad_names()

    # self.full_path = Path(file_path)
    # self.filename = self.full_path.name
    # self.location = self.full_path.parent
    # self.file_stat = Path(file_path).stat()
    # self.movie_data = {
    #   'id': None,
    #   'title': '',
    #   'synopsis': '',
    #   'year': 0,
    #   'cast': [],
    #   'runtime_m': 0,
    #   'runtime_hm': 0,
    #   'rating':0,
    #   'genres':[],
    #   'kind':[],
    #   'seen': False,
    #   'fav':False,
    #   'image_url':None,
    #   'file_name': self.full_path,
    #   'file_title': None
    # }
    
    count = 0
    for k in media_lib['video'].keys():
      #if len(media_lib['video'][k].movie_data['title']) == 0: continue        # skip titles of zero length - curate later
      count += 1
      print(f"\n\ndisk: {k} - {count}<")
      pprint(media_lib['video'][k])               # TODO ex - use metaclass to dump object attributes
      print(media_lib['video'][k].full_path)
      print(media_lib['video'][k].filename)
      print(media_lib['video'][k].location)
      print(media_lib['video'][k].file_stat)
      pprint(media_lib['video'][k].movie_data)
      # print(media_lib['video'][k].movie_data['title'], len(media_lib['video'][k].movie_data['title']))
      # print(media_lib['video'][k].movie_data['year'])
      print(f"{int(media_lib['video'][k].file_stat.st_size/(1024*1024))}MiB")
      print(f"{round(media_lib['video'][k].file_stat.st_size/(1024*1024*1024),1)}GiB")
      if count > 200: break
    
            
    # 
    #print(json.dumps(media_lib))   #MMdia not serializable
    #print(MMdia.JSON_DUMP)
    #       
    # # create JSON for easy flask import (DB interrim)
    # with open(MMdia.JSON_DUMP, "w") as f:      
    #   f.write(json.dumps(media_lib)

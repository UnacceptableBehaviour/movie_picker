#! /usr/bin/env python
from pathlib import Path
from collections import Counter
from pprint import pprint
import re
import json
import imdb    
import urllib.request
import math
import traceback
import pickle


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
    
    # return result with highest Doc Distance with search
    movie = select_best_item_from_search_results('movie', query, results)
      
    
    self.movie_data['id'] = movie.movieID
    
    m = ia.get_movie(movie.movieID)
    #print(ia.get_movie_infoset())
    
    try:
      print(f"ID: {m.movieID}")
      print(f"Title: {m['title']}")
      self.movie_data['title'] = m['title']
    except:
      print(">> - - - - - > WARNING: no m['title']")
    
    
    try:
      print(f"Rating: {m['rating']}")
      self.movie_data['rating'] = m['rating']
    except:
      print(">> - - - - - > WARNING: no m['rating']")      
    

    try:
      print(f"Runtimes: {m['runtimes']} or {int(int(m['runtimes'][0])/60)}h{int(m['runtimes'][0])%60}m")
      print(m.current_info)
      self.movie_data['runtime_m'] = m['runtimes'][0]
      self.movie_data['runtime_hm'] = f"{int(int(m['runtimes'][0])/60)}h{int(m['runtimes'][0])%60}m"
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
    
    limit_to = 1
    count = 0
    # iterate through all paths found - p
    for p in root_dir.glob('**/*'):
      
      if MMdia.is_audio(p):
        MMdia.media_files_count['audio'][p.name.lower()] += 1
        MMdia.media_files['audio'][p.name.lower()] = MMdia(p)

      elif MMdia.is_video(p):
        MMdia.media_files_count['video'][p.name.lower()] += 1
        MMdia.media_files['video'][p.name.lower()] = MMdia(p)
        count += 1
        if count > limit_to:
          break

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
#mmdia_root = Path('./scratch')
def get_list_of_file_extensions(root_dir = mmdia_root):
  extensions = Counter()
  
  for p in root_dir.glob('**/*'):
    extensions[p.suffix.lower()] += 1
    
  return extensions

# given the kind and query select the most appropriate result
# from the list returned by the query
def select_best_item_from_search_results(kind, query, results):
  result = None
  right_kind = []
  doc_distances = {}
  
  possible_kinds = ['movie', 'tv series', 'tv mini series', 'video game', 'video movie', 'tv movie', 'episode']
  
  if kind not in possible_kinds:
    kind == 'movie'
    
  # collect result of the right 'kind'
  for i,r in enumerate(results):
    print(f"{i} - {r['title']}")
    if r['kind'] == kind:
      right_kind.append(r)
  
  print(f"Found {len(right_kind)} of the right_kind . .")
  pprint(right_kind)
  
  # walk saerch results and find best match  
  for sr in right_kind:
    search_vector = get_doc_vector_word(query)
    
    result_title_with_year = sr['title']    
    try:
      result_title_with_year = f"{sr['title']} {sr['year']}"
    except Exception:
      print("select_best_item_from_search_results")
      traceback.print_exc()
    finally:
      result_vector = get_doc_vector_word(result_title_with_year)
      
    doc_distances[sr] = doc_distance(search_vector, result_vector)
    print(f"\nQRY:{query}\n\nRESULT: {result_title_with_year}\nd_d:{doc_distances[sr]}")
    pprint(sr)
  
  # print("right_kind")
  # pprint(right_kind)
  # print("doc_distances")
  # pprint(doc_distances)
  # sort dict by value
  # for dict x    items in x---\             
  # {k: v for k, v in sorted(x.items(), key=lambda item: item[1])}    # dict comprehension
  # sorted( item_to_sort, key=sorting_function_applied_to_each_item ) # https://docs.python.org/3/howto/sorting.html
  # sorted_d_d = {k: v for k,v in sorted(doc_distances.items(), key=lambda item: item[1])}  # dict item[0]=key item[1]=value ?
  # print("doc_distances.items()")
  # pprint(doc_distances.items())
  # print(r'sorted(doc_distances.items(), key=lambda item: item[1])')
  # pprint(sorted(doc_distances.items(), key=lambda item: item[1]))
  # print("sorted_d_d")
  # pprint(sorted_d_d)      # not sorted when it prints!? WTF
  # print('sorted(doc_distances.items(), key=lambda item: item[1])[0][0]')
  # pprint(sorted(doc_distances.items(), key=lambda item: item[1])[0][0])
  
  LOWEST_DOC_DISTANCE = 0
  MOVIE = 0
  DOC_DIST = 1
  
  return sorted(doc_distances.items(), key=lambda item: item[1])[LOWEST_DOC_DISTANCE][MOVIE] 

# put smaller vector 1st!
def inner_product(v1,v2):
  sum = 0.0
  
  for symbol1 in v1:                # go through keys 
    if symbol1 in v2:      
        sum += v1[symbol1] * v2[symbol1]
  
  return sum


#def vector_angle(d1, d2):  
def doc_distance(d1, d2):
  """
  Return the angle between these two vectors.
  """
  numerator = inner_product(d1,d2)  
  denominator = math.sqrt(inner_product(d1,d1)*inner_product(d2,d2))
  return math.acos(numerator/denominator)  
    
  

def get_doc_vector_word(doc):
  # remove non alphanumeric and white space
  #print(f"get_doc_vector_word 0:{doc}")
  doc = re.sub(r'[\W_]',' ',doc)
  #print(f"get_doc_vector_word 1:{doc}")
  
  # split into words
  doc_words = doc.split()
  #print(f"get_doc_vector_word 2:{doc}")
  #pprint(doc_words)
  
  # create vector
  vector = Counter()
  for w in doc_words:
    vector[w] += 1
  
  #print("get_doc_vector_word 3:")
  #pprint(vector)
    
  return vector
  
  
def get_doc_vector_seq2(doc):
  # remove non alphanumeric and white space
  
  # split into 2 character sequnces 
  
  # create vector
  return None  
  
  

  

def main():
  pass


if __name__ == '__main__':
        
    #pprint(get_list_of_file_extensions())
    # pathlib example - use

    media_lib = ''
    media_lib = MMdia.refresh_media_files_information(mmdia_root)
    
     
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
        
    
    # saving object to disk
    # marshal.dump / load docs say use pickle
    # pickle (marshal/store) media_lib to mmdia_root
    # https://docs.python.org/3/library/pickle.html#module-pickle
    # https://docs.python.org/3/library/pickle.html#pickling-class-instances
    
    # target Path
    picked_media_lib_file = mmdia_root.joinpath('media_data','medialib.pickle')
    
    # create directory if it doesn't exist
    picked_media_lib_file.parent.mkdir(parents=True, exist_ok=True)
    
    # write lib to disk - save rebuild all on every run
    #if len(media_lib) > 0:
    print(f"SIZE: {media_lib['video'].keys()} - {len(media_lib['video'].keys())} - {type(media_lib)}")
    print(f"len(media_lib): {len(media_lib)}")
    print(f"picked_media_lib_file: {picked_media_lib_file}")
    
    print(f"PICKLING to {picked_media_lib_file}")
    with open(picked_media_lib_file, 'wb') as f:
      pickle.dump(media_lib, f, pickle.HIGHEST_PROTOCOL)
    
    media_lib = None
    
    print(f"\n\nUN-PICKLING from {picked_media_lib_file}")
    with open(picked_media_lib_file, 'rb') as f:
      media_lib = pickle.load(f)
    
    print(f"SIZE: {media_lib['video'].keys()} - {len(media_lib['video'].keys())} - {type(media_lib)}")
    print(f"len(media_lib): {len(media_lib)}")
    print(f"picked_media_lib_file: {picked_media_lib_file}")
      
    # 
    #print(json.dumps(media_lib))   #MMdia not serializable
    #print(MMdia.JSON_DUMP)
    #       
    # # create JSON for easy flask import (DB interrim)
    # with open(MMdia.JSON_DUMP, "w") as f:      
    #   f.write(json.dumps(media_lib)

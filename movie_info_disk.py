#! /usr/bin/env python
from pathlib import Path
from collections import Counter
from pprint import pprint
import re
import json
import imdb    


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
      'runtime': 0,
      'rating':0,
      'genre':[],
      'kind':[],
      'seen': False,
      'fav':False
    }
    self.get_media_name_and_year_from_disc()
    #st_size

  def to_s(self):
    print

  def query_imdb_for_movie_info(self):
    pass
    # self.movie_data = {
    #   'id': None,
    #   'title': '',
    #   'synopsis': '',
    #   'year': 0,
    #   'cast': [],
    #   'runtime': 0,
    #   'rating':0,
    #   'genre':[],
    #   'kind':[],
    #   'seen': False,
    #   'fav':False
    # }
    ia = imdb.IMDb()      # instantiation cost?
#     
# integrate. . . 
#     media_title = 'Joker'
#     media_year = '2019'
#     query = f"{media_title} {media_year}"
#     
#     print(f"\n\n\nRetieving info from IMDB\nSearching fror: {query} <")
#     results = ia.search_movie(query)
# 
#     for m in results:
#       pprint(m)
#       
#     # return result with highest Doc Distance with search
#     movie = results[0]
#     m = ia.get_movie(results[0].movieID)
    
    

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
        self.movie_data['title'] = dirty_title
        
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
    vid = '/here/i/am/Ghostbusters.1984.Remastered.1080p.mp4'
    print(f"AUDIO?: {MMdia.is_audio('Atominc Fusion Corp.mp3')}")
    print(f"VIDEO?: {MMdia.is_video('Atominc Fusion Corp.ac3')}")        
    print(f"AUDIO?: {MMdia.is_audio('Ghostbusters.1984.Remastered.1080p.mp4')}")
    print(f"VIDEO?: {MMdia.is_video('Ghostbusters.1984.Remastered.1080p.mp4')}")
    print(f"AUDIO?: {MMdia.is_audio(vid)}")
    print(f"VIDEO?: {MMdia.is_video(vid)}")
    print(f"Path:  {Path(vid).parent}")
    print(f"Name:  {Path(vid).name}")
    print(f"Ext:   {Path(vid).suffix}")        
    
    pprint(Path(r'/Volumes/FAITHFUL500/15_rpi_shortlist/The Last Thing He Wanted (2020) [720p] [WEBRip] [YTS.MX]/The.Last.Thing.He.Wanted.2020.720p.WEBRip.x264.AAC-[YTS.MX].mp4').stat())
    
    t = 'first.man.'
    print(re.sub(r'[\W_]*$','',t))
    t = '(^*)a.pistol.shooter.dies.'
    u = re.sub(r'^[\W_]*','',t)
    print(re.sub(r'\.',' ',u).strip())
    t = '._a.star.is.born.'
    print(re.sub(r'^[\W_]*','',t))


    media_lib = MMdia.refresh_media_files_information(mmdia_root)
    
    #pprint(media_lib['video'])
    #pprint(media_lib['audio'])
    ##MMdia.dump_bad_names()
    
    for i,k in enumerate(media_lib['video'].keys()):
      if len(media_lib['video'][k].movie_data['title']) == 0: continue        # skip titles of zero length - curate later
      print(f"\n\ndisk: {k} <")
      pprint(media_lib['video'][k])               # TODO ex - use metaclass to dump object attributes
      print(media_lib['video'][k].movie_data['title'], len(media_lib['video'][k].movie_data['title']))
      print(media_lib['video'][k].movie_data['year'])
      print(media_lib['video'][k].file_stat)
      print(f"{int(media_lib['video'][k].file_stat.st_size/(1024*1024))}MiB")
      print(f"{round(media_lib['video'][k].file_stat.st_size/(1024*1024*1024),1)}GiB")
      if i > 20: break
    
            
    # 
    #print(json.dumps(media_lib))   #MMdia not serializable
    #print(MMdia.JSON_DUMP)
    #       
    # # create JSON for easy flask import (DB interrim)
    # with open(MMdia.JSON_DUMP, "w") as f:      
    #   f.write(json.dumps(media_lib)

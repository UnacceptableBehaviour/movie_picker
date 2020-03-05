#! /usr/bin/env python
from pathlib import Path
from collections import Counter
from pprint import pprint
import re
import json
    


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
    self.media_title = None
    self.media_year = None
    self.get_media_name_and_year()
    self.seen = False
    #st_size

  def to_s(self):
    print

  def get_media_name_and_year(self):
    #if self.is_video(self.filename):
    if self.obj_is_video():
      # movies
      # looking for: name followed by year or (year) or [year] resolution bla bla .ext
      # r'[\(\)\[\]]?\d\d\d\d[\(\)\[\]]?[\.\b]' - 4 digit year followed by . or word boundary      
      match = re.search(r'(.*?)[\(\)\[\]]?(\d\d\d\d)[\(\)\[\]]?[\.\b]', self.filename, re.I )
      if match:
        self.media_year = match.group(2)
        dirty_title = match.group(1)
        dirty_title = re.sub(r'^[\W_]*','',dirty_title)     # remove leading non word
        dirty_title = re.sub(r'[\W_]*$','',dirty_title)     # remove trailing non word
        dirty_title = re.sub(r'[\._]',' ',dirty_title)      # replace . and underscore with space
        self.media_title = dirty_title
        
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
    
    for k in media_lib['video'].keys():
      print(f"\n\n\ndisk: {k} <")
      pprint(media_lib['video'][k])               # TODO ex - use metaclass to dump object attributes
      print(media_lib['video'][k].media_title)
      print(media_lib['video'][k].media_year)
    
            
    # 
    #print(json.dumps(media_lib))   #MMdia not serializable
    #print(MMdia.JSON_DUMP)
    #       
    # # create JSON for easy flask import (DB interrim)
    # with open(MMdia.JSON_DUMP, "w") as f:      
    #   f.write(json.dumps(media_lib)

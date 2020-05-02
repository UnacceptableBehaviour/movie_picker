#! /usr/bin/env python
# from pathlib import Path
# from collections import Counter
from pprint import pprint
# import re
from pathlib import Path

# touch __init__.py in directory that is to be module to allow inport of class
# this creats an empty file that will add the driectory to the import path
from movie_info_disk import MMdia       

import copy

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# helpers
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

PATH_TO_LIB = Path('/Volumes/time_box_2018/movies/')
PATH_TO_TOR = Path('/Volumes/meep/temp_delete/tor')

def main():
  pass


if __name__ == '__main__':
    
    time_box = copy.deepcopy(MMdia.refresh_media_files_information(PATH_TO_LIB))
    # for i,f in enumerate(time_box['video']):
    #   pprint(f)
    
    #pprint(time_box)
    #pprint(time_box['video']['blindspotting.2018.hdrip.xvid-etrg.avi'])
    #pprint(time_box['video']['blindspotting.2018.hdrip.xvid-etrg.avi'].movie_data)
    
    #pprint(time_box['video'])
    
    fs_tor   = MMdia.refresh_media_files_information(PATH_TO_TOR, True)
    
    removal_list = []
    
    for movie,media in fs_tor['video'].items():
      file_size = round(fs_tor['video'][movie].file_stat.st_size / (1024 * 1024),1)
      if file_size > 400:
        if movie in time_box['video']:
          print(f"\n\ \nFound:\n{movie}\nfs_tor:{fs_tor['video'][movie]}\ntime_box:{time_box['video'][movie]}")
          print(f"{file_size}MB")
          removal_list.append(movie)
        else:
          print(f"\nunique:{movie} on fs_tor")
          print(f"{file_size}MB")
    
    for m in removal_list:
      print(m)
    print(len(removal_list))
    
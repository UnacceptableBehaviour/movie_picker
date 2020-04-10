#! /usr/bin/env python
# from pathlib import Path
# from collections import Counter
from pprint import pprint
# import re
from pathlib import Path

# touch __init__.py in directory that is to be module to allow inport of class
# this creats an empty file that will add the driectory to the import path
from movie_info_disk import MMdia       



# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# helpers
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

PATH_TO_LIB = Path('/Volumes/time_box_2018/movies/')
PATH_TO_TOR = Path('/Volumes/meep/temp_delete/tor')




def main():
  pass


if __name__ == '__main__':
    
    time_box = MMdia.refresh_media_files_information(PATH_TO_LIB)
    # for i,f in enumerate(time_box['video']):
    #   pprint(f)
    
    #pprint(time_box)
    #pprint(time_box['video']['blindspotting.2018.hdrip.xvid-etrg.avi'])
    #pprint(time_box['video']['blindspotting.2018.hdrip.xvid-etrg.avi'].movie_data)
    
    pprint(time_box['video'])
    
    #fs_tor   = MMdia.refresh_media_files_information(PATH_TO_TOR)
    
    
    
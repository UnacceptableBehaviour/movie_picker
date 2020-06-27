#! /usr/bin/env python
# from pathlib import Path
# from collections import Counter
from pprint import pprint
import re
import sys    
from pathlib import Path

import wget                 # method 1
import urllib.request       # method 2 & 3
import shutil               # method 3

# method 1 - get
# pip install wget
# import wget
# wget.download(url, '/Users/scott/Downloads/cat4.jpg') 

# method 2 - considered legacy - depracated
# import urllib.request
# urllib.request.urlretrieve(url, file_name)

# method 3
# import urllib.request
# import shutil
# ...
# # Download the file from `url` and save it locally under `file_name`:
# with urllib.request.urlopen(url) as response, open(file_name, 'wb') as out_file:
#     shutil.copyfileobj(response, out_file)


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# helpers
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
  

def main():
    pass


if __name__ == '__main__':
    
    
    # get image from blog
    oxtail_pie_url = 'http://1.bp.blogspot.com/-CsuV9w1jVZw/XGQI4b6hYZI/AAAAAAAAL1k/Si7tvX9fGswX2xlUg1C7SGICTHIxvyEkACK4BGAYYCw/s1600/DSC_0111.jpg'
    octopus_url = 'http://3.bp.blogspot.com/-IOb-6l0hmBM/WCDs8TJ_8_I/AAAAAAAAGe8/OZBl9KfaHNE-705ybXJ6TFiSsztUo7nRwCK4B/s1600/ferdiesfoodlab%2B-%2Blondon%2Bsupper%2Bclub%2B-%2Bsimon%2Bfernandez%2B-%2Bparties%2B-07_y048_lobster_octopus_carpaccio.jpg'
    tagteli_url = 'http://2.bp.blogspot.com/-SAw1c1b-dns/XGgXqgSxLqI/AAAAAAAAL3I/QsFAm5SOib4LXDyH3Ar0VIuHAYpXFZBIACK4BGAYYCw/s1600/veggie%2B-%2Bartichoke%2Band%2Basparagus%2Btagliatelle.jpg'
    
    # save to path
    save_as = Path('/Users/simon/a_syllabus/lang/python/repos/movie_picker/scratch/test_img.jpg')
    
    # method 1 - default behaviour: if target exits the file created had (1) in brakets after it - polution!
    save_as = Path('/Users/simon/a_syllabus/lang/python/repos/movie_picker/scratch/test_img_1_get.jpg')
    url = oxtail_pie_url
    wget.download(url, str(save_as)) 
        
    # method 2
    save_as = Path('/Users/simon/a_syllabus/lang/python/repos/movie_picker/scratch/test_img_2_urlretrieve.jpg')
    url = octopus_url
    urllib.request.urlretrieve(url, str(save_as))
    
    # method 3
    save_as = Path('/Users/simon/a_syllabus/lang/python/repos/movie_picker/scratch/test_img_3_urlopen.jpg')
    url = tagteli_url
    with urllib.request.urlopen(url) as response, open(save_as, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)

    # method 3 - wikipedia instead of blog
    save_as = Path('/Users/simon/a_syllabus/lang/python/repos/movie_picker/scratch/test_img_4_urlopen_wiki.jpg')
    url = 'https://en.wikipedia.org/wiki/The_Call_of_the_Wild_(2020_film)#/media/File:The_Call_of_the_Wild_poster.jpg' # fails
    
    with urllib.request.urlopen(url) as response, open(save_as, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)
    
    # method 1 - wiki - default behaviour: if target exits the file created had (1) in brakets after it - polution!
    save_as = Path('/Users/simon/a_syllabus/lang/python/repos/movie_picker/scratch/test_img_5_wiki_get.jpg')
    url = 'https://upload.wikimedia.org/wikipedia/en/4/43/The_Call_of_the_Wild_poster.jpg'
    wget.download(url, str(save_as)) 
        
    # method 2 - wiki 
    save_as = Path('/Users/simon/a_syllabus/lang/python/repos/movie_picker/scratch/test_img_6_wiki_urlretrieve.jpg')
    url = 'https://upload.wikimedia.org/wikipedia/en/4/43/The_Call_of_the_Wild_poster.jpg'
    urllib.request.urlretrieve(url, str(save_as))
    
    # method 3 - wiki
    save_as = Path('/Users/simon/a_syllabus/lang/python/repos/movie_picker/scratch/test_img_7_wiki_urlopen.jpg')
    url = 'https://upload.wikimedia.org/wikipedia/en/4/43/The_Call_of_the_Wild_poster.jpg'
    with urllib.request.urlopen(url) as response, open(save_as, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)
        
    # # method 3 - wikipedia instead of blog
    # url = 'https://upload.wikimedia.org/wikipedia/en/4/43/The_Call_of_the_Wild_poster.jpg'
    # save_as = Path('/Users/simon/a_syllabus/lang/python/repos/movie_picker/scratch/test_img_5_get_wiki.jpg')    
    # wget.download(url, str(save_as))
    # 
    # headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}
    
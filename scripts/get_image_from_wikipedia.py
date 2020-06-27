#! /usr/bin/env python
# from pathlib import Path
# from collections import Counter
from pprint import pprint
import re
import wikipedia  # API for wikipedia - pip install wikipedia
                  # 
                  # 
                  # 
import sys    
import urllib.request
from pathlib import Path
    

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# helpers
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
  

def main():
    pass


if __name__ == '__main__':
    
    #print(sys.path)
    #'/Users/simon/a_syllabus/lang/python/repos/movie_picker/venv/lib/python3.7/site-packages'
    # scraping movie info for local app
     
    wikipedia.set_lang('en')
    
    searches = [#'Blade Runner 2049 (2049 film)',
                #'The Invisible Man (2020 film)',
                'Mary Queen of Scots (2019 film)',
                'The Call of the Wild (2020 film)',
                'The Banker (2020 film)',
                'The Last Thing He Wanted (2020 film)',
                #'Star Wars: Episode IX - The Rise of Skywalker (2020 film)',
                #'The Hustle (2019 film)',
                'The Great Hack (2019 film)',
                'The Man Who Killed Hitler and Then the Bigfoot (2019 film)',
                #'The Irishman (2019 film)',
                'The Art of Self-Defense (2019 film)',  # 11
                #'Spider-Man: Far from Home (2019 film)',
                #'Shazam! (2019 film)',
                #'Shaft (2019 film)',
                'Ready or Not (2019 film)',
                'Parasite (2019 film)',
                #'Once Upon a Time... in Hollywood (2019 film)',
                'Men in Black: International (2019 film)']
    
    
    
    #print( wikipedia.summary("Wikipedia") )
    #moviesearch = searches[0]
    scrape_targets = []
    
    for moviesearch in searches:
        print(f"- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  Search: {moviesearch}")
        try:
            page_result = wikipedia.page(moviesearch)    
        except:
            moviesearch = re.sub('(\d\d\d\d film)', 'film', moviesearch)
            search_results = wikipedia.search(moviesearch)
            print(f"PAGE FAILED - SEARCHING - - - - - - - -wikipedia.search({moviesearch})")
            print(search_results[0])
            print(search_results)
            page_result = wikipedia.page(search_results[0])    
            # print("\n- - - - - - - -wikipedia.search().url")
            # pprint(page_result.url)    
            # print("\n- - - - - - - -page_result.images")
            # print(page_result.images)
        print("\n- - - - - - - -wikipedia.page()")
        print(page_result)
        print("\n- - - - - - - -wikipedia.page().url")
        pprint(page_result.url)
        possible_image_url = ''
        try:
            print("\n- - - - - - - -page_result.images")
            print(page_result.images)            
            for img in page_result.images:
                if 'poster' in str(img):
                    possible_image_url = img
                    print(img)
                else:
                    print('.', end='')
        except KeyError:
            scrape_targets.append(page_result.url)
            print(f"NO IMAGES FOR: {moviesearch}")
            
        
        search_results = wikipedia.search(moviesearch)
        print("\n- - - - - - - -wikipedia.search()")
        print(search_results[0])        
        print(search_results)
        # print("\n- - - - - - - -wikipedia.search().url")
        # pprint(page_result.url)    
        # print("\n- - - - - - - -page_result.images")
        # print(page_result.images)
        
        print(f"\n- - - - - - - -retrieving image\n{possible_image_url}")
        img_path = Path('/Users/simon/a_syllabus/lang/python/repos/movie_picker/scratch/')
        try:
            filename = possible_image_url.split('/')[-1]    
            # print(img_path)
            # print(filename)
            print(img_path.joinpath(filename))
            urllib.request.urlretrieve(possible_image_url, img_path.joinpath(filename))
        except:
            print(f"NAUSE UP {filename} <")
            print(img_path.joinpath(filename))
            pass
    
    print("\nscrape_targets:")
    print(scrape_targets)
    
    
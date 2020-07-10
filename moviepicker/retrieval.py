#! /usr/bin/env python
from pprint import pprint
import re
import sys    
from pathlib import Path

from urllib.parse import unquote  # comvert Annihilation_%28film%29.png to Annihilation_(film).png

#TODO remove DEBUG
print(" - - - - - - - - import exceptions into retrieval.py - - - - < < S")
print(dir())
print("__name__",__name__)
from exceptions import IncorrectURLForImageRetrieval
print(" - - - - - - - - import exceptions into retrieval.py - - - - < < E")
#TODO remove DEBUG

import urllib.request
import shutil
from bs4 import BeautifulSoup        # https://www.crummy.com/software/BeautifulSoup/bs4/doc/ 
import wikipedia
wikipedia.set_lang('en')

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# helpers
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# from retrieval import get_hires_cover, find_wiki_url_for_movie, get_lead_image_from_wikipedia

def find_wiki_url_for_movie(title, year):
    
    if title == None:
        return 
        
    moviesearch = f"{title} ({year} film)"

    movie_url = ''    
    print(f"Finding URL for: {moviesearch}")
    
    try:
        page_result = wikipedia.page(moviesearch)
        movie_url = page_result.url
    except wikipedia.exceptions.PageError:
        try:
            moviesearch = re.sub('(\d\d\d\d film)', 'film', moviesearch)
            search_results = wikipedia.search(moviesearch)
            print(f"PAGE FAILED - SEARCHING - - - - - - - -wikipedia.search({moviesearch})")
            print(search_results[0])
            print(search_results)
            page_result = wikipedia.page(search_results[0])  
            movie_url = page_result.url
        except (wikipedia.exceptions.PageError, IndexError):
            print(f"ALSO FAILED - - - - - - - - - {moviesearch} < WARNING**")
    
    print(f"movie_url: {movie_url}")
    
    return movie_url


def get_lead_image_from_wikipedia(url, save_as_path):
    save_as_path = Path(save_as_path) if save_as_path else Path('')
    image_href = ''
    full_img_url = 'https:'
    page = urllib.request.urlopen(url)
    
    soup = BeautifulSoup(page, 'html.parser')
    
    info_pane = soup.find('table', attrs={'class': 'infobox vevent'})

    if info_pane:    
        row_tds = info_pane.find_all('td')
        
        for row_td in row_tds:
            try:
                if row_td.a.img != None:
                    print(f"src - {row_td.a.img.get('src')}")
                    print(f"srcset - {row_td.a.img.get('srcset')}")
                    if row_td.a.img.get('srcset') == None:
                        image_href = row_td.a.img.get('src')
                    else:
                        image_href = row_td.a.img.get('srcset').split(' ')[0]
                    break
            except AttributeError:
                return(save_as_path) 
        
    full_img_url = full_img_url + image_href

    filename = full_img_url.split('/')[-1]
    
    filename = unquote(filename)
    
    save_as_path = save_as_path.joinpath(filename)

    try:
        with urllib.request.urlopen(full_img_url) as response, open(save_as_path, 'wb') as out_file:
            shutil.copyfileobj(response, out_file)
            if save_as_path.exists():                   # check it saved & delete temp in local dir
                print(f"SAVED to {save_as_path}")
                
    except urllib.error.URLError as e:
        msg = "Incorrect URL for image retrieval"
        print(f"\n**\nget_lead_image_from_wikipedia: {msg},\n{full_img_url}\n**\n")
        #raise IncorrectURLForImageRetrieval(msg, full_img_url)
    finally:
        pass
    
    print(f"GOT: {save_as_path.name}")
    return(save_as_path)
    
    
def get_hires_cover(title, year, save_as_path):
    ret_val = None
    file_path = ''
    movei_url = ''
    
    movei_url = find_wiki_url_for_movie(title, year)    
        
    if movei_url != '':
        file_path = get_lead_image_from_wikipedia(movei_url, save_as_path)
    
    if Path(file_path).exists():
        ret_val = file_path
    
    return ret_val



searches = [('Blade Runner 2049','2020'),
            ('The Invisible Man','2020'),
            ('Mary Queen of Scots','2019'),
            ('The Call of the Wild','2020'),
            ('The Banker','2020'),
            ('The Last Thing He Wanted','2020'),
            ('Star Wars: Episode IX - The Rise of Skywalker','2020'),
            ('The Hustle','2019'),
            ('The Great Hack','2019'),
            ('The Man Who Killed Hitler and Then the Bigfoot','2019'),
            ('The Irishman','2019'),
            ('The Art of Self-Defense','2019'),  # 11
            ('Spider-Man: Far from Home','2019'),
            ('Shazam!','2019'),
            ('Shaft','2019'),
            ('Ready or Not','2019'),
            ('Parasite','2019'),
            ('Once Upon a Time... in Hollywood','2019'),
            ('Men in Black: International','2019')]    
    
    

def main():
    pass


if __name__ == '__main__':
    
    for title, year in searches:    
        result = get_hires_cover(title, year, Path('/Users/simon/a_syllabus/lang/python/repos/movie_picker/scratch/'))
        print(f"Saught: {title} - {year} - GOT: {result.name}\n{result}")
    
    sys.exit()

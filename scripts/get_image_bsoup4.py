#! /usr/bin/env python
# from pathlib import Path
# from collections import Counter
from pprint import pprint
import re
import sys    
#import urllib.request
from pathlib import Path

# https://towardsdatascience.com/in-10-minutes-web-scraping-with-beautiful-soup-and-selenium-for-data-professionals-8de169d36319

import urllib.request                       # API for BeautifulSoup - pip install BeautifulSoup4
import shutil                               #
from bs4 import BeautifulSoup               # https://www.crummy.com/software/BeautifulSoup/bs4/doc/
                                            # 
import wikipedia                            # 
wikipedia.set_lang('en')

# import urllib.request
# import shutil
# ...
# # Download the file from `url` and save it locally under `file_name`:
# with urllib.request.urlopen(url) as response, open(file_name, 'wb') as out_file:
#     shutil.copyfileobj(response, out_file)                  
                  
                  
    

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# helpers
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

def find_wiki_url_for_movie(title, year):
    moviesearch = f"{title} ({year} film)"

    movie_url = ''    
    print(f"Finding URL for: {moviesearch}")
    
    try:
        page_result = wikipedia.page(moviesearch)
        movie_url = page_result.url
    except:
        moviesearch = re.sub('(\d\d\d\d film)', 'film', moviesearch)
        search_results = wikipedia.search(moviesearch)
        print(f"PAGE FAILED - SEARCHING - - - - - - - -wikipedia.search({moviesearch})")
        print(search_results[0])
        print(search_results)
        page_result = wikipedia.page(search_results[0])  
        movie_url = page_result.url
    
    print(f"movie_url: {movie_url}")
    
    return movie_url


def get_lead_image_from_wikipedia(url, save_as_path):
    image_href = ''
    page = urllib.request.urlopen(url)
    
    soup = BeautifulSoup(page, 'html.parser')
    
    info_pane = soup.find('table', attrs={'class': 'infobox vevent'})
    
    rows = info_pane.find_all('tr')
    
    for row in rows:
        text = row.text.strip().lower()        
        if ('theatrical release poster' in text) or ('official release poster' in text):
            print(f"src - {row.a.img.get('src')}")
            print(f"srcset - {row.a.img.get('srcset')}")
            if row.a.img.get('srcset') == None:
                image_href = row.a.img.get('src')
            else:
                image_href = row.a.img.get('srcset').split(' ')[0]
    
    full_img_url = 'https:' + image_href

    filename = full_img_url.split('/')[-1]
    
    save_as_path = save_as_path.joinpath(filename)

    with urllib.request.urlopen(full_img_url) as response, open(save_as_path, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)      
    
    print(f"GOT: {save_as_path.name}")
    return(save_as_path)
    
    

url_targets = ['https://en.wikipedia.org/wiki/Mary_Queen_of_Scots_(2018_film)',
               'https://en.wikipedia.org/wiki/The_Call_of_the_Wild_(2020_film)',
               'https://en.wikipedia.org/wiki/The_Banker_(2020_film)',
               'https://en.wikipedia.org/wiki/The_Last_Thing_He_Wanted_(film)',
               'https://en.wikipedia.org/wiki/The_Great_Hack',
               'https://en.wikipedia.org/wiki/The_Art_of_Self-Defense_(2019_film)',
               'https://en.wikipedia.org/wiki/Ready_or_Not_(2019_film)']
    
def get_hires_cover(title, year, save_as_path):
    ret_val = None
    
    movei_url = find_wiki_url_for_movie(title, year)    
    
    # for movei_url in url_targets:
    #     print(f"retrieving image: {movei_url}")
    #     file_path = get_lead_image_from_wikipedia(movei_url, save_as_path)
    
    file_path = get_lead_image_from_wikipedia(movei_url, save_as_path)
    
    if Path(file_path).exists():
        ret_val = file_path
    
    return file_path

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

    # # comment back in to run image retrieval from (title, year)    
    # for title, year in searches:    
    #     result = get_hires_cover(title, year, Path('/Users/simon/a_syllabus/lang/python/repos/movie_picker/scratch/'))
    #     print(f"Saught: {title} - {year} - GOT: {result.name}\n{result}")
    # 
    # sys.exit()
    

    
    url_targets = ['https://en.wikipedia.org/wiki/Mary_Queen_of_Scots_(2018_film)',
                   'https://en.wikipedia.org/wiki/The_Call_of_the_Wild_(2020_film)',
                   'https://en.wikipedia.org/wiki/The_Banker_(2020_film)',
                   'https://en.wikipedia.org/wiki/The_Last_Thing_He_Wanted_(film)',
                   'https://en.wikipedia.org/wiki/The_Great_Hack',
                   'https://en.wikipedia.org/wiki/The_Art_of_Self-Defense_(2019_film)',
                   'https://en.wikipedia.org/wiki/Ready_or_Not_(2019_film)']
    
    
    page = urlopen(url_targets[1])
    
    soup = BeautifulSoup(page, 'html.parser')
        
    # target node that preceeds "Theatrical release poster"
    # <tr>
    #     <td colspan="2" style="text-align:center">
    #         <a href="/wiki/File:The_Call_of_the_Wild_poster.jpg" class="image"><img alt="The Call of the Wild poster.jpg" src="//upload.wikimedia.org/wikipedia/en/thumb/4/43/The_Call_of_the_Wild_poster.jpg/220px-The_Call_of_the_Wild_poster.jpg" decoding="async" width="220" height="348" class="thumbborder" srcset="//upload.wikimedia.org/wikipedia/en/4/43/The_Call_of_the_Wild_poster.jpg 1.5x" data-file-width="251" data-file-height="397"></a>
    #         <div style="font-size:95%;padding:0.35em 0.35em 0.25em;line-height:1.25em;">Theatrical release poster</div>
    #     </td>
    # </tr>
    
    # sidebar_title
    # <th> class="summary"
    sidebar_title = soup.find('th', attrs={'class': 'summary'}) # get element by tag type & class
    sidebar_title_txt = sidebar_title.text.strip()
    print(f'sidebar_title_txt: {sidebar_title_txt} <')
    
    # release_date_row    
    # <tr> text = 'Release date'
    release_date_row = soup.find('tr', attrs={'text': 'Release date'})
    #release_date_row_txt = release_date_row.text.strip()
    #print(f'release_date_row_txt: {release_date_row_txt} <')
    
    # 
    info_pane = soup.find('table', attrs={'class': 'infobox vevent'})
    rows = info_pane.find_all('tr')
    image_href = ''
    for row in rows:
        print("\n========================> rows")
        pprint(row)
        print(dir(row))
        pprint(row.attrs)
        print('---')
    print("====> rows")
    for i,row in enumerate(rows):
        print(f"\n>= {i} =")
        text = row.text.strip().lower()
        print(f"={i}= {text} <{'theatrical release poster' in text}>")
        if 'theatrical release poster' in text:
            print(row.get('href'))
            print(row.a.get('href'))
            print(f"src - {row.a.img.get('src')}")
            print(f"srcset - {row.a.img.get('srcset')}")                    # sequence of nodes
            image_href = row.a.img.get('srcset').split(' ')[0]
        print(row.text.strip())
        print(row.a)
        print(row.td)
    
# url_target 'https://en.wikipedia.org/wiki/The_Call_of_the_Wild_(2020_film)'
            # https://en.wikipedia.org/wiki/The_Call_of_the_Wild_(2020_film)#/media/File:The_Call_of_the_Wild_poster.jpg
                                                                            # /wiki/File:The_Call_of_the_Wild_poster.jpg
            # https://upload.wikimedia.org/wikipedia/en/4/43/The_Call_of_the_Wild_poster.jpg
    # https://upload.wikimedia.org/wikipedia/en/4/43/The_Call_of_the_Wild_poster.jpg
    image = info_pane.find_all('a', attr={'class':'image'})
    print(image)
    
    for link in info_pane.find_all('a'):
        print(link.get('href'))
        print(link['href'])
    
    full_img_url = 'https:' + image_href
    
    print(f"theatrical release poster - match: {image_href} <\n {full_img_url} <")
    possible_image_url = full_img_url

    print(f"\n- - - - - - - -retrieving image\n{full_img_url}")
    img_path = Path('/Users/simon/a_syllabus/lang/python/repos/movie_picker/scratch/')
    save_as = ''
    try:
        filename = possible_image_url.split('/')[-1]    
        print(img_path)
        print(filename)
        save_as = img_path.joinpath(filename)
        print(save_as)
        urllib.request.urlretrieve(possible_image_url, save_as)
    except Exception as err:
        print(repr(err))
        print(f"NAUSE UP {filename} <")
        print(img_path.joinpath(filename))
        pass    

    
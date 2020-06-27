#! /usr/bin/env python
# from pathlib import Path
# from collections import Counter
from pprint import pprint
import re
import sys    
#import urllib.request
from pathlib import Path

# https://towardsdatascience.com/in-10-minutes-web-scraping-with-beautiful-soup-and-selenium-for-data-professionals-8de169d36319
from urllib.request import Request, urlopen # API for BeautifulSoup - pip install BeautifulSoup4
import urllib.request
from bs4 import BeautifulSoup               # https://www.crummy.com/software/BeautifulSoup/bs4/doc/
                                            # 
#import wikipedia                           # 
                  
                  
                  
    

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# helpers
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
  

def main():
    pass


if __name__ == '__main__':
    
    #print(sys.path)
    #'/Users/simon/a_syllabus/lang/python/repos/movie_picker/venv/lib/python3.7/site-packages'
    # scraping movie info for local app
    
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
            print(f"srcset - {row.a.img.get('srcset')}")
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

    
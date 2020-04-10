#! /usr/bin/env python
# from pathlib import Path
# from collections import Counter
from pprint import pprint
# import re
import imdb     # API for imdb - pip install IMDbPY
                # https://imdbpy.readthedocs.io/en/latest/usage/movie.html#movies
                # downloadable S3 datasets for postgres or mariadb:
                #       https://imdbpy.readthedocs.io/en/latest/usage/s3.html#s3
    



# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# helpers
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
  

def main():
  pass


if __name__ == '__main__':
    
    # scraping movie info for local app
        
    media_title = 'Joker'
    media_year = '2019'
    
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # BY SCRAPING
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # for Joker 2019 
    # query for
    # TITLE	<h1> text
    #       movie.get('title')
    # YEAR  <span id="titleYear">
    # CONTENT TYPE
    #   <a href="/search/title?genres=thriller&amp;explore=title_type,genres&amp;ref_=tt_ov_inf">Thriller</a> (one link for each genre)
    #   more than 1
    # PLAY TIME <time datetime="PT122M">2h 2min</time>
    # RATING    <span itemprop="ratingValue">8.6</span>
    # IMAGE     <div class="poster">
    #             <a href="/title/tt7286456/mediaviewer/rm3353122305?ref_=tt_ov_i"> 
    #               <img alt="Joker Poster" title="Joker Poster" src="https://m.media-amazon.com/images/GUID_BLA_BLA_.jpg">
    #             </a>
    # SYNOPSIS
    

    
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # USING imdb module
    # Usage (keys): https://imdbpy.readthedocs.io/en/latest/usage/movie.html#movies
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    
    ia = imdb.IMDb()
    
    media_title = 'Joker'
    media_year = '2019'
    query = f"{media_title} {media_year}"
    
    print(f"\n\n\nRetieving info from IMDB\nSearching fror: {query} <")
    results = ia.search_movie(query)

    print("Found:")
    for i,m in enumerate(results):
      print(i, m)  
    
    chosen = 0
    # chosen = input(f"Select result from 0 - {len(results)-1} (default 0):")
    # if chosen == '' : chosen = 0    
    # chosen = int(chosen)
      
    # return result with highest Doc Distance with search
    #movie = results[chosen]
    m = ia.get_movie(results[chosen].movieID)
    print(ia.get_movie_infoset())
    
    print(f"ID: {m.movieID}")
    print(f"Title: {m.get('title')}")
    print(f"Title: {m['title']}")
    print(f"Rating: {m['rating']}")
    print(f"Runtimes: {m['runtimes']} or {int(m['runtimes'][0])%60}h{int(m['runtimes'][0])%60}")
    print(m.current_info)
    
    # m.get('plot') - list of str (7 in this case all diffferent)
    for synopsis in m.get('plot'):
      print(f"SYNOPSIS:\n{synopsis}")
    
    # this is actually the plot - massive
    # print(f"\nSYNOPSIS:\n{m.get('synopsis')}")
    
    print(f"GENRES?: {'genres' in m}")
    if 'genres' in m: print(m['genres'])
    print(f"KIND: {m['kind']}")
    
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
    # from scrape
    # https://www.imdb.com/title/tt7286456/mediaviewer/rm3353122305
    #                          ID: 7286456
    #                       Title: Joker
    
    
    
    
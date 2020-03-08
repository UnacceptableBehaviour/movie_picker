# movie_picker
build movie library into flask web interface allows browsing and playing of movie

## Status: Build as quickly / simply as possible . . 
[AMBER]

## Abstract
Turn and old tv (without a remote) and a 2.5 inch usb hard disc with DVD collection stored on it into a home cinema using a raspberry pi as a webserver, and an old tablet for a remote. 

## Contents  
1. [Status: Build as quickly / simply as possible . .](#status-build-as-quickly--simply-as-possible--)  
2. [Abstract](#abstract)  
3. [Contents](#contents)  
4. [AIM:](#aim)  
5. [Next steps](#next-steps)  
6. [Questions / Barriers](#questions--barriers)  
	1. [How do we scrape IMDB for movie info to display?](#how-do-we-scrape-imdb-for-movie-info-to-display)  
7. [How To's](#how-tos)  
	1. [How to do initial git repo setup for simple Flask app](#how-to-do-initial-git-repo-setup-for-simple-flask-app)  
	2. [How do we access IMDB for movie info to display?](#how-do-we-access-imdb-for-movie-info-to-display)  
	3. [Whats teh minimum serach info required for sensible results?](#whats-teh-minimum-serach-info-required-for-sensible-results)  
	4. [How do I auto generate TOC?](#how-do-i-auto-generate-toc)  
	5. [How do I insert a TOC?](#how-do-i-insert-a-toc)  
8. [TIPS](#tips)  
9. [REFERENCES](#references)  
10. [Completed](#completed)  


## AIM:
A little python practice, scraping, flask, basic web.

## Next steps
X-ref search result and query using doc_ditsance to get nearest match
Make MMdia serializable - w/ meta class? (allow to and from JSON/DUMPS)
Build DB / non-valatile storage (JSON file will do to start).
Display information using flask & boostrap cards.
Allow toggling of favourite icon, seen it icon


## Questions / Barriers
### How do we scrape IMDB for movie info to display?



## How To's
### How to do initial git repo setup for simple Flask app
```
> git add .gitignore			# add config file - which dir/files to track/ignore
> git commit -m'update config'
> git push
> python3 -m venv venv			# setup python 3 virtual env
> .pe							# activate environment - alias .pe='. venv/bin/activate'
> pip install --upgrade pip		# update pip 
> nano requirements.txt			# add following to text file
Click==7.0
Flask==1.0.3
httplib2==0.17.0
IMDbPY==6.8
itsdangerous==1.1.0
Jinja2==2.10.1
lxml==4.5.0
MarkupSafe==1.1.1
pathlib==1.0.1
SQLAlchemy==1.3.13
striprtf==0.0.8					# if maintining README.md in and RTF doc
Werkzeug==0.15.4
> pip install -r requirements.txt	# gives us the basics for flask, postgres, imdb 
```

### How do we access IMDB for movie info to display?
```
import imdb						# use this module

> ./movie_info_imdb.py 			# < exaples here
								# retrieves id, title, synopsis, year release, cast, runtime, rating, genre, kind, 
```

### Whats teh minimum serach info required for sensible results?
Are we looking for a movie? YES for now.
Movie name, year released.


### How do I auto generate TOC?
```
Point script at the right docs				# DEFAULT_FILE (input)
											# DEFAULT_README(output w TOC)
> create_TOC_for_md.py                      # run script
                                            # paste output into .md file TOC
```
Available here: [create_TOC_for_md.py](https://github.com/UnacceptableBehaviour/movie_picker/blob/master/create_TOC_for_md.py)  


### How do I insert a TOC?
To create a link to a chapter in MD:
```
[Text to Display](#text-from-title)\
[Q's & How To's](#qs--how-tos)\
```

The text-from-title is the the text from the title downcased, with spaces replaced with a hyphen '-' and non alphanumeric characters removed. So "Q's & How To's" becomes '#qs--how-tos'
The '\\' at the end of the line is same as <br> or CRLF. (New line)

To create a TOC, create a numbered list of links. Tab in next level with new numbers.
```
1. [Current status](#status)\
2. [Contents](#contents)\
3. [Next steps](#next-steps)\
4. [Completed](#completed)\
5. [Q's & How To's](#qs--how-tos)\
    1. [Adding tabs to content links](#adding-tabs-to-content-links) \
    2. [Auto generaging TOC](#auto-generaging-toc)\
6. [Tips on context doc](#tips)\
7. [References](#references)
```


## TIPS
Keep status concise:  
Put the colour in square brackets on the next line immediately after status  
RED   - Stalled, technology/cost barrier.  
AMBER - Work in progress.  
GREEN - Complete.  
BLUE  - Parked, no action planned. (maybe incomplete / redundant)  

<br>/CRLF in markdown is endline \\ or 2 spaces at the end '  '



## REFERENCES


## Completed
2020.Mar.05 - SF - Create Context Template - Move to bottom?  
2020.Mar.05 - SF - Setup basic Flask dir tree.
2020.Mar.05 - SF - Add disc scan, to find movie (and audio) files.
2020.Mar.05 - SF - Query IMDB for movie info.
2020.Mar.07 - SF - Integrate IMDB queries into MMdia class (was Pass the information to scraper, gather information.)
2020.Mar.08 - SF - Check search reulst for kind = movie
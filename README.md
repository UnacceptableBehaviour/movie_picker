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
	1. [What directory structure is required for a module? (python3)](#what-directory-structure-is-required-for-a-module-python3)  
		1. [Flow chart of how modules are loaded](#flow-chart-of-how-modules-are-loaded)  
	2. [How do you pickle a class (with it's class variables) and reconstitute it](#how-do-you-pickle-a-class-with-its-class-variables-and-reconstitute-it)  
7. [How To's](#how-tos)  
	1. [How do I auto generate TOC?](#how-do-i-auto-generate-toc)  
	2. [How do I insert a TOC?](#how-do-i-insert-a-toc)  
		1. [TIPS](#tips)  
	3. [How to do initial git repo setup for simple Flask app](#how-to-do-initial-git-repo-setup-for-simple-flask-app)  
	4. [How do we scrape IMDB for movie info to display?](#how-do-we-scrape-imdb-for-movie-info-to-display)  
	5. [How do we access IMDB for movie info to display?](#how-do-we-access-imdb-for-movie-info-to-display)  
	6. [Whats the minimum search info required for sensible results?](#whats-the-minimum-search-info-required-for-sensible-results)  
	7. [How do I mount the media disk (on rPi) R/W locally on mac for development](#how-do-i-mount-the-media-disk-on-rpi-rw-locally-on-mac-for-development)  
	8. [How do I make a class iterable?](#how-do-i-make-a-class-iterable)  
8. [REFERENCES](#references)  
9. [Completed](#completed)  


## AIM:
A little python practice, scraping, flask, basic web.

## Next steps
Fix Exceptions file - maybe check a few modules for examples.
  /venv/lib/python3.7/site-packages
POC working. Refactor functionality into a module split into MMediaLib, MMedia (item)	
- return_block (next 10 items - for JS world)
- get_n_items(n, json=True) = return keys if json False  
- return block as json - add flag to above  
Tidy up argument processing, bit flaky - not thought out - exception city!
Allow toggling of favourite icon, seen it icon  
Get cover art from wikipedia/google > 

## Questions / Barriers
### How to scrape wikipedia for cover art?
For example a quick search of title: ""
<a href="/wiki/File:Ant-Man_and_the_Wasp_poster.jpg" class="image"><img alt="Ant-Man and the Wasp poster.jpg" src="//upload.wikimedia.org/wikipedia/en/2/2c/Ant-Man_and_the_Wasp_poster.jpg" decoding="async" width="220" height="326" class="thumbborder" data-file-width="220" data-file-height="326"></a>
How to Google movie name & year movie tab pick wiki link
https://stackoverflow.com/questions/20716842/python-download-images-from-google-image-search
https://pypi.org/project/Google-Images-Search/		depends on 
	https://developers.google.com/custom-search/	API key needed
https://github.com/hardikvasa/google-images-download
https://pypi.org/project/wikipedia/
https://www.mediawiki.org/wiki/Manual:Pywikibot		more advanced 

## How To's
### How do I auto generate TOC?
```
Point script at the right docs			# DEFAULT_FILE (input)
						# DEFAULT_README(output w TOC)
> create_TOC_for_md.py 			# run script
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
#### TIPS
Keep status concise:  
Put the colour in square brackets on the next line immediately after status  
RED   - Stalled, technology/cost barrier.  
AMBER - Work in progress.  
GREEN - Complete.  
BLUE  - Parked, no action planned. (maybe incomplete / redundant)  
<br>/CRLF in markdown is endline \\ or 2 spaces at the end '  '

### How to do initial git repo setup for simple Flask app
```
> git add .gitignore			# add config file - which dir/files to track/ignore
> git commit -m'update config'
> git push
> python3 -m venv venv			# setup python 3 virtual env
> .pe					# activate environment - alias .pe='. venv/bin/activate'
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
striprtf==0.0.8				# if maintining README.md in and RTF doc
Werkzeug==0.15.4
> pip install -r requirements.txt	# gives us the basics for flask, postgres, imdb 
```
### How do we scrape IMDB for movie info to display?  
Scraping isnt needed for this task theres an imdb module:  
```
> pip install IMDbPY
import imdb     # API for imdb
```
Demo script: [scripts/movie_info_imdb.py](https://github.com/UnacceptableBehaviour/movie_picker/blob/master/scripts/movie_info_imdb.py)  

REFS
https://imdbpy.readthedocs.io/en/latest/usage/movie.html#movies

### How do we access IMDB for movie info to display?
```
import imdb			# use this module

> ./movie_info_imdb.py 		# < exaples here
				# retrieves id, title, synopsis, year release, cast, runtime, rating, genre, kind, 
```

### Whats the minimum search info required for sensible results?
Are we looking for a movie? YES for now.
Movie NAME, YEAR released.

### How do I mount the media disk (on rPi) R/W locally on mac for development
Find UUID of device, 
```
> sudo lsblk -o UUID,NAME,FSTYPE,SIZE,MOUNTPOINT,LABEL,MODEL		# list attached devices & mount point
UUID                                 NAME        FSTYPE    SIZE MOUNTPOINT            LABEL       MODEL
                                     sdb                 465.8G                                   MK5076GSX
564B-5772                            └─sdb1      vfat    465.8G /media/pi/FAITHFUL500 FAITHFUL500 
or
> sudo blkid		# list bulk devices
/dev/sdb1: LABEL="FAITHFUL500" UUID="564B-5772" TYPE="vfat" PARTUUID="00095536-01"
> sudo mount /dev/sdb1 /home/pi/MMdia/		# source_device_mountpoint target_mount_point
					# with this mount can view FAITHFUL500 remotely on osx
```
Next setup so mounts automatically on boot
```
> sudo nano /etc/fstab			# edit file system table
					# add following line
UUID=564B-5772 /home/pi/MMdia/ vfat defaults,auto,users,rw,nofail 0 0
     ^ID       ^mount point    ^FSTYPE
```



### How do I make a class iterable?
Give the calss you need to be iterable a base class of Iterable  
Create a class to handle iteration and have it inherit from Iterator  
implement ```__init__``` , ```__iter__``` and ```__next__``` in this class!  
```
from collections.abc import Iterable, Iterator
```
Example iterator implimentation: [iterator_example.py here](https://github.com/UnacceptableBehaviour/movie_picker/blob/master/iterator_example.py)  
Iterates FORWARD & REVERSE, and content SORTED by YEAR, TITLE or RATING.

### What directory structure is required for a module? (python3)
From article "For multifile module simply add a directory at base of project"
If I do that I get an error when I run:
```
File "./hello.py", line 9, in <module>
    from movie_picker import MMediaLib,MMedia
ImportError: cannot import name 'MMediaLib' from 'movie_picker' (unknown location)
```
to fix this needed to add additional path and relative dots, doesn't feel right!?
```
from .helpers import creation_date, hr_readable_from_nix	# movie_picker.py
from .mp_exceptions import *

from movie_picker.movie_picker import MMediaLib,MMedia 		# hello.py
```
Module basics & terminology:
```
module			any .py file
package			group of modules in a directory with __init__.py present
import mymod	adds mymod to symbol table - allow call mymod.myfunc() my mod.MY_CONST etc
				each module has its own symbol table (private namespace)

Interpreter looks for modules in sys.path
import sys
print(f"Modules searched for here:{sys.path}")
> Modules searched for here:['/Users/simon/a_syllabus/lang/python/repos/movie_picker',
'/usr/local/Cellar/python/3.7.5/Frameworks/Python.framework/Versions/3.7/lib/python37.zip',
'/usr/local/Cellar/python/3.7.5/Frameworks/Python.framework/Versions/3.7/lib/python3.7',
'/usr/local/Cellar/python/3.7.5/Frameworks/Python.framework/Versions/3.7/lib/python3.7/lib-dynload',
'/Users/simon/a_syllabus/lang/python/repos/movie_picker/venv/lib/python3.7/site-packages']

Note directory the code runs from is FIRST in the search path giving it priority.  

The interpreter compiles modules into bytecode with is caches in the __pycache__ directory.
Format: moviepicker.cpython-37.pyc - 37 is the python version number
The bytecode is platform independent - will run across architectures.
-OO option size bytecode optimisation 	EG python -OO ./hello.py  produced bytecode 17x smaller 
```
#### Flow chart of how modules are loaded  
![Flow chart of how modules are loaded](https://s3.dualstack.us-east-2.amazonaws.com/pythondotorg-assets/media/dev/peps/pep-3147/pep-3147-1.png)

[Section on packages](https://docs.python.org/3/tutorial/modules.html#packages)  
```
from moviepicker import moviepicker
dir()
['Flask', '__annotations__', '__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__',
 '__package__', '__spec__', 'app', 'render_template', 'request', 'sys']

dir(moviepicker):
['AUDIO_EXTS', 'Counter', 'DOC_DIST', 'FORWARD', 'IncorrectSortAttributeError', 'Iterable', 'Iterator', 'LOWEST_DOC_DISTANCE',
  'MMedia', 'MMediaLib', 'MMediaLibError', 'MOVIE', 'MediaLibIter', 'NoDBFileFound', 'NoRootDirectoryOrDBFound',
  'PICKLED_MEDIA_LIB_FILE_REPO', 'PICKLED_MEDIA_LIB_FILE_V2', 'Path', 'READ_ONLY', 'READ_WRITE', 'REVERSE', 'VIDEO_EXTS',
  '__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__', 'atexit',
  'creation_date', 'doc_distance', 'get_doc_vector_word', 'get_list_of_file_extensions', 'hr_readable_from_nix', 'imdb',
  'inner_product', 'json', 'look_in_repo', 'main', 'math', 'mmdia_root2', 'pickle', 'pprint', 're',
  'select_best_item_from_search_results', 'sys', 'traceback', 'urllib']
__main__
./hello.py
```
In the end the least noisy, namespace-wise, and for most readable I think the following:
```
./hello.py
from moviepicker.moviepicker import MMediaLib,MMedia,REVERSE,FORWARD

./moviepicker/moviepicker.py
from moviepicker.helpers import creation_date, hr_readable_from_nix
from moviepicker.exceptions import *
```

REFS:
https://docs.python.org/3/tutorial/modules.html
>> Lots anti pattern Examples <<
http://python-notes.curiousefficiency.org/en/latest/python_concepts/import_traps.html
https://dev.to/codemouse92/dead-simple-python-project-structure-and-imports-38c6
https://docs.python-guide.org/writing/structure/
https://github.com/navdeep-G/samplemod	Is this 2.7? 


## REFERENCES


## Completed
2020.Mar.05 - SF - Create Context Template - Move to bottom?  
2020.Mar.05 - SF - Setup basic Flask dir tree.  
2020.Mar.05 - SF - Add disc scan, to find movie (and audio) files.  
2020.Mar.05 - SF - Query IMDB for movie info.  
2020.Mar.07 - SF - Integrate IMDB queries into MMdia class (was Pass the information to scraper, gather information.)  
2020.Mar.08 - SF - Check search results for kind = movie  
2020.Mar.13 - SF - X-ref search result and query using doc_ditsance to get best match  
2020.Mar.14 - SF - Build DB / non-valatile storage (used pickle to start).  
2020.Apr.10 - SF - Added __repr__ to class.
2020.Jun.19 - SF - POC working. Refactored functionality into a module split into MMediaLib, MMedia (item)
	added MMedia items, added iterator functionality MMediaLib
2020.Jun.22 - SF - Added beginings of script interface, some basic option processing
2020.Jun.23 - SF - move imdb query function over to new classes
2020.Jun.25 - SF - add exceptions file
2020.Jun.26 - SF - tidy up import python package layout
2020.Jun.26 - SF - Display information using flask & boostrap cards.  	
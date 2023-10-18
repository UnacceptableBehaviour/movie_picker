# movie_picker
build movie library into flask web interface allows browsing and playing of movie

## Status: Build as quickly / simply as possible . . 
[BLUE] . . nearly GREEN

## Abstract
Turn and old tv (without a remote) and a 2.5 inch usb hard disc with DVD collection stored on it into a home cinema using a raspberry pi as a webserver, and an old tablet for a remote. 

## Contents  
1. [Status: Build as quickly / simply as possible . .](#status-build-as-quickly--simply-as-possible--)  
2. [Abstract](#abstract)  
3. [Contents](#contents)  
4. [AIM:](#aim)  
5. [Next steps](#next-steps)  
6. [Questions / Barriers](#questions--barriers)  
	1. [How do I run package as a script with options, like venv?](#how-do-i-run-package-as-a-script-with-options-like-venv)  
7. [How To's](#how-tos)  
	1. [How to auto generate TOC?](#how-to-auto-generate-toc)  
	2. [How to insert a TOC?](#how-to-insert-a-toc)  
		1. [TIPS](#tips)  
	3. [How to do initial git repo setup for simple Flask app](#how-to-do-initial-git-repo-setup-for-simple-flask-app)  
	4. [How to scrape IMDB for movie info to display?](#how-to-scrape-imdb-for-movie-info-to-display)  
	5. [How to access IMDB for movie info to display?](#how-to-access-imdb-for-movie-info-to-display)  
	6. [Whats the minimum search info required for sensible results?](#whats-the-minimum-search-info-required-for-sensible-results)  
	7. [How do I mount the media disk (on rPi) R/W locally on mac for development](#how-do-i-mount-the-media-disk-on-rpi-rw-locally-on-mac-for-development)  
	8. [How to make a class iterable?](#how-to-make-a-class-iterable)  
	9. [What directory structure is required for a module? (python3)](#what-directory-structure-is-required-for-a-module-python3)  
		1. [Flow chart of how modules are loaded](#flow-chart-of-how-modules-are-loaded)  
	10. [How to scrape wikipedia for cover art?](#how-to-scrape-wikipedia-for-cover-art)  
	11. [When is __init__.py called?](#when-is-initpy-called)  
	12. [How to do argument parsing w/ argparse module?](#how-to-do-argument-parsing-w-argparse-module)  
8. [REFERENCES](#references)  
9. [Completed](#completed)  


## AIM:  

A little python practice, scraping, flask, basic web.

## Next steps
* * *   
- implement todays pseudo code / UML - genre concept / NI /fav
- Show shortlisted item on shortlist page (should work same as gallery but media list from shortlist not DB).  
- Add super basic Preferences class inc shortlist / genre prefs.  
* * *   

Quick test clone onto a linux target, SB platform agnostic - quick check.  
- add supporting vid files to test create DB, fetch info etc.  
  
Comment out superfluous code, add TODOs to code make tidy up list.  

Enable passing -u option a path in CLI mode - Check if done.  
Tidy up argument processing - use argparse. See [cli_parse.py](https://github.com/UnacceptableBehaviour/movie_picker/blob/master/scripts/cli_parse.py)   
  
  
Create JS lib for rest: 
Identify different devices - use JS fingerprint?  
Change reshuffle button icon to back button icon in play remote mode  
Add DEBUG - detected display size - debug mobile remote - look like in desktop mode?  
How to debug CSS media detect  
  
  
Require user profile:  
Allow toggling of favourite icon, seen it icon.  
  
Add genre blocking - click on genre button cycle gm_grey (last), normal (no opinion), light(favour)
  




## Questions / Barriers
### How do I run package as a script with options, like venv?



## How To's
### How to auto generate TOC?
```
Point script at the right docs			# DEFAULT_FILE (input)
						# DEFAULT_README(output w TOC)
> create_TOC_for_md.py 			# run script
						# paste output into .md file TOC
```
Available here: [create_TOC_for_md.py](https://github.com/UnacceptableBehaviour/movie_picker/blob/master/create_TOC_for_md.py)  


### How to insert a TOC?
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
### How to scrape IMDB for movie info to display?
Scraping isnt needed for this task theres an imdb module:  
```
> pip install IMDbPY
import imdb     # API for imdb
```
Demo script: [scripts/movie_info_imdb.py](https://github.com/UnacceptableBehaviour/movie_picker/blob/master/scripts/movie_info_imdb.py)  

REFS
https://imdbpy.readthedocs.io/en/latest/usage/movie.html#movies

### How to access IMDB for movie info to display?
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

### How to make a class iterable?
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

### How to scrape wikipedia for cover art?
Initially tried wikipedia package but its pretty flakey when it comes to image retrieval. Its effective at getting the URL for the movie so use it to locat movie info & then use beautiful soup to get url for image and DL it.
```
scripts/get_image_from_wikipedia.py 					 # demo of wikipedia package - bit flaky retrieving images 50/50
scripts/get_image_bsoup4.py 														# beautifulsoup4 super basic demo - retrives image from wikipedia
scripts/image_from_web.py 														  # 3 ways to download image to local disk
```

REFS
https://pypi.org/project/wikipedia/  
https://www.crummy.com/software/BeautifulSoup/bs4/doc/  
other  
https://stackoverflow.com/questions/20716842/python-download-images-from-google-image-search  
https://pypi.org/project/Google-Images-Search/		depends on  https://developers.google.com/custom-search/	API key needed  
https://github.com/hardikvasa/google-images-download  
https://www.mediawiki.org/wiki/Manual:Pywikibot		more advanced   


### When is __init__.py called? 
Problem
FILE: hello.py
from moviepicker.moviepicker import MMediaLib,MMedia,REVERSE,FORWARD

FILE: moviepicker/moviepicker.py
from moviepicker.helpers import creation_date, hr_readable_from_nix
from moviepicker.exceptions import *
from moviepicker.retrieval import get_hires_cover, find_wiki_url_for_movie, get_lead_image_from_wikipedia

FILE: __init__.py
from .moviepicker import MMediaLib,MMedia,REVERSE,FORWARD
from .exceptions import *
from .retrieval import get_hires_cover, find_wiki_url_for_movie, get_lead_image_from_wikipedia
__version__ = (0, 0, 1)
print(dir())

$ ./hello.py 																									# works
$ ./moviepicker/moviepicker.py -l     # fails
Traceback (most recent call last):
  File "./moviepicker/moviepicker.py", line 4, in <module>
    from moviepicker.helpers import creation_date, hr_readable_from_nix
  File "/Users/simon/a_syllabus/lang/python/repos/movie_picker/moviepicker/moviepicker.py", line 4, in <module>
    from moviepicker.helpers import creation_date, hr_readable_from_nix
ModuleNotFoundError: No module named 'moviepicker.helpers'; 'moviepicker' is not a package

CHANGE
$ ./moviepicker/moviepicker.py -l     # fails
from moviepicker.helpers import creation_date, hr_readable_from_nix
from moviepicker.exceptions import *
from moviepicker.retrieval import get_hires_cover, find_wiki_url_for_movie, get_lead_image_from_wikipedia
FAILS:
File "/Users/simon/a_syllabus/lang/python/repos/movie_picker/moviepicker/moviepicker.py", line 4, in <module>
    from moviepicker.helpers import creation_date, hr_readable_from_nix
ModuleNotFoundError: No module named 'moviepicker.helpers'; 'moviepicker' is not a package

$ ./moviepicker/moviepicker.py -l     # fails
from .helpers import creation_date, hr_readable_from_nix
from .exceptions import *
from .retrieval import get_hires_cover, find_wiki_url_for_movie, get_lead_image_from_wikipedia
FAILS:
File "./moviepicker/moviepicker.py", line 4, in <module>
    from .helpers import creation_date, hr_readable_from_nix
ImportError: attempted relative import with no known parent package

$ ./moviepicker/moviepicker.py -l     # works
from helpers import creation_date, hr_readable_from_nix
from exceptions import *
from retrieval import get_hires_cover, find_wiki_url_for_movie, get_lead_image_from_wikipedia
but BREAKS
$ ./hello.py
File "/Users/simon/a_syllabus/lang/python/repos/movie_picker/moviepicker/moviepicker.py", line 4, in <module>
    from helpers import creation_date, hr_readable_from_nix
ModuleNotFoundError: No module named 'helpers'

ADDED
$ ./moviepicker/moviepicker.py -l     # works
if __name__ == '__main__':
	from helpers import creation_date, hr_readable_from_nix
	from exceptions import *
	from retrieval import get_hires_cover, find_wiki_url_for_movie, get_lead_image_from_wikipedia


Problem X
When is __init__.py called? [Whenever package is imported!](https://docs.python.org/3/reference/import.html#regular-packages)  

-----------------------------
-- __init__.py moviepicker --
-----------------------------
['FORWARD', 'IncorrectSortAttributeError', 'MMedia', 'MMediaLib', 'MMediaLibError', 'NoDBFileFound', 'NoRootDirectoryOrDBFound', 'REVERSE', '__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__path__', '__spec__', 'exceptions', 'find_wiki_url_for_movie', 'get_hires_cover', 'get_lead_image_from_wikipedia', 'helpers', 'moviepicker', 'retrieval']


[__init__.py raison d'etre](https://stackoverflow.com/questions/448271/what-is-init-py-for#:~:text=The%20__init__.py%20file%20makes%20Python%20treat%20directories,the%20submodules%20to%20be%20exported.)  
[stackexchange note](https://stackoverflow.com/questions/41816973/modulenotfounderror-what-does-it-mean-main-is-not-a-package/41817024#41817024)  

Cant run moviepicker as a script?
Problem X - rename moviepicker.py mvpicker.py?
[stackexchange note](https://stackoverflow.com/questions/45446418/modulenotfounderror-no-module-named-main-xxxx-main-is-not-a-packag)  
However, beware that this absolute import (from package.module import something) fails if, for some reason, the package contains a module file with the same name as the package (at least, on my Python 3.7). So, for example, it would fail if you have (using the OP's example):
```
proj/
    __init__.py (empty)
    proj.py (same name as package)
    moduleA.py
    moduleB.py
```


### How to do argument parsing w/ argparse module?  
[demo of argparse in repo - /scripts/cli_parse.py](https://github.com/UnacceptableBehaviour/movie_picker/blob/master/scripts/cli_parse.py)   
[Python docs - argparse - tutorial](https://docs.python.org/3/howto/argparse.html)   
[ArgumentParser - docs](https://docs.python.org/3/library/argparse.html#type)   
[Real Python](https://realpython.com/command-line-interfaces-python-argparse/#how-to-use-the-python-argparse-library-to-create-a-command-line-interface)  




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
2020.Jun.27 - SF - Get cover art from wikipedia/google > retrieval.py  
2020.Jul.05 - SF - Make module runnable  
2021.Apr.14 - SF - Re-orient cards boostrap (make screen width or width/2?)    
Add functionality to retrieve image when adding media.  
Flask prefer load image over low quality href from imdb  
2021.Apr.14 - SF - Added Buttons for order by: year, release, A-Z, most recently added  

# movie_picker
Build movie library into flask web interface allows browsing and playing of movie.

## Status: Build as quickly / simply as possible . . 
[BLUE] . . nearly GREEN [see ACTIONS -old README.md](https://github.com/UnacceptableBehaviour/movie_picker/blob/master/ACTIONS.md)  
Add user needs implementing.  
Actor favourites needs implementing.  
  
## Abstract
Turn and old tv (without a remote) and a 2.5 inch usb hard disc with DVD collection stored on it into a home cinema using a raspberry pi as a webserver, and an old tablet for a remote.  
  
This developed into a system that allowed everyone to use their phone or tablet pick their favourite movies from the carousel. The combination of which would show up on the combined movie shortlist from which we would pick one.  
  
I adapted it for seasonal holidays and other family gatherings!
  
## Contents  
1. [Status: Build as quickly / simply as possible . .](#status-build-as-quickly--simply-as-possible--)  
2. [Abstract](#abstract)  
3. [Contents](#contents)  
4. [AIM:](#aim)  
5. [Quick start](#quick-start)  
	1. [How to: Scan a directory & Create DB, Add it to DB list so entries apear in carousel](#how-to-scan-a-directory--create-db-add-it-to-db-list-so-entries-apear-in-carousel)  
	2. [Running the moviepicker](#running-the-moviepicker)  
	3. [The carousell](#the-carousell)  
	4. [Movie Synopsis](#movie-synopsis)  
	5. [Tablet Remote Control](#tablet-remote-control)  
	6. [Settings 1 - Genre preferences etc](#settings-1---genre-preferences-etc)  
	7. [Settings 2 - About Listings](#settings-2---about-listings)  
6. [Clone onto a raspberry Pi](#clone-onto-a-raspberry-pi)  
	1. [How do I mount the media disk (on raspberry Pi) R/W locally on mac for development](#how-do-i-mount-the-media-disk-on-raspberry-pi-rw-locally-on-mac-for-development)  
7. [Next steps](#next-steps)  
8. [Questions / Barriers](#questions--barriers)  
9. [How To's](#how-tos)  
	1. [How to auto generate TOC?](#how-to-auto-generate-toc)  
	2. [How to insert a TOC?](#how-to-insert-a-toc)  


## AIM:  

A little python practice, scraping, flask, basic web.  

## Quick start
Setting up on a local machine to experiment:  

### How to: Scan a directory & Create DB, Add it to DB list so entries apear in carousel
```
$ git clone https://github.com/UnacceptableBehaviour/movie_picker
$ cd into movie_picker repo
$ . venv/bin/activate

# run with option update - - - \     / - - specify directory where movies files are
$ ./moviepicker/moviepicker.py -u /Volumes/Osx4T/mov_2022
```
```
Once finished the DB filename displayed like so:
PICKLING before EXIT: /Volumes/Osx4T/mov_2022/__media_data2/medialib2.pickle
```
Copy path to bottom of file: ```./movie_picker/db_paths.txt```  
EG  
```
/Volumes/Osx4T/mov_2022/__media_data2/medialib2.pickle
```
  
A list of paths to search for DB file held in  
./movie_picker/db_paths.txt  
Lines starting with a # are ignored.  
  
Movies found in the DB files will automatically be added to the carousels  
  
### Running the moviepicker
This was a python/flask hello world project so it's still called hello (TODO rename).  
Having [built a DB](#quick-start)  
```
$ cd into moviepicker repo
$ . venv/bin/activate
$ ./hello.py
```
Navigate to URL indicated at boot (0.0.0.0):
 * Running on http://127.0.0.1:52001
  
### The carousell
![The carousell](https://github.com/UnacceptableBehaviour/movie_picker/blob/master/static/images/moviepicker%20-%20screen%20grab%201.jpeg?raw=true)
  
### Movie Synopsis
![Movie Synopsis](https://github.com/UnacceptableBehaviour/movie_picker/blob/master/static/images/moviepicker%20-%20screen%20grab%202.jpeg?raw=true)
  
### Tablet Remote Control
![Tablet Remote Control](https://github.com/UnacceptableBehaviour/movie_picker/blob/master/static/images/moviepicker%20-%20tablet%20remote.jpeg?raw=true)
  
### Settings 1 - Genre preferences etc
![Settings 1 - Genre preferences etc](https://github.com/UnacceptableBehaviour/movie_picker/blob/master/static/images/moviepicker%20-%20settings.1%20-%20prefs.jpeg?raw=true)
  
### Settings 2 - About Listings
![Settings 2 - About Listings](https://github.com/UnacceptableBehaviour/movie_picker/blob/master/static/images/moviepicker%20-%20settings.2%20-%20movie%20info.jpeg?raw=true)
  

## Clone onto a raspberry Pi
Plug the Pi into the TV (and network).  
SSH into target device, clone the repo there.  
Install VLC.  
Point the db_paths.txt file at the relavant databases.  
(the pathe must be visible from the Pi)  
Run the flask server.  
Use a tablet or phone to browse the carousel and select / play a movie.  


### How do I mount the media disk (on raspberry Pi) R/W locally on mac for development
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

## Next steps
* * *   
- There's still a few manul bits that need smoothing out.
- Implement ADD user button.  
* * *   
  
Comment out superfluous code, add TODOs to code make tidy up list.  

Create JS lib for rest: 
Identify different devices - use JS fingerprint?  
  
Add DEBUG - detected display size - debug mobile remote - look like in desktop mode?  
  
Require user profile:  
Allow toggling of favourite icon, seen it icon.  
  

## Questions / Barriers
  
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


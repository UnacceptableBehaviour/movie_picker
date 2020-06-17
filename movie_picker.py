#! /usr/bin/env python
from pathlib import Path
from collections import Counter
import re
# import json
import imdb	
import urllib.request
# import math
# import traceback
import pickle
import sys		# sys.exit()
import atexit

# TODO remove after refactor \\
from pprint import pprint
from movie_info_disk import get_MMdia_lib, MMdia
# TODO remove after refactor ^^



class MMedia:
	# choose order by most frequently occuring - TODO - stats from data
	AUDIO_EXTS = [ '.mp3', '.ac3' ]                   
	VIDEO_EXTS = [ '.mp4', '.avi', '.mkv', '.m4a' ]
	
	def __init__( self, mmdia_info = {}, file_path=None ):
		self.info = { 'id': None,
			'title': '',
			'synopsis': '',
			'year': 0,
			'cast': [],
			'runtime_m': 0,
			'runtime_hm': 0,
			'rating':0,
			'genres':[],
			'kind':[],
			'seen': False,
			'fav':False,
			'image_url':None,
			'hires_image': None,			# or path to image
			'file_name': None,				# actually full path - refactor
			'file_title': None,
			'movie_data_loaded': False
		}
		
		if file_path != None:
			# build movie data
			print("** IMPLEMENT BUILD MOVIE DATA **")
		else:
			self.info.update(mmdia_info)


	def __str__(self):	
		return 'MMedia::def __str__'

	def __repr__(self):
		print('MMedia::def __repr__')
		obj_as_string = ''
		dict_name = "'info':"
		md = ''
		line = 0
		for k,v in self.info.items():
			v_str = f"{v}"
			if v_str.__class__.__name__ == 'str': v_str = f"'{v}'"
			spacer = ' ' * ((len(dict_name)+1) * min(1,line)) # 0 on first line, 1 otherwise
			line += 1
			md = md + f"{spacer}'{k}': {v_str},\n"
		
		md = re.sub('^ ?', '{', md)	 # add { at start 
		md = re.sub(',\n$', '}', md)	# add } at end
		
		md = f"{dict_name}{md}"
		
		obj_as_string += md
		
		obj_as_string = f"\n{type(self)}" + '\n{' + f"{obj_as_string}" + ' }'
		
		return obj_as_string

	def is_audio(self):
		return Path(self.info['file_name']).suffix in MMedia.AUDIO_EXTS
	
	def is_video(self):
		return Path(self.info['file_name']).suffix in MMedia.VIDEO_EXTS

	def file_path(self):
		return self.info['file_name']
	
	def data_loaded(self):
		return self.info['movie_data_loaded']



mmdia_root2 = Path('/Volumes/time_box_2018/movies/')
PICKLED_MEDIA_LIB_FILE_V2 = mmdia_root2.joinpath('__media_data2','medialib2.pickle')
class MMediaLib():
	
	ia = imdb.IMDb()

	def __init__( self, lib_file_path=PICKLED_MEDIA_LIB_FILE_V2 ):
		self.lib_file_path = lib_file_path
		
		self.__badly_formatted_names = []
	
		self.media_files_count = { 'video': Counter(),   # no need to initialise, and will find duplicates
								   'audio': Counter() }
		
		self.media_files = { 'video': {},
							 'audio': {} }
		
		self.other_files = []

		# run pickler on exit
		atexit.register(self.exit_handler)
	
		if self.lib_file_path.exists():
			print(f"\n\nUN-PICKLING from {self.lib_file_path}")
			with open(self.lib_file_path, 'rb') as f:				
				self.media_files = pickle.load(f)

	def __str__(self):	
		return 'MMediaLib::def __str__'

	def __repr__(self):   
		return 'MMediaLib::def __repr__'  

	def add_media(self, media):
		
		# TODO raise if incorrect type
		print(f"ADD MEDIA: {media.file_path()} type:{media.__class__.__name__}")
		if self.is_new_media(media.file_path()):
			print(f"NEW MEDIA: {media.file_path()}")
			# TODO add check to see if info['movie_data_loaded']: False
			# load it if not
			if not media.data_loaded:
				print(f"DATA LOADED?: {media.data_loaded()}")
				media = MMedia({}, media.file_path())
			
			if media.is_video():
				print("MEDIA: isVideo")
				self.media_files_count['video'][media.file_path().name.lower()] += 1
				self.media_files['video'][media.file_path().name.lower()] = media
			
			elif media.is_audio():
				print("MEDIA: isAudio")
				self.media_files_count['audio'][media.file_path().name.lower()] += 1
				self.media_files['audio'][media.file_path().name.lower()] = media
			
			else:
				print(f"** WARNING ** unknown media type {media.file_path()}")
				#raise
				

	def is_new_media(self, mfile):
		#mfile = Path(mfile)

		if mfile.name.lower() in self.media_files['video']:
			return False
	
		if mfile.name.lower() in self.media_files['audio']:
			return False
				
		return True
			
	# maybe use a context manager to call this? (https://docs.python-guide.org/writing/structure/)
	def exit_handler(self):		
		# create directory if it doesn't exist
		self.lib_file_path.parent.mkdir(parents=True, exist_ok=True)
		
		print(f'Pickling before exit:\n{self.lib_file_path}')
		print(f"SIZE: {self.media_files['video'].keys()} - {len(self.media_files['video'].keys())} - {type(self.media_files)}")
		print(f"len(self.media_files): {len(self.media_files)}")
		print(f"self.lib_file_path: {self.lib_file_path}")
		
		print(f"PICKLING to {self.lib_file_path}")
		with open(self.lib_file_path, 'wb') as f:
			#pickle.dump(MMediaLib, f, pickle.HIGHEST_PROTOCOL)  # how to pickle class instance?
			pickle.dump(self.media_files, f, pickle.HIGHEST_PROTOCOL)	

	

def main():
	pass


if __name__ == '__main__':
	
	# convert to new classes for pickling
	print("** movie picker main() - old_media_lib **")
	old_media_lib = get_MMdia_lib()

	print("** movie picker main() - new_media_lib **")
	new_media_lib = MMediaLib()			
	
	for count, (movie,media) in enumerate(old_media_lib['video'].items()):
		
		file_size = (str( round(old_media_lib['video'][movie].file_stat.st_size / (1024 * 1024),1))+'MB').rjust(6)
		
		print(f"== {str(count).rjust(3)} - {file_size} - {movie}")
		media.movie_data['movie_data_loaded'] = media.movie_data_loaded
		media.movie_data['hires_image'] = media.hires_image
		new_media_type = MMedia(media.movie_data)
		new_media_lib.add_media(new_media_type)
				
	sys.exit()			# MMediaLib() pickles info on exit - in case crash / Ctrl+C during building DB
		

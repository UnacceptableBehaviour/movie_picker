#! /usr/bin/env python
from pathlib import Path
from helpers import creation_date, hr_readable_from_nix
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

# from operator import itemgetter, attrgetter		# sorting by object attributes


# TODO remove after refactor \\
from pprint import pprint
from movie_info_disk import get_MMdia_lib, MMdia
# TODO remove after refactor ^^


# choose order by most frequently occuring - TODO - stats from data
AUDIO_EXTS = [ '.mp3', '.ac3' ]                   
VIDEO_EXTS = [ '.mp4', '.avi', '.mkv', '.m4a' ]
class MMedia:
	
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
			'file_path': None,
			'file_stats':None,
			'file_name': None,				# actually full path - refactor
			'file_title': None,
			'when_added': None,				# TODO - add epoch now
			'movie_data_loaded': False
		}
		
		if file_path != None:
			# build movie data
			print("** IMPLEMENT BUILD MOVIE DATA **")
		else:
			self.info.update(mmdia_info)


	def __str__(self):		
		return f"MMedia: {self.info['year']} {str(self.info['rating']).rjust(4)} {self.info['title']} - Added:{hr_readable_from_nix(self.info['when_added'])}"

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
		return Path(self.info['file_path']).suffix in AUDIO_EXTS
	
	def is_video(self):
		return Path(self.info['file_path']).suffix in VIDEO_EXTS

	def file_path(self):
		return self.info['file_path']
	
	def data_loaded(self):
		return self.info['movie_data_loaded']



from collections.abc import Iterable, Iterator
# collection.abc = abstract base class
# https://docs.python.org/3/library/collections.abc.html

FORWARD = 1
REVERSE = -1
class MediaLibIter(Iterator):
	'''
	Iterator designed for MediaLib inherits from Iterator base class
	'''
	def __init__(self, media_dict, sorted_keys, direction=FORWARD):
		self.direction = REVERSE if direction==REVERSE else FORWARD 	# has to be FORWARD or REVERSE!
		self._index = -1 if direction==REVERSE else 0					# start at index 0 if going forward -1 if reversing
		self.media_files = media_dict
		self.media_keys = sorted_keys 	#[key for key in media_dict.keys()]			# get an list of keys media_dict.keys() -> dict_keys
																		# list(media_dict.keys()) works too
	def __iter__(self):				# use?
		return self
	
	def __next__(self):
		try:
			return_item = self.media_files[self.media_keys[self._index]]			
			self._index += self.direction
	
		except IndexError:
			raise StopIteration()
	
		return return_item
	

mmdia_root2 = Path('/Volumes/time_box_2018/movies/')
PICKLED_MEDIA_LIB_FILE_V2 = mmdia_root2.joinpath('__media_data2','medialib2.pickle')
READ_ONLY = 'r'
READ_WRITE = 'w'
class MMediaLib(Iterable):

	ia = imdb.IMDb()

	def __init__( self, lib_file_path=PICKLED_MEDIA_LIB_FILE_V2 ):
		self.lib_file_path = lib_file_path
		self.read_write_mode = READ_ONLY
		
		self.__badly_formatted_names = []
	
		self.media_files_count = Counter() 		# track duplicates 
		
		self.media_files = {}
		
		self.other_files = []

		# run pickler on exit
		atexit.register(self.exit_handler)
	
		if self.lib_file_path.exists():
			print(f"\n\nUN-PICKLING from {self.lib_file_path}")
			with open(self.lib_file_path, 'rb') as f:				
				self.media_files = pickle.load(f)
			print(f"Loaded:{len(self.media_files)} - {type(self.media_files)}")
		
		self._sorted_by_year = list
		self._sorted_by_title = []
		self._sorted_by_rating = []
		self._sorted_by_most_recently_added = []
		
		print("MMediaLib: building sorted lists . . .")
		self.sort_lists()
		print(" . . . Done")
			

	def __iter__(self) -> MediaLibIter:									#  -> MediaLibIter is optional guide to coder & toolchain
		keys = list(self.media_files.keys())
		return MediaLibIter(self.media_files, keys)							#                  it indicates the return type
	
	def reverse_each(self) -> MediaLibIter:
		keys = list(self.media_files.keys())
		return MediaLibIter(self.media_files, keys, direction=REVERSE)

	def sorted_by_year(self, direction=FORWARD) -> MediaLibIter:		
		return MediaLibIter(self.media_files, self._sorted_by_year, direction)	
	
	def sorted_by_title(self, direction=FORWARD) -> MediaLibIter:
		return MediaLibIter(self.media_files, self._sorted_by_title, direction)	
	
	def sorted_by_rating(self, direction=FORWARD) -> MediaLibIter:
		return MediaLibIter(self.media_files, self._sorted_by_rating, direction)

	def sorted_by_most_recently_added(self, direction=FORWARD) -> MediaLibIter:
		return MediaLibIter(self.media_files, self._sorted_by_most_recently_added, direction)

	def sort_lists(self):
		# create list of sorted keys - use sorted key for iterators
		self._sorted_by_year = sorted(self.media_files, key=lambda k: int(self.media_files[k].info['year']))	# in place media_files.sort(key=lambda x: x.year)
		self._sorted_by_title = sorted(self.media_files, key=lambda k: self.media_files[k].info['title'])
		self._sorted_by_rating = sorted(self.media_files, key=lambda k: float(self.media_files[k].info['rating']), reverse=True)
		self._sorted_by_most_recently_added = sorted(self.media_files, key=lambda k: float(self.media_files[k].info['when_added']), reverse=True)
	
		
	
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
		
			self.media_files_count[media.file_path().name.lower()] += 1
			self.media_files[media.file_path().name.lower()] = media
							

	def is_new_media(self, mfile):
		#mfile = Path(mfile)

		if mfile.name.lower() in self.media_files.keys():
			return False
		
		return True
	
	def set_write_mode(self, mode):
		self.read_write_mode = mode

	def get_write_mode(self, mode):
		return self.read_write_mode

						
	# maybe use a context manager to call this? (https://docs.python-guide.org/writing/structure/)
	# TODO assees exersize
	def exit_handler(self):		
		if self.read_write_mode == READ_WRITE:
			# create directory if it doesn't exist
			self.lib_file_path.parent.mkdir(parents=True, exist_ok=True)			
			print(f'PICKLING before EXIT: {self.lib_file_path}')
			third_key = list(self.media_files.keys())[2]
			print(f"SIZE: {len(self.media_files.keys())} - {type(self.media_files[third_key])} ")
			with open(self.lib_file_path, 'wb') as f:
				pickle.dump(self.media_files, f, pickle.HIGHEST_PROTOCOL)	

	

def main():
	pass


if __name__ == '__main__':

	print("** movie picker main() - new_media_lib **")
	new_media_lib = MMediaLib()
	#new_media_lib.set_write_mode(READ_WRITE)
	
	
	# TODO - the 'And Then There Were None' bug
	# - possible due to video title incorrectly extracted from file?
	# - querie imdb with None and the closest resul is 'And Then There Were None'
	
	count = 0
	#for m in new_media_lib.sorted_by_year():
	#for m in new_media_lib.sorted_by_title():
	for m in new_media_lib.sorted_by_rating():
	#for m in new_media_lib.sorted_by_most_recently_added():
		if m == {} or m.info['title'] == 'And Then There Were None':
			continue
		print(m)
		# print(f" - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - << S {count}")
		# pprint(m)
		# print(dir(m))		
		# print(f" - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - << E {count}")
		# count += 1
		# if count > 15:
		# 	break
	
	
	sys.exit()			# MMediaLib() pickles info on exit - in case crash / Ctrl+C during building DB


	# from pprint import pprint
	# from movie_info_disk import get_MMdia_lib, MMdia
	#
	print("** movie picker main() - new_media_lib **")
	new_media_lib = MMediaLib()
	new_media_lib.set_write_mode(READ_WRITE)
	
	# convert to new classes for pickling - import data
	print("** movie picker main() - old_media_lib **")
	old_media_lib = get_MMdia_lib()
	
	for count, (movie,media) in enumerate(old_media_lib['video'].items()):
		print(f" - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - << S {count}")
		pprint(media)
		print(" - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - << M")
		print(f"== {str(count).rjust(3)} - - - - - - - - - - - - - - - - - - - - - ")		
		file_stats = Path(old_media_lib['video'][movie].full_path).stat() # refresh stats
		file_size = (str( round(file_stats.st_size / (1024 * 1024),1))+'MB').rjust(6)
		file_path = old_media_lib['video'][movie].full_path
		added_epoch = creation_date(file_path)
		print(file_stats)
		print(f"epoch added: {added_epoch} - {hr_readable_from_nix(added_epoch)}")
		
		print(f"== {str(count).rjust(3)} - {file_size} - {movie}")
		media.movie_data['movie_data_loaded'] = media.movie_data_loaded
		media.movie_data['hires_image'] = media.hires_image
		media.movie_data['file_path'] = file_path
		media.movie_data['file_name'] = movie
		media.movie_data['file_stats'] = file_stats
		media.movie_data['when_added'] = added_epoch
		new_media_type = MMedia(media.movie_data)
		new_media_lib.add_media(new_media_type)						
		print(" - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - << M2")
		pprint(new_media_type)
		print(" - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - << E")
		#if count > 5: break

	sys.exit()
	
	# # ah dict.keys() returns dict_keys(['f1', 'f2', 'f3', 'f4']) type 
	# a = {'f1': MMedia({'title': 'F1'}),
	# 	 'f2': MMedia({'title': 'F2'}),
	# 	 'f3': MMedia({'title': 'F3'}),
	# 	 'f4': MMedia({'title': 'F4'}) }
	# 
	# b = [key for key in a.keys()]	# use list comprehension to convert
	# 
	# pprint(b)		

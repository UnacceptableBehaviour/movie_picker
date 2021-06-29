#! /usr/bin/env python
from pathlib import Path

# allow run directly as script or as module - TODO see if this is best practice doesnt feel like it!
if __name__ == '__main__':
	from helpers import creation_date, hr_readable_from_nix
	from exceptions import *
	from retrieval import get_hires_cover, find_wiki_url_for_movie, get_lead_image_from_wikipedia
else:
	from .helpers import creation_date, hr_readable_from_nix

from collections import Counter
import re
import imdb
import urllib.request
import pickle
import sys		# sys.exit()
import atexit
import math
import traceback
import json
import shutil

# from operator import itemgetter, attrgetter		# sorting by object attributes

# TODO remove after refactor \\
from pprint import pprint
#from movie_info_disk import get_MMdia_lib, MMdia
# TODO remove after refactor ^^


# choose order by most frequently occuring - movie_picker -ec will print this info about target disk
AUDIO_EXTS = [ '.mp3', '.ac3' ]
VIDEO_EXTS = [ '.mp4', '.mkv', 'wmv', '.avi', '.m4a' ]
class MMedia:
	_badly_formatted_names = ['Empty']
	_problem_match = []

	def __init__( self, file_path=None, mmdia_info = {}, imdb_query=False ):
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
			'file_path': Path(file_path),
			'file_stats':None,
			'file_name': None,
			'file_title': None,
			'when_added': None,				# TODO - add epoch now
			'movie_data_loaded': False
		}

		if file_path != None:
			self.info['file_name'] = self.info['file_path'].name
			self.get_media_stats()

			self.get_media_name_and_year_from_filename()

			if imdb_query == True:
				self.query_imdb_for_movie_info()

		else:
			self.info.update(mmdia_info)

	def as_json(self):
		media = self.info.copy()
		#media['cast'] = [ (str(actor), actor.getID()) for actor in media['cast'] ] # name & ID
		media['cast'] = [ str(actor) for actor in media['cast'] ]
		media['file_path'] = str(media['file_path'])
		return json.dumps(media)

	def __str__(self):
		return f"{self.info['year']} {str(self.info['rating']).rjust(4)} {(self.info['title']).ljust(40)} - Added:{hr_readable_from_nix(self.info['when_added'])}\t{self.get_media_size_in_mb()} - {self.info['file_path'].name}"

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

	def get_media_stats(self):
		self.info['file_stats'] = self.info['file_path'].stat()
		return self.info['file_stats']

	def get_media_size_in_mb(self):
		if self.info['file_stats'] == None:
			self.get_media_stats()

		return round(self.info['file_stats'].st_size / (1024 * 1024),1)


	def get_media_name_and_year_from_filename(self):

		if self.is_video():
			filename = re.sub(r'((\d{3,4}p)|brrip|dvdrip|eng subs|bluray|english dub|dvd|divx|xvid).*', '', self.info['file_path'].stem)
			# movies
			# looking for: name followed by year or (year) or [year] resolution bla bla .ext
			# r'[\(\)\[\]]?\d\d\d\d[\(\)\[\]]?[\.\b]' - 4 digit year followed by . or word boundary
			match = re.search(r'(.*?)[\(\)\[\]]?(\d\d\d\d)[\(\)\[\]]?', filename, re.I )
			dirty_title = ''
			year = 0
			if match:
				self.info['year'] = match.group(2)
				dirty_title = match.group(1)
			else:
				dirty_title = filename

			dirty_title = re.sub(r'^[\W_]*','',dirty_title)     # remove leading non word
			dirty_title = re.sub(r'[\W_]*$','',dirty_title)     # remove trailing non word
			cleaned_up_title = re.sub(r'[\._]',' ',dirty_title) # replace . and underscore with space
			self.info['file_title'] = cleaned_up_title

		elif self.is_audio():
			pass

	# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
	# USING imdb module
	# Usage (keys): https://imdbpy.readthedocs.io/en/latest/usage/movie.html#movies
	# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
	def query_imdb_for_movie_info(self):
		skip_list = ['Alien Directors Cut 1979']
		url = None
		search_year = self.info['year'] if len(str(self.info['year'])) > 3 else ''

		query = f"{self.info['file_title']} {search_year}"

		if query in skip_list:
			print(f"\n\n\n\n\n\n\n- - - - - - SKIPPING {query}\n\n\n\n\n\n\n")
			return

		if self.info['file_title'].lower() == 'sample' and search_year == '':
			return

		if self.info['movie_data_loaded']:
			print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
			print(f"Retieving info from D-I-S-C\nSearching for: {query} < {self.info['movie_data_loaded']}")
			pprint(self.info)
			print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
			return

		print(f"\n\n\n")
		print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
		print(f"Retieving info from IMDB\nSearching for: {query} < LOADED? {self.info['movie_data_loaded']}")
		print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
		results = MMediaLib.imdb_search.search_movie(query)

		# return result with highest Doc Distance with search
		movie = select_best_item_from_search_results('movie', query, results)

		if movie == None:
			MMedia._badly_formatted_names.append(self.info['file_path'])
			self.info['movie_data_loaded'] = False # dont get hung up on failure
			return

		self.info['id'] = movie.movieID

		m = MMediaLib.imdb_search.get_movie(movie.movieID)
		#print(MMediaLib.imdb_search.get_movie_infoset())
		if m == None:
			MMedia._badly_formatted_names.append(self.info['file_path'])
			self.info['movie_data_loaded'] = False # dont get hung up on failure
			return

		try:
			print(f"ID: {m.movieID}")
			print(f"Title: {m['title']}")
			self.info['title'] = m['title']
		except:
			print(">> - - - - - > WARNING: no m['title']")


		try:
			print(f"Rating: {m['rating']}")
			self.info['rating'] = m['rating']
		except:
			print(">> - - - - - > WARNING: no m['rating']")

		try:
			print(f"Runtimes: {m['runtimes']} or {int(int(m['runtimes'][0])/60)}h{int(m['runtimes'][0])%60}m")
			print(m.current_info)
			self.info['runtime_m'] = m['runtimes'][0]
			self.info['runtime_hm'] = f"{int(int(m['runtimes'][0])/60)}h{int(m['runtimes'][0])%60}m"
		except:
			print(">> - - - - - > WARNING: no m['runtimes']")

		# m.get('plot') - list of str (7 in this case all diffferent)
		plot_size = 0
		try:
			for synopsis in m.get('plot'):
				# caballo grande ande on no ande!
				if plot_size < len(synopsis):
					plot_size = len(synopsis)
					self.info['synopsis'] = synopsis
					print(f"SYNOPSIS:\n{synopsis}")

			print(f"\nSYNOPSIS PICKED:\n{synopsis}")
		except TypeError:
			print(">> - - - - - > WARNING: no m['synopsis']")

		# this is actually the plot - massive
		# print(f"\nSYNOPSIS:\n{m.get('synopsis')}")

		print(f"GENRES?: {'genres' in m}")
		if 'genres' in m: print(m['genres'])
		print(f"KIND: {m['kind']}")
		try:
			self.info['genres'] = m['genres']
			self.info['kind'] = m['kind']
		except:
			print(">> - - - - - > WARNING: no m['genres'] or ['kind'] ?")

		print(f"CAST:")
		# for index, member in enumerate(m['cast']):
		#   print(index, member) # member['id']

		try:
			for index, member in enumerate(m['cast']):
				print(member)
				self.info['cast'].append(member)
				#if index > 15: break
		except:
			print(">> - - - - - > WARNING: no m['cast']")


		# this retreives low quality cover art
		#
		# https://m.media-amazon.com/images/M/MV5BNGVjNWI4ZGUtNzE0MS00YTJmLWE0ZDctN2ZiYT...
		# ...k2YmI3NTYyXkEyXkFqcGdeQXVyMTkxNjUyNQ@@._V1_SY150_CR0,0,101,150_.jpg
		#
		# Change ending @@._V1_SY300_CR0,0,201,300_.jpg
		#                    size ^    x,y,x1, y1
		try:
			print(f"COVER ART: {m['cover url']}")
			self.info['image_url'] = m['cover url']
			url = self.info['image_url']
		except:
			print(">> - - - - - > WARNING: no m['cover url']")

		if url == None:
			MMedia._badly_formatted_names.append(self.info['file_path'])
			self.info['movie_data_loaded'] = False # dont get hung up on failure
			return

		# url = urllib.parse.quote(url, safe='/:')  # replace spaces if there are any - urlencode
		# print(url)
		local_file_name = Path(self.info['file_path'].parent, f"{self.info['file_path'].stem}_dl_lowres.jpg")
		print(f"STORING lores IMAGE TO:\n{local_file_name}")
		urllib.request.urlretrieve(url, local_file_name)

		# this retreives better quality cover art
		local_file_name = Path(self.info['file_path'].parent, f"{self.info['file_path'].parent}")
		print(f"STORING hires IMAGE TO:\n{local_file_name}")

		result = get_hires_cover(self.info['file_title'], search_year, local_file_name)
		print("IMAGE_RETRIEVAL:")
		pprint(result)
		pprint(result.__class__)
		pprint(result.__class__.__name__)
		print('-')
		if result != None and result.__class__.__name__ == 'PosixPath':
			self.info['hires_image'] = result.name

		print(f"RETRIEVED hires IMAGE: {result} <")

		# from scrape
		# https://www.imdb.com/title/tt7286456/mediaviewer/rm3353122305
		#                          ID: 7286456
		#                       Title: Joker
		# TODO do integrity / minimum requiremnts check before setting True
		self.info['movie_data_loaded'] = True












from collections.abc import Iterable, Iterator
# collection.abc = abstract base class
# https://docs.python.org/3/library/collections.abc.html
#
# See - for __reversed__() method. HowTO
# class collections.abc.Reversible

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

# TODO - refactor - check presence of each - merge into one DB
mmdia_root2a = Path('/Volumes/time_box_2018/movies/')
PICKLED_MEDIA_LIB_FILE_V2_TIMEBOX = mmdia_root2a.joinpath('__media_data2','medialib2.pickle')
mmdia_root2b = Path('/Volumes/FAITHFUL500/')
PICKLED_MEDIA_LIB_FILE_V2_F500 = mmdia_root2b.joinpath('__media_data2','medialib2.pickle')
look_in_repo = Path('./movies/')	# git demo
PICKLED_MEDIA_LIB_FILE_REPO = look_in_repo.joinpath('__media_data2','medialib2.pickle')
look_in_linux = Path('/home/pi/MMdia/')
PICKLED_MEDIA_LIB_FILE_LINUX = look_in_linux.joinpath('__media_data2','medialib2.pickle')
look_in_linux = Path('/media/pi/time_box_2018/movies/')
PICKLED_MEDIA_LIB_FILE_LINUX_TIMEBOX = look_in_linux.joinpath('__media_data2','medialib2.pickle')
PICKLED_MEDIA_LIB_FILE_OSX4T = Path('/Volumes/Osx4T/tor/__media_data2/medialib2.pickle')
KNOWN_PATHS = [
	PICKLED_MEDIA_LIB_FILE_LINUX_TIMEBOX,
	PICKLED_MEDIA_LIB_FILE_OSX4T,
	PICKLED_MEDIA_LIB_FILE_V2_TIMEBOX,
	PICKLED_MEDIA_LIB_FILE_LINUX,
	PICKLED_MEDIA_LIB_FILE_V2_F500,
	#PICKLED_MEDIA_LIB_FILE_REPO,
]
READ_ONLY = 'r'
READ_WRITE = 'w'
class MMediaLib(Iterable):

	imdb_search = imdb.IMDb()

	def __init__( self, lib_file_path=PICKLED_MEDIA_LIB_FILE_V2_F500, media_root=None ):
		self.lib_file_path = lib_file_path
		self.media_root = media_root

		# create DB in directory of search path - ./media_root/__media_data2/medialib2.pickle
		if self.lib_file_path == None and media_root != None:
			self.lib_file_path = Path(media_root).joinpath('__media_data2','medialib2.pickle')

		if self.lib_file_path != None and media_root == None:
			self.media_root = self.lib_file_path.parent.parent

		if self.lib_file_path == None and media_root == None:
			raise NoRootDirectoryOrDBFound()

		if self.media_root == None:
			print(id(self))
			print(f"self.lib_file_path: {self.lib_file_path}")
			print(f"media_root: {media_root}")
			print(f"self.media_root: {self.media_root}")
			raise NoDBFileFound()


		self.read_write_mode = READ_ONLY

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
		self._id_to_movie_keys = {}

		print("MMediaLib: building sorted lists . . .")
		self.sort_lists()
		self.build_id_lookup()
		print(" . . . Done")


	def __iter__(self) -> MediaLibIter:					#  -> MediaLibIter is optional guide to coder & toolchain
		keys = list(self.media_files.keys())
		return MediaLibIter(self.media_files, keys)		#                  it indicates the return type

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
		# TODO - fix: TypeError: float() argument must be a string or a number, not 'NoneType' - probably Non record in data?
		#self._sorted_by_most_recently_added = sorted(self.media_files, key=lambda k: float(self.media_files[k].info['when_added']), reverse=True)

	def sorted_lists(self):
		lists = [self._sorted_by_year,self._sorted_by_title,self._sorted_by_rating,self._sorted_by_most_recently_added]
		lists_names = ["sorted_by_year","sorted_by_title","sorted_by_rating","sorted_by_most_recently_added"]
		for idx,l in enumerate(lists):
			print(f"{lists_names[idx]}- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - S")
			pprint(l)
			print(f"{lists_names[idx]}- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - E")
		return lists

	def build_id_lookup(self):
		for media_key in self.media_files.keys():
			media_id = self.media_files[media_key].info['id']
			self._id_to_movie_keys[media_id] = media_key

	def media_with_id(self, media_id):
		media_key = self._id_to_movie_keys[media_id]
		return self.media_files[media_key].info

	def rebase_media_DB(self, old_root, new_root):
		# this needs to be OS independant

		print(f"rebase_media_DB: \nfrom:{old_root} \nto:{new_root}\nself.media_root: {self.media_root}")

		#if self.media_root == old_root:
		self.media_root == new_root
		for key, movie in self.media_files.items():
			new_file_path = str(movie.info['file_path']).replace(old_root, new_root)
			movie.info['file_path'] = Path(new_file_path)
			#pprint(movie.info['file_path'])


	def __str__(self):
		return 'MMediaLib::def __str__'

	def __repr__(self):
		return 'MMediaLib::def __repr__'

	def __len__(self):
		return len(self.media_files)

	def inspect_directory_before_adding_to_library(self, search_dir = None):
		problem_match = []
		series_match = []

		search_dir = self.media_root if not search_dir else search_dir
		search_dir = Path(search_dir)

		# glob for files here
		for media_file in search_dir.glob('**/*'):
			if MMediaLib.is_accepted_media(media_file):

				mm = MMedia(media_file, {}, False)

				size = mm.get_media_size_in_mb()

				if (size > 400) and (mm.info['file_title'] == None):
					print('-- \ ')
					print(f"f: {mm.info['file_path']}")
					print(f"f: {mm.info['file_name']}")
					# search = re.search(r'[sS]\d\d[eE]\d\d',mm.info['file_name'])
					# print(f"search: {search} <")
					# if re.search(r'[sS]\d\d[eE]\d\d',str(mm.info['file_name'])): # series
					# 	print(f"SERIES: {mm.info['file_name']}")

					print(f"Found: Y:{mm.info['year']} < size:{size}Mb > Ft:{mm.info['file_title']} <  >\n")
					#pprint(mm)
					if re.search(r'[sS]\d\d\s*?[eE]\d\d',str(mm.info['file_name'])): # series
						series_match.append(mm.info['file_name'].lower())
					else:
						problem_match.append(mm.info['file_name'].lower())
					print('-- /')

		print("-------------------series_match-------------------")
		pprint(series_match)
		print("-------------------problem_match-------------------")
		pprint(problem_match)


	def add_directory_to_library(self, search_dir = None):

		search_dir = self.media_root if not search_dir else search_dir
		search_dir = Path(search_dir)

		# glob for files here
		for media_file in search_dir.glob('**/*'):
			if MMediaLib.is_accepted_media(media_file):
				self.add_media(media_file)


	def add_media(self, media_path):
		media_path = Path(media_path)

		if re.search(r'([sS]\d+?[eE]\d+?)|(\dx\d\d)', str(media_path)):
			print("MEDIA LOOK LIKE SERIES - SKIPPING\n{media_path}\n - - - - - ")
			return

		if self.is_new_media(media_path):
			print(f"\n\n\nADD NEW MEDIA: {media_path.name} type:{media_path.__class__.__name__}\n{media_path.parent}\n{media_path}")

			if not MMediaLib.is_valid_video(media_path):
				print(f"SKIPPING MEDIA: {media_path.name} FILE TOO SMALL or NOT recognised video format")
				return # raise & log TODO

			media = MMedia(media_path, {}, True)

			if media.info['movie_data_loaded'] == True:
				self.media_files_count[media.file_path().name.lower()] += 1
				self.media_files[media.file_path().name.lower()] = media
				print(f"*** ADDED NEW MEDIA: {media.file_path().name.lower()} type:{media_path.__class__.__name__}\n{media.file_path()}")
			else:
				print(f"WARNING movie_data_loaded = False \n<{media_path}>")

		elif self.media_files[media_path.name.lower()].info['movie_data_loaded'] == False:
			print(f"REPLACING MEDIA: {media_path.name} type:{media_path.__class__.__name__}\n{media_path.parent}")
			media = MMedia(media_path, {}, True)

		else:
			print(f"MEDIA ALREADY EXISTS: {media_path.name} loc:{media_path.parent}")
			pprint(self.media_files[media_path.name.lower()])

	#@classmethod	#def is_accepted_media(klass, file_name)
	@staticmethod	#def is_accepted_media(file_name)
	def is_accepted_media(file_name):
		#return ( Path(file_name).suffix.lower() in (AUDIO_EXTS + VIDEO_EXTS) )
		return ( Path(file_name).suffix.lower() in VIDEO_EXTS )

	@staticmethod
	def is_valid_video(video_path):
		valid = True
		video_path = Path(video_path)

		if ( video_path.suffix.lower() not in VIDEO_EXTS ): valid = False

		file_size = round(video_path.stat().st_size / (1024 * 1024),1)

		if file_size < 200: valid = False

		return valid

	def is_new_media(self, mfile):
		mfile = Path(mfile)

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
		print(f"R/W? - {self.read_write_mode}")
		if self.read_write_mode == READ_WRITE:
			# create directory if it doesn't exist
			self.lib_file_path.parent.mkdir(parents=True, exist_ok=True)
			print(f'PICKLING before EXIT: {self.lib_file_path}')
			print(f"SIZE: {len(self.media_files.keys())}")
			pprint(self.media_files.keys())
			print(" - - ")
			with open(self.lib_file_path, 'wb') as f:
				pickle.dump(self.media_files, f, pickle.HIGHEST_PROTOCOL)


	def list_DB_by_attribute(self, attribute='year', verbose=False):
		sort_type = {
			'year'	:self.sorted_by_year,
			'title' :self.sorted_by_title,
			'rating':self.sorted_by_rating,
			'recent':self.sorted_by_most_recently_added
		}

		if attribute in sort_type:
			self.sorted_iterator = sort_type[attribute]
			last = None
			for m in self.sorted_iterator():
				if verbose == True:
					print(f" - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - S")
					pprint(m)
				else:
					#if m == {} or m.info['title'] == 'And Then There Were None':
					print(m)
					last = m
			#pprint(last)
			print(f"Entries: {len(self.media_files)}")
		else:
			print(f"**WARNING** INVALID -l option. Sort types: {' '.join(sort_type.keys())}\n\n")
			raise IncorrectSortAttributeError(attribute)

		return(last)


	LOCAL_IMAGE_CACHE_DEFAULT = Path('/tmp')
	def cache_images_locally(self, cache_dir=LOCAL_IMAGE_CACHE_DEFAULT):
		cached_files = []
		cache_dir = Path(cache_dir)

		print(f"MMediaLib: caching images to local disc: {cache_dir}")
		print(f"MMediaLib: from: {self.media_root}")
		for mv_file_name,media in self.media_files.items():
			#print("- - - - - - - - - - - - - - - - - - - - - - - - - S")
			#pprint(media)
			info = media.info
			if info['hires_image']:
				cache_image = cache_dir.joinpath(Path(info['hires_image']).name)
				source_path = info['file_path'].parent
				source_image = source_path.joinpath(info['hires_image'])
				#print(f"{source_image}")
				#print(f"{cache_image}")
				if not source_image.exists():
					print(f"WARNING SOURCE IMAGE <{source_image}> NOT FOUND ***** < < <")
					#TODO raise error thsi shouldn't happen
					continue
				if cache_image.exists():
					#print(f"PRESENT: {cache_image}")
					pass
				else:		# move image
					#print(f"Moving {source_image} to {cache_image}")
					shutil.copy(source_image, cache_image)
					cached_files.append(source_image.name)
			else:
				print(f"USE LORES: {info['image_url']}")
			#print("- - - - - - - - - - - - - - - - - - - - - - - - - E")
		print(f"COPIED {len(cached_files)} images to cache: {cache_dir}")

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# HELPERS
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def get_list_of_file_extensions(search_dir = None):
	extensions = Counter()
	search_dir = Path(search_dir)

	if search_dir.exists():
		for p in search_dir.glob('**/*'):
			extensions[p.suffix.lower()] += 1
	else:
		print(f'ERROR invalid path: {search_dir}')

	return extensions


# given the kind and query select the most appropriate result
# from the list returned by the query
LOWEST_DOC_DISTANCE = 0
MOVIE = 0
DOC_DIST = 1
def select_best_item_from_search_results(kind, query, results):
	result = None
	right_kind = []
	doc_distances = {}

	possible_kinds = ['movie', 'tv series', 'tv mini series', 'video game', 'video movie', 'tv movie', 'episode']

	if kind not in possible_kinds:
		kind == 'movie'

	# collect result of the right 'kind'
	for i,r in enumerate(results):
		print(f"{i} - {r['title']}")
		if r['kind'] == kind:
			right_kind.append(r)

	print(f"Found {len(right_kind)} of the right_kind . .")
	pprint(right_kind)

	# walk search results and find best match
	for sr in right_kind:
		search_vector = get_doc_vector_word(query)

		result_title_with_year = sr['title']
		try:
			result_title_with_year = f"{sr['title']} {sr['year']}"
		except KeyError:
			print("select_best_item_from_search_results")
			pprint(sr)
			traceback.print_exc()
			print(" - - ^ ^ - - ")
		finally:
			result_vector = get_doc_vector_word(result_title_with_year)

		doc_distances[sr] = doc_distance(search_vector, result_vector)
		print(f"\nQRY:{query}\n\nRESULT: {result_title_with_year}\nd_d:{doc_distances[sr]}")
		pprint(sr)

	try:
		result = sorted(doc_distances.items(), key=lambda item: item[1])[LOWEST_DOC_DISTANCE][MOVIE]
	except:
		print(">> - - - - - > WARNING: sorting issue  --S ")
		pprint(right_kind)
		print(">> - - - - - > WARNING: sorting issue  --M ")
		pprint(doc_distances)
		print(">> - - - - - > WARNING: sorting issue  --E ")

	return result


# put smaller vector 1st!
def inner_product(v1,v2):
	sum = 0.0

	for symbol1 in v1:                # go through keys
		if symbol1 in v2:
			sum += v1[symbol1] * v2[symbol1]

	return sum


#def vector_angle(d1, d2):
def doc_distance(d1, d2):
	"""
	Return the angle between these two vectors.
	"""
	numerator = inner_product(d1,d2)
	denominator = math.sqrt(inner_product(d1,d1)*inner_product(d2,d2))

	return math.acos(numerator/denominator)


def get_doc_vector_word(doc):
	# remove non alphanumeric and white space
	#print(f"get_doc_vector_word 0:{doc}")
	doc = re.sub(r'[\W_]',' ',doc)
	#print(f"get_doc_vector_word 1:{doc}")

	# split into words
	doc_words = doc.split()
	#print(f"get_doc_vector_word 2:{doc}")
	#pprint(doc_words)

	# create vector
	vector = Counter()
	for w in doc_words:
	  vector[w] += 1

	#print("get_doc_vector_word 3:")
	#pprint(vector)

	return vector




def main():
	pass


if __name__ == '__main__':
	#'/Volumes/meep/temp_delete/'
	#Path('/Volumes/Home Directory/MMdia/')

	# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
	# -help = list file extensions found
	if ('-h' in sys.argv) or ('-help' in sys.argv) or ('--help' in sys.argv):
		print(
'''
- - Help / Exmple use - -
$ cd path
$ .pe										# alias .pe='. venv/bin/activate'
$ ./moviepicker/moviepicker.py 				# plug in all disks - will report each DB contents &
											# DUPLICATES that appear across discs

											# list movies in DB - ldb
$ ./moviepicker/moviepicker.py -ldb /Volumes/Osx4T/tor/__media_data2/medialib2.pickle

$ ./moviepicker/moviepicker.py -u -d 		# find info about new additions to movie directory
											# - dummy run (NO WRITE)
$ ./moviepicker/moviepicker.py -u   		# find info about new additions to movie directory UPDATE DB

option
-ec 			print list of file extension found on default target
-ec /path/		print list of file extension found on path

-d  			run but don't save results to disk (dummy run)
-u 				udate entries on default target
-u /path/		udate entries on default target with path
				NOT IMPLEMENTED - TODO

-udev	update from local repo movie directory

-ldb /path/medialib2.pickle 	list entries in a pickleDB
-ldr /path/media 				list potential entries in a target directory ??

'''
		)
		sys.exit()

	# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
	# load media lib
	# timebox_media_lib = MMediaLib()	# default
	# new_media_lib = timebox_media_lib
	#
	# repo_media_lib = MMediaLib(PICKLED_MEDIA_LIB_FILE_REPO)
	# new_media_lib = repo_media_lib

	# alt_media_lib = MMediaLib(None,'/Volumes/time_box_2018/movies_Chris/__for_chris/movies_recomended') # create DB.pickle in search dir
	# new_media_lib = alt_media_lib
	# print(f"** movie picker main() - new_media_lib: {new_media_lib.media_root} **")



	#
	#
	# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
	# -ec = list file extensions found
	if '-ec' in sys.argv:
		try:
			ec_path = Path(sys.argv[sys.argv.index('-ec')+1])
			print(f"option -ec: {ec_path}")
			if ec_path.exists():
				pprint(get_list_of_file_extensions(ec_path))
			else:
				print(f'ERROR invalid path: {ec_path}')
			# '.mp4': 126, '.mkv': 85, '.wmv': 74, '.avi': 51,
		except IndexError:
			print(f"ERROR option -ec requires a path to check!\n EG: moviepicker.py -ec /Volumes/movies")

		sys.exit()


	# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -



	# TODO - the 'And Then There Were None' bug
	# - possible due to video title incorrectly extracted from file?
	# - querie imdb with None and the closest result is 'And Then There Were None'

	pprint(sys.argv)

	# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
	# -udev update dev directory
	if '-udev' in sys.argv:
		new_media_lib = MMediaLib(None, Path('/Users/simon/a_syllabus/lang/python/repos/movie_picker/movies'))
		new_media_lib.add_directory_to_library()


	# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
	# -u dir_name = update searching in directory for media
	if '-u' in sys.argv:
		# PICKLED_MEDIA_LIB_FILE_V2_TIMEBOX
		# PICKLED_MEDIA_LIB_FILE_V2_F500
		# PICKLED_MEDIA_LIB_FILE_REPO
		#new_media_lib = MMediaLib(PICKLED_MEDIA_LIB_FILE_V2_F500)	# default
		#new_media_lib = MMediaLib(PICKLED_MEDIA_LIB_FILE_V2_TIMEBOX)
		#new_media_lib = MMediaLib(PICKLED_MEDIA_LIB_FILE_REPO)
		#new_media_lib = MMediaLib(PICKLED_MEDIA_LIB_FILE_OSX4T)
		new_media_lib = MMediaLib(PICKLED_MEDIA_LIB_FILE_LINUX_TIMEBOX)

		if '-d' not in sys.argv:	# -d = dont save results		as in WRITE mode unless blocked
			new_media_lib.set_write_mode(READ_WRITE)

		#new_media_lib.add_directory_to_library('/Volumes/Home Directory/MMdia/')
		#Path('/Volumes/FAITHFUL500/')
		new_media_lib.add_directory_to_library()	# will look in the PICKLED_MEDIA_ROOT

		# try:
		# 	search_directory = sys.argv[sys.argv.index('-u')+1]
		#
		# 	if Path(search_directory).exists():
		# 		new_media_lib.add_directory_to_library(search_directory)
		#
		# except IndexError:
		# 	new_media_lib.add_directory_to_library()

	# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
	# list entries in a pickleDB
	# -ldb		/path/medialib2.pickle
	if '-ldb' in sys.argv:
		try:
			db_path = Path(sys.argv[sys.argv.index('-ldb')+1])
			print(f"option -ldb: {db_path}")
			if db_path.exists():
				new_media_lib = MMediaLib(db_path)
				last_movie = new_media_lib.list_DB_by_attribute()
				pprint(last_movie)
		except IndexError:
			print(f"ERROR option -ldb requires a path to check!\n EG: moviepicker.py -ldb /Volumes/media/__media_data2/medialib2.pickle")


	# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
	# list potential entries in a target directory
	# -ldr		/path/media
	if '-ldr' in sys.argv:
		try:
			dir_path = Path(sys.argv[sys.argv.index('-ldr')+1])
			print(f"option -ldr: {dir_path}")
			if dir_path.exists():
				new_media_lib = MMediaLib()
				new_media_lib.inspect_directory_before_adding_to_library()
				print("\n\nMMedia._badly_formatted_names")
				pprint(MMedia._badly_formatted_names)

		except IndexError:
			print(f"ERROR option -ldr requires a path to check!\n EG: moviepicker.py -ldr /Volumes/media/")


	# json check
	# for m in new_media_lib:
	# 	print(m.as_json())

	mmdbs = []
	for db_path in KNOWN_PATHS:
		if db_path.exists():
			mmdbs.append(MMediaLib(db_path))

	import shutil
	remove_from_disc = 'FAITHFUL500' # 'time_box_2018' 'meep' 'Osx4T'
	remove_duplicates = False			# remove duplicates PARENT directory & ALL contents

	all_media = {}
	duplicates = []
	for mmdb in mmdbs:
		print(f"\n\nDB Location: {mmdb.media_root} < - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
		for m in mmdb.media_files:
			#pprint(mmdb.media_files[m])
			if m not in all_media.keys():
				all_media[m] = mmdb.media_files[m]
				print(m)
			else:
				splitpath = str(all_media[m].info['file_path']).split('/')
				report = f"{(all_media[m].info['title']).ljust(40)} in {(splitpath[2]).ljust(20)} and {(str(mmdb.media_root).split('/')[2]).ljust(20)}"
				duplicates.append(report)
				duplicate_in = (str(mmdb.media_root).split('/')[2])
				loop_report = f"{(all_media[m].info['title']).ljust(40)} in {(splitpath[2]).ljust(20)} and {duplicate_in.ljust(20)}"
				print(loop_report)
				if duplicate_in == remove_from_disc and remove_duplicates == True:
					target_path = mmdb.media_files[m].info['file_path'].parent
					print(f"\t\t{mmdb.media_files[m].info['file_path']}\n\t\t{target_path}")
					# remove duplicate directories
					try:
						shutil.rmtree(target_path)
					except:
						pass


	import random
	print("\n\n\nMedia Object\n\n\n:")
	pprint( random.choice(list(all_media.items())) ) # pprint a randon dict item to look at object

	print("\n\nDUPLICATES:")
	for d in duplicates:
		print(d)

	print(f"\n\nUnique movies: {len(all_media)}")


	print(f"Available DATABASES:")
	# for mmdb in mmdbs:
	# 	print(f"Lib:{mmdb.media_root} - Movies:{len(mmdb.media_files)}") #
	# 	mmdb.list_DB_by_attribute()
	#
	mmdb_any = None
	for mmdb in mmdbs:
		mmdb_any = mmdb
		print(f"Lib:{mmdb.media_root} - Movies:{len(mmdb.media_files)}") #

	# # test get media byt ID
	# print("- - - - - - - - - - - - - - - - - - - - - - - - -  mmdb_any.media_with_id('0076929') - - - - - - - - - - - - - - - - - - - - - - - - - " )
	# print( mmdb_any.media_with_id('0076929') )
	# print("- - - - - - - - - - - - - - - - - - - - - - - - -  mmdb_any.media_with_id('0076929') - - - - - - - - - - - - - - - - - - - - - - - - - " )

	sys.exit()			# MMediaLib() pickles info on exit - in case crash / Ctrl+C during building DB

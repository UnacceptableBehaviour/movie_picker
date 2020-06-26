#! /usr/bin/env python
from pathlib import Path
from .helpers import creation_date, hr_readable_from_nix
from .mp_exceptions import *
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
import math
import traceback
import json

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
			'file_name': None,				# actually full path - refactor
			'file_title': None,
			'when_added': None,				# TODO - add epoch now
			'movie_data_loaded': False
		}
		
		if file_path != None:
			self.get_media_name_and_year_from_disc()
			print(f"Found: Y:{self.info['year']} <  Title:{self.info['file_title']} < \n") #Bad: {MMedia._badly_formatted_names[-1]} <\n")
			if imdb_query == True:
				self.query_imdb_for_movie_info()
				
		else:
			self.info.update(mmdia_info)

	def as_json_str(self):
		media = self.info.copy()
		#media['cast'] = [ (str(actor), actor.getID()) for actor in media['cast'] ] # name & ID
		media['cast'] = [ str(actor) for actor in media['cast'] ]
		media['file_path'] = str(media['file_path'])
		return json.dumps(media)

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

	def get_media_name_and_year_from_disc(self):

		if self.is_video():
			# movies
			# looking for: name followed by year or (year) or [year] resolution bla bla .ext
			# r'[\(\)\[\]]?\d\d\d\d[\(\)\[\]]?[\.\b]' - 4 digit year followed by . or word boundary      
			match = re.search(r'(.*?)[\(\)\[\]]?(\d\d\d\d)[\(\)\[\]]?[\.\b]', self.info['file_path'].stem, re.I )
			if match:
				self.info['year'] = match.group(2)
				dirty_title = match.group(1)
				dirty_title = re.sub(r'^[\W_]*','',dirty_title)     # remove leading non word
				dirty_title = re.sub(r'[\W_]*$','',dirty_title)     # remove trailing non word
				cleaned_up_title = re.sub(r'[\._]',' ',dirty_title) # replace . and underscore with space
				self.info['file_title'] = cleaned_up_title
			else:
				MMedia._badly_formatted_names.append(self.info['file_path'].stem)
		
		elif self.is_audio():
			pass

	# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
	# USING imdb module
	# Usage (keys): https://imdbpy.readthedocs.io/en/latest/usage/movie.html#movies
	# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
	def query_imdb_for_movie_info(self):
		
		seach_year = self.info['year'] if len(str(self.info['year'])) > 3 else ''
		
		query = f"{self.info['file_title']} {seach_year}"
		
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
			MMediaLib._badly_formatted_names.append(self.info['file_path'])
			self.info['movie_data_loaded'] = True # dont get hung up on failure
			return      
		
		self.info['id'] = movie.movieID
		
		m = MMediaLib.imdb_search.get_movie(movie.movieID)
		#print(MMediaLib.imdb_search.get_movie_infoset())
		
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
		for synopsis in m.get('plot'):
			# caballo grande ande on no ande!
			if plot_size < len(synopsis):
				plot_size = len(synopsis)
				self.info['synopsis'] = synopsis
				print(f"SYNOPSIS:\n{synopsis}")

		print(f"\nSYNOPSIS PICKED:\n{synopsis}")        
		
		
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
				if index > 15: break
		except:
			print(">> - - - - - > WARNING: no m['cast']")


		# this retreives low quality cover art
		#
		# https://m.media-amazon.com/images/M/MV5BNGVjNWI4ZGUtNzE0MS00YTJmLWE0ZDctN2ZiYT...
		# ...k2YmI3NTYyXkEyXkFqcGdeQXVyMTkxNjUyNQ@@._V1_SY150_CR0,0,101,150_.jpg
		#
		# Change ending @@._V1_SY300_CR0,0,201,300_.jpg
		#                    size ^    x,y,x1, y1
		print(f"COVER ART: {m['cover url']}")
		try:
			self.info['image_url'] = m['cover url']
			url = self.info['image_url']
		except:
			print(">> - - - - - > WARNING: no m['cover url']")

		# url = urllib.parse.quote(url, safe='/:')  # replace spaces if there are any - urlencode
		# print(url)    
		local_file_name = Path(self.info['file_path'].parent, f"{self.info['file_path'].stem}_dl.jpg")
		print(f"STORING IMAGE TO:\n{local_file_name}")
		urllib.request.urlretrieve(url, local_file_name)
		#urllib.request.urlretrieve(url, Path('./scratch', f"{self.info['file_path'].stem}.jpg"))
		
		# from scrape
		# https://www.imdb.com/title/tt7286456/mediaviewer/rm3353122305
		#                          ID: 7286456
		#                       Title: Joker
		# TODO do integrity / minimum requiremnts check before setting True
		self.info['movie_data_loaded'] = True










	

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
look_in_repo = Path('./movies/')	# git demo
PICKLED_MEDIA_LIB_FILE_REPO = look_in_repo.joinpath('__media_data2','medialib2.pickle')
READ_ONLY = 'r'
READ_WRITE = 'w'
class MMediaLib(Iterable):

	imdb_search = imdb.IMDb()

	def __init__( self, lib_file_path=PICKLED_MEDIA_LIB_FILE_V2, media_root=None ):
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

	def sorted_lists(self):
		lists = [self._sorted_by_year,self._sorted_by_title,self._sorted_by_rating,self._sorted_by_most_recently_added]
		lists_names = ["sorted_by_year","sorted_by_title","sorted_by_rating","sorted_by_most_recently_added"]
		for idx,l in enumerate(lists):
			print(f"{lists_names[idx]}- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - S")
			pprint(l)
			print(f"{lists_names[idx]}- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - E")
		return lists

	
		
	def __str__(self):	
		return 'MMediaLib::def __str__'

	def __repr__(self):   
		return 'MMediaLib::def __repr__'  

	def __len__(self):
		return len(self.media_files)

	def inspect_directory_before_adding_to_library(self, search_dir = None):
	
		search_dir = self.media_root if not search_dir else search_dir		
		search_dir = Path(search_dir)
		
		# glob for files here		
		for media_file in search_dir.glob('**/*'):			
			if MMediaLib.is_accepted_media(media_file):
				print(media_file)
				MMedia(media_file, {}, False)

	def add_directory_to_library(self, search_dir = None):
	
		search_dir = self.media_root if not search_dir else search_dir		
		search_dir = Path(search_dir)
		
		# glob for files here		
		for media_file in search_dir.glob('**/*'):
			if MMediaLib.is_accepted_media(media_file):
				self.add_media(media_file)
			

	def add_media(self, media_path):
		media_path = Path(media_path)
						
		if self.is_new_media(media_path):
			print(f"ADD NEW MEDIA: {media_path.name} type:{media_path.__class__.__name__}\n{media_path.parent}")			
			
			media = MMedia(media_path, {}, True)
		
			self.media_files_count[media.file_path().name.lower()] += 1
			self.media_files[media.file_path().name.lower()] = media
		else:
			print(f"MEDIA ALREADY EXISTS: {media_path.name()} loc:{media_path.parent}")
			pprint(self.media_files[media_path.name])
	
	#@classmethod	#def is_accepted_media(klass, file_name)
	@staticmethod	#def is_accepted_media(file_name)
	def is_accepted_media(file_name):
		return ( Path(file_name).suffix.lower() in (AUDIO_EXTS + VIDEO_EXTS) )

	# # ** DEPRACATED ** was for importing legacy data **
	# def add_media_legacy(self, media):		
	# 	# TODO raise if incorrect type
	# 	
	# 	print(f"ADD MEDIA: {media.file_path()} type:{media.__class__.__name__}")
	# 	if self.is_new_media(media.file_path()):
	# 		print(f"NEW MEDIA: {media.file_path()}")
	# 		# TODO add check to see if info['movie_data_loaded']: False
	# 		# load it if not
	# 		if not media.data_loaded:
	# 			print(f"DATA LOADED?: {media.data_loaded()}")
	# 			media = MMedia(media.file_path(), {})
	# 	
	# 		self.media_files_count[media.file_path().name.lower()] += 1
	# 		self.media_files[media.file_path().name.lower()] = media
							

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
			#third_key = list(self.media_files.keys())[2] ; print(f"Entry type {type(self.media_files[third_key])} ")
			print(f"SIZE: {len(self.media_files.keys())}") 
			with open(self.lib_file_path, 'wb') as f:
				pickle.dump(self.media_files, f, pickle.HIGHEST_PROTOCOL)	


	def list_DB_by_attribute(self, attribute='recent', verbose=False):
		sort_type = {
			'year'	:self.sorted_by_year,				
			'title' :self.sorted_by_title,
			'rating':self.sorted_by_rating,				
			'recent':self.sorted_by_most_recently_added
		}
				
		if attribute in sort_type:
			self.sorted_iterator = sort_type[attribute]
			for m in self.sorted_iterator():			
				if verbose == True:
					print(f" - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - S")
					pprint(m)
				else:
					#if m == {} or m.info['title'] == 'And Then There Were None':
					print(m)
		else:
			print(f"**WARNING** INVALID -l option. Sort types: {' '.join(sort_type.keys())}\n\n")
			raise IncorrectSortAttributeError(attribute)
	
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# HELPERS
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def get_list_of_file_extensions(search_dir = None):
	extensions = Counter()
	
	search_dir = mmdia_root2 if not search_dir else search_dir
	
	for p in search_dir.glob('**/*'):
		extensions[p.suffix.lower()] += 1
	
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
	
	# walk saerch results and find best match  
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

	# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
	# load media lib
	
	# timebox_media_lib = MMediaLib()	# default
	# new_media_lib = timebox_media_lib
	# 
	# repo_media_lib = MMediaLib(PICKLED_MEDIA_LIB_FILE_REPO)
	# new_media_lib = repo_media_lib
	
	alt_media_lib = MMediaLib(None,'/Volumes/time_box_2018/movies_Chris/__for_chris/movies_recomended') # create DB.pickle in search dir
	new_media_lib = alt_media_lib
	print(f"** movie picker main() - new_media_lib: {new_media_lib.media_root} **")
	
	
	# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
	# -ec = dont save results
	if '-ec' in sys.argv:
		pprint(get_list_of_file_extensions())
		# '.mp4': 126, '.mkv': 85, '.wmv': 74, '.avi': 51,
		sys.exit()
	
	
	# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
	# -d = dont save results		as in WRITE mode unless blocked
	if '-d' not in sys.argv:
		new_media_lib.set_write_mode(READ_WRITE)

	
	# TODO - the 'And Then There Were None' bug
	# - possible due to video title incorrectly extracted from file?
	# - querie imdb with None and the closest result is 'And Then There Were None'
	
	pprint(sys.argv)

	# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
	# -u dir_name = update searching in directory for media
	if '-u' in sys.argv:
		new_media_lib.add_directory_to_library()
		# try: 
		# 	search_directory = sys.argv[sys.argv.index('-u')+1]
		# 	
		# 	if Path(search_directory).exists():
		# 		new_media_lib.add_directory_to_library(search_directory)
		# 
		# except IndexError:
		# 	new_media_lib.add_directory_to_library()

	
	if '-l' in sys.argv:
		try:
			print(f"option -l: {sys.argv[sys.argv.index('-l')+1]}")
			new_media_lib.list_DB_by_attribute(attribute=sys.argv[sys.argv.index('-l')+1])
		except IndexError:		
			if len(new_media_lib) == 0:
				print(f"Inspecting: {new_media_lib.media_root}")
				new_media_lib.inspect_directory_before_adding_to_library()
				pprint(MMedia._badly_formatted_names)			
			else:
				for m in new_media_lib:
					print(f"{str(m).ljust(60)}\t{m.info['file_name']}")
				
	# json check			
	# for m in new_media_lib:
	# 	print(m.as_json_str())
	
	sys.exit()			# MMediaLib() pickles info on exit - in case crash / Ctrl+C during building DB

	# # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
	# # importing library from old script
	# from pprint import pprint
	# from movie_info_disk import get_MMdia_lib, MMdia
	#
	# print("** movie picker main() - new_media_lib **")
	# new_media_lib = MMediaLib()
	# new_media_lib.set_write_mode(READ_WRITE)
	# 
	# # convert to new classes for pickling - import data
	# print("** movie picker main() - old_media_lib **")
	# old_media_lib = get_MMdia_lib()
	# 
	# for count, (movie,media) in enumerate(old_media_lib['video'].items()):
	# 	print(f" - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - << S {count}")
	# 	pprint(media)
	# 	print(" - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - << M")
	# 	print(f"== {str(count).rjust(3)} - - - - - - - - - - - - - - - - - - - - - ")		
	# 	file_stats = Path(old_media_lib['video'][movie].full_path).stat() # refresh stats
	# 	file_size = (str( round(file_stats.st_size / (1024 * 1024),1))+'MB').rjust(6)
	# 	file_path = old_media_lib['video'][movie].full_path
	# 	added_epoch = creation_date(file_path)
	# 	print(file_stats)
	# 	print(f"epoch added: {added_epoch} - {hr_readable_from_nix(added_epoch)}")
	# 	
	# 	print(f"== {str(count).rjust(3)} - {file_size} - {movie}")
	# 	media.movie_data['movie_data_loaded'] = media.movie_data_loaded
	# 	media.movie_data['hires_image'] = media.hires_image
	# 	media.movie_data['file_path'] = file_path
	# 	media.movie_data['file_name'] = movie
	# 	media.movie_data['file_stats'] = file_stats
	# 	media.movie_data['when_added'] = added_epoch
	# 	new_media_type = MMedia(media.movie_data)
	# 	new_media_lib.add_media_legacy(new_media_type)						
	# 	print(" - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - << M2")
	# 	pprint(new_media_type)
	# 	print(" - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - << E")
	# 	#if count > 5: break
	# 
	# sys.exit()
	# # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
	
	# # ah dict.keys() returns dict_keys(['f1', 'f2', 'f3', 'f4']) type 
	# a = {'f1': MMedia({'title': 'F1'}),
	# 	 'f2': MMedia({'title': 'F2'}),
	# 	 'f3': MMedia({'title': 'F3'}),
	# 	 'f4': MMedia({'title': 'F4'}) }
	# 
	# b = [key for key in a.keys()]	# use list comprehension to convert
	# 
	# pprint(b)		

	# # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
	# # dumb info from DB
	# count = 0
	# #for m in new_media_lib.sorted_by_year():
	# #for m in new_media_lib.sorted_by_title():
	# for m in new_media_lib.sorted_by_rating():
	# #for m in new_media_lib.sorted_by_most_recently_added():
	# 	if m == {} or m.info['title'] == 'And Then There Were None':
	# 		continue
	# 	print(m)
	# 	# print(f" - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - << S {count}")
	# 	# pprint(m)
	# 	# print(dir(m))		
	# 	# print(f" - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - << E {count}")
	# 	# count += 1
	# 	# if count > 15:
	# 	# 	break

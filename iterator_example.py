#! /usr/bin/env python

# from example
# https://www.slideshare.net/DamianGordon1/python-the-iterator-pattern
# (2c3df72cf70ff3760096b8deae038995ebbbe076)
# &
# https://refactoring.guru/design-patterns/iterator/python/example#:~:text=Iterator%20in%20Python,using%20a%20single%20iterator%20interface.
# 

from collections.abc import Iterable, Iterator
# collection.abc = abstract base class
# https://docs.python.org/3/library/collections.abc.html


import sys		# sys.exit()
from pprint import pprint

FORWARD = 1
REVERSE = -1
class MediaLibIter(Iterator):
	'''
	Iterator designed for MediaLib inherits from Iterator base class
	'''
	def __init__(self, media_list, direction=FORWARD):
		self.direction = REVERSE if direction==REVERSE else FORWARD 	# has to be FORWARD or REVERSE!
		self._index = -1 if direction==REVERSE else 0					# start at index 0 if going forward -1 if reversing
		self.media_files = media_list

	def __iter__(self):				# use?
		return self
	
	def __next__(self):
		try:
			return_item = self.media_files[self._index]			
			self._index += self.direction
	
		except IndexError:
			raise StopIteration()
	
		return return_item
	

class Movie:	
	def __init__(self, name, year, rating):
		self.title = name
		self.year = year
		self.rating = rating
		
	def __str__(self):
		return f"{self.year} {self.rating.rjust(4)} - {self.title}"

	def __repr__(self):
		return f"{self.year} {self.rating.rjust(4)} - {self.title}"
	
	def __lt__(self):	# support bisect or http://code.activestate.com/recipes/577197-sortedcollection/
		pass			# in dir ./scripts 


class MediaLib(Iterable):
	def __init__(self, media_list=[]):
		self.media_files = media_list
		self.sort_lists()

	def add_media(self, media):		
		self.media_files.append(media)
		# http://code.activestate.com/recipes/577197-sortedcollection/
		self.sort_lists() 	# TODO maintain a sorted collection ^
		
	def sort_lists(self):
		self._sorted_by_year = sorted(self.media_files, key=lambda x: x.year)	# in place media_files.sort(key=lambda x: x.year)
		self._sorted_by_title = sorted(self.media_files, key=lambda x: x.title)
		self._sorted_by_rating = sorted(self.media_files, key=lambda x: float(x.rating), reverse=True)

	def __iter__(self) -> MediaLibIter:									#  -> MediaLibIter is optional guide to coder & toolchain
		return MediaLibIter(self.media_files)
	
	def reverse_each(self) -> MediaLibIter:
		return MediaLibIter(self.media_files, direction=REVERSE)
	
	def sorted_by_year(self, direction=FORWARD) -> MediaLibIter:
		#direction = REVERSE if direction==REVERSE else FORWARD			# check done in iterato redundant
		return MediaLibIter(self._sorted_by_year, direction)	
	
	def sorted_by_title(self, direction=FORWARD) -> MediaLibIter:
		return MediaLibIter(self._sorted_by_title, direction)	
	
	def sorted_by_rating(self, direction=FORWARD) -> MediaLibIter:
		return MediaLibIter(self._sorted_by_rating, direction)
		
	


def main():
	
	titles = ['The Big Short','A Star Is Born','Annihilation','Alita: Battle Angel','Bill Burr: Why Do I Do This?','Joker','Shallow Grave','The Thirteenth Floor','The Great Hack']
	year = ['2015','2018','2018','2019','2008','2019','1994','1999','2019']
	rating = ['7.8','7.7','6.9','7.3','8.4','8.5','7.3','7.1','7.0']	
	
	movies = []
	for title, year, rating in zip(titles, year, rating):
		movies.append(Movie(title, year, rating))
	
	media_library = MediaLib(movies)
	
	for media in media_library:
		print(media)
	
	media_library.add_media(Movie("The Rattlers Cage",'2020','10.0'))
	
	print(". . and for my next trick . . . BACKWARDS . . . ooh!")
	
	for media in media_library.reverse_each():
		print(media)

	print(". . and for my next trick . . . SORTED BY YEAR . . . aaah!")
	
	for media in media_library.sorted_by_year():
		print(media)

	print(". . and for my next trick . . . SORTED YEAR BACKWARDS . . . waah!?")
	
	for media in media_library.sorted_by_year(REVERSE):
		print(media)

if __name__ == '__main__':

	main()
						
	sys.exit()			# MMediaLib() pickles info on exit - in case crash / Ctrl+C during building DB
		

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# Notes
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# -> notation after method definition is a return type hint
# :  natation inside signature brackets preceeds a return type hint
#
# def __init__(self, collection: List[Any] = []) -> None:			# w/ hints
# same as
# def __init__(self, collection = []):								# unadorned
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
#
# def greeting(name):
#   return 'Hello, {}'.format(name)
# 
# can be written
# 
# def greeting(name: str) -> str:
#   return 'Hello, {}'.format(name)
# to indicate types (not enforced but useful for toolchain)
# Ref: https://stackoverflow.com/questions/5336320/how-to-know-function-return-type-and-argument-types

# You can also alias types:
#
# from typing import List
# Vector = List[float]
# def scale(scalar: float, vector: Vector) -> Vector:
#     return [scalar * num for num in vector]
# 
# > scale(2.0, [1.0, -4.2, 5.4])
# > [2.0, -8.4, 10.8]
#
#
# Type aliases are useful for simplifying complex type signatures. For example: 
# from typing import Dict, Tuple, Sequence
# 
# ConnectionOptions = Dict[str, str]
# Address = Tuple[str, int]
# Server = Tuple[Address, ConnectionOptions]
# 
# def broadcast_message(message: str, servers: Sequence[Server]) -> None:
#     ...
# 
# # The static type checker will treat the previous type signature as
# # being exactly equivalent to this one.
# def broadcast_message(
#         message: str,
#         servers: Sequence[Tuple[Tuple[str, int], Dict[str, str]]]) -> None:
# 
# Ref: https://docs.python.org/3/library/typing.html



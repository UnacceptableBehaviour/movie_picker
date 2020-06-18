#! /usr/bin/env python

# from example
# https://www.slideshare.net/DamianGordon1/python-the-iterator-pattern
# &
# https://refactoring.guru/design-patterns/iterator/python/example#:~:text=Iterator%20in%20Python,using%20a%20single%20iterator%20interface.

from collections.abc import Iterable, Iterator
# collection.abc = abstract base class
# https://docs.python.org/3/library/collections.abc.html


import sys		# sys.exit()


class Movies:
	def __init__(self, name, year, rating):
		pass


class MediaLib(Iterable):
	def __init__(self, media_list=[]):
		self.media_files = media_list

	def __iter__(self):		
		return MediaLibIter(self.media_files)
	
	
	
class MediaLibIter(Iterator):
	'''
	Iterator designed for MediaLib inherits from Iterator base class
	'''
	def __init__(self, media_list):
		self._index = 0
		self.media_files = media_list

	def __iter__(self):				# use?
		return self
	
	def __next__(self):
		#print(f"idx:{self._index + 1} - {len(self.media_files)} - {self.media_files[self._index]}")
		if self._index + 1 < len(self.media_files):
			return_item = self.media_files[self._index]
			self._index += 1	
			return return_item
		else:
			raise StopIteration()

		

def main():
	movies = ['The Big Short','A Star Is Born','Annihilation','Alita: Battle Angel','Bill Burr: Why Do I Do This?','Food Inc','Joker','Shallow Grave','The Thirteenth Floor','The Great Hack','District 9','Taxi','Taxi Driver']
	
	media_library = MediaLib(movies)
	
	for media in media_library:
		print(media)
	


if __name__ == '__main__':

	main()
						
	sys.exit()			# MMediaLib() pickles info on exit - in case crash / Ctrl+C during building DB
		

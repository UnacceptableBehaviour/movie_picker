# add exception used in module here

# # https://docs.python.org/3/tutorial/errors.html
# # For example, the following code will print B, C, D in that order:
#
# # ** Note that if the except clauses were reversed (with except B first),
# # it would have printed B, B, B  the FIRST matching except clause is triggered.
# class B(Exception):
#     pass
# 
# class C(B):
#     pass
# 
# class D(C):
#     pass
# 
# for cls in [B, C, D]:
#     try:
#         raise cls()			# calls B(), then C()  then D()
#     except D:				# triggered by D(C(B))
#         print("D")
#     except C:				# triggered by C(B)
#         print("C")
#     except B:				# triggered by B()
#         print("B")

# try:
# 	with open('ingredient_db.json', 'w') as f:
# 		f.write(json.dumps(ingredient_db))
# 	
# except (NotImplementedError, DemoMultipleCatch) as e:
# 	print("WARNING FAILED to commit DB to disk")
# 	print(f"\n***\n{e} \n<")
# 
# finally:
# 	# make sure this happens
# 	pass

class MMediaLibError(Exception):
    '''TODO Move this and other error classes to separate file: exceptions.py'''
    pass

class NoDBFileFound(MMediaLibError):
    '''failed to evaluate a root directory or .pickle file to load'''
    pass

class NoRootDirectoryOrDBFound(MMediaLibError):
    '''failed to evaluate .pickle file to load'''
    pass

class IncorrectSortAttributeError(MMediaLibError):
	'''sorting attribute past to iterator invalid'''
	def __init__(self, attribute):
		self.attribute = attribute
		return(f"IncorrectSortAttributeError - {self.attribute} invalid.")


# from wikipedia exceptions
# """
# Global wikipedia exception and warning classes.
# """
# 
# import sys
# 
# 
# ODD_ERROR_MESSAGE = "This shouldn't happen. Please report on GitHub: github.com/goldsmith/Wikipedia"
# 
# 
# class WikipediaException(Exception):
#   """Base Wikipedia exception class."""
# 
#   def __init__(self, error):
#     self.error = error
# 
#   def __unicode__(self):
#     return "An unknown error occured: \"{0}\". Please report it on GitHub!".format(self.error)
# 
#   if sys.version_info > (3, 0):
#     def __str__(self):
#       return self.__unicode__()
# 
#   else:
#     def __str__(self):
#       return self.__unicode__().encode('utf8')
# 
# 
# class PageError(WikipediaException):
#   """Exception raised when no Wikipedia matched a query."""
# 
#   def __init__(self, pageid=None, *args):
#     if pageid:
#       self.pageid = pageid
#     else:
#       self.title = args[0]
# 
#   def __unicode__(self):
#     if hasattr(self, 'title'):
#       return u"\"{0}\" does not match any pages. Try another query!".format(self.title)
#     else:
#       return u"Page id \"{0}\" does not match any pages. Try another id!".format(self.pageid)
# 
# 
# class DisambiguationError(WikipediaException):
#   """
#   Exception raised when a page resolves to a Disambiguation page.
# 
#   The `options` property contains a list of titles
#   of Wikipedia pages that the query may refer to.
# 
#   .. note:: `options` does not include titles that do not link to a valid Wikipedia page.
#   """
# 
#   def __init__(self, title, may_refer_to):
#     self.title = title
#     self.options = may_refer_to
# 
#   def __unicode__(self):
#     return u"\"{0}\" may refer to: \n{1}".format(self.title, '\n'.join(self.options))
# 
# 
# class RedirectError(WikipediaException):
#   """Exception raised when a page title unexpectedly resolves to a redirect."""
# 
#   def __init__(self, title):
#     self.title = title
# 
#   def __unicode__(self):
#     return u"\"{0}\" resulted in a redirect. Set the redirect property to True to allow automatic redirects.".format(self.title)
# 
# 
# class HTTPTimeoutError(WikipediaException):
#   """Exception raised when a request to the Mediawiki servers times out."""
# 
#   def __init__(self, query):
#     self.query = query
# 
#   def __unicode__(self):
#     return u"Searching for \"{0}\" resulted in a timeout. Try again in a few seconds, and make sure you have rate limiting set to True.".format(self.query)
# 

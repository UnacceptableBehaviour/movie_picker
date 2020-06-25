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
		print(f"IncorrectSortAttributeError - {self.attribute} invalid")


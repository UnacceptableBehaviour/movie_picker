# add exception used in module here

# experimental - understanding syntax and python style . . TODO


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
#         raise cls()            # calls B(), then C()  then D()
#     except D:                # triggered by D(C(B))
#         print("D")
#     except C:                # triggered by C(B)
#         print("C")
#     except B:                # triggered by B()
#         print("B")

# try:
#     with open('ingredient_db.json', 'w') as f:
#         f.write(json.dumps(ingredient_db))
#     
# except (NotImplementedError, DemoMultipleCatch) as e:
#     print("WARNING FAILED to commit DB to disk")
#     print(f"\n***\n{e} \n<")
#
# else:
#     # executes only if no exception is raised in try block
#     pass
# 
# finally:
#     # make sure this happens
#     pass

# Create specialised exception for lib - that way if you need you change dependencies the app
# doesn't need to know about it - encapsulation


from pprint import pprint

class MMediaLibError(Exception):
    '''Base exception used by this module.'''
    def __init__(self, *args):
        if args:
            self.message = args[0]
            self.args = args
            self.log_exception()
        else:
            self.message = None
    
    def __str__(self):
        return(f"MMediaLibError.__str__ {self.__class__.__name__} : Error: '{self.message}' <")
        
    def log_exception(self):
        print(self)
        pprint(self.args)
        print("> - - -")
        # implement logging
        

class MMediaLibWarning(Warning):
    '''Base warning used by this module.'''
    pass



class HelpersError(MMediaLibError):
    '''base class for Helper errors'''
    pass

class RetrievalError(MMediaLibError):
    '''base class for Helper errors'''
    pass

class MMediaError(MMediaLibError):
    '''base class for Helper errors'''
    pass

class MediaLibIterError(MMediaLibError):
    '''base class for MediaLibIterError errors'''
    pass

class WikipediaError(MMediaLibError):
    '''base class for Helper errors'''
    pass



# Log exception to file - TODO


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

    def __str__(self):
        return(f"{self.__class__.__name__} Sorting attribute: '{self.attribute}' invalid.")

class IncorrectURLForImageRetrieval(RetrievalError):
    '''failure to locate wiki page for image'''
    def __init__(self, msg, url):
        #MMediaLibError.__init__(self, msg, url) # 2.7
        super().__init__(msg, url)               # 3.x # super() -> same as super(__class__, self)
    


#! /usr/bin/env python

# prototype / test - for parsing commands from CLI
# basics: ArgumentParser
# https://docs.python.org/3/howto/argparse.html
#
# ArgumentParser - docs
# https://docs.python.org/3/library/argparse.html#type

# taking had written help like this and generating help using ArgumentParser (Python stdLib)
example_help = '''
- - Help / Exmple use - -
$ cd path
$ .pe                                        # alias .pe='. venv/bin/activate'
$ ./moviepicker/moviepicker.py                 # plug in all disks - will report each DB contents &
                                            # DUPLICATES that appear across discs

                                            # list movies in DB - ldb
$ ./moviepicker/moviepicker.py -ldb /Volumes/Osx4T/tor/__media_data2/medialib2.pickle

$ ./moviepicker/moviepicker.py -u -d         # find info about new additions to movie directory
                                            # - dummy run (NO WRITE)
$ ./moviepicker/moviepicker.py -u           # find info about new additions to movie directory UPDATE DB

option
-ec             print list of file extension found on default target
-ec /path/        print list of file extension found on path

-d              run but don't save results to disk (dummy run)
-u                 udate entries on default target
-u /path/        udate entries on default target with path

-udev    update from local repo movie directory

-ldb /path/medialib2.pickle     list entries in a pickleDB
-ldr /path/media                 list potential entries in a target directory ??

'''


def main(args):
    pass



if __name__ == "__main__":
    from pprint import pprint
    import sys


    # parse arges
    import argparse
    parser = argparse.ArgumentParser(exit_on_error=False,
                                     description='This is a lead in to the help describing the program.\n\n',
                                     epilog='Bug reports to https://github.com/UnacceptableBehaviour.')

    # exit_on_error=False       allows exception to be caught on error instead of direct exit
    #
    # annoyingly description & epilog scrub \n so appear as continous text!? :/



    #print(example_help)

    # examples how to process different types of optiona & arguments

    # NON - OPTIONAL argv[1], argv[2]
    # COMMENT IN next two lines

    parser.add_argument("argv_1", help="path to media files")                         # argv[1]   - ORDER DEPENDANT
    parser.add_argument("argv_2", type=int, help="max number of new media to add")    # argv[2]   - can use ANY name
    # ./scripts/cli_parse.py ./movies 10
    # Namespace(argv_1='./movies', argv_2='10', update=False, dummy=False)


    # --option      - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # -o
    parser.add_argument("-u", "--update", help="scan for new media & update database ", action="store_true")
    parser.add_argument("-d", "--dummy", help="dummy run - report only - NO database update", action="store_true")
    # ./scripts/cli_parse.py -u         Namespace(dummy=False, update=True)
    # ./scripts/cli_parse.py -u -d      Namespace(dummy=True, update=True)
    # ./scripts/cli_parse.py -ud        Namespace(dummy=True, update=True)
    #
    # ./scripts/cli_parse.py -h
        # usage: cli_parse.py [-h] [-u] [-d]
        #
        # optional arguments:
        #   -h, --help    show this help message and exit
        #   -u, --update  scan for new media & update database              << order dependent on how added above ^
        #   -d, --dummy   dummy run - report only - NO database update

    # --option value [coices for value]   - - - - - - - - - - - - - - - - - - - - - - - - -
    parser.add_argument("-v", "--verbosity", type=int, choices=[0, 1, 2], help="set output verbosity")

    # list entries in a pickleDB   - - - - - - - - - - - - - - - - - - - - - - - - -
    # --list_entries_db NON optional_target
    # -ldb /path/    print list of file extension found on path
    parser.add_argument("-ldb", "--list_entries_db", type=open, help="list media in DBname.pickle at PATH")
    # ./scripts/cli_parse.py -ldb                   < argument missing
    #                                                           |
    # usage: cli_parse.py [-h] [-u] [-d] [-v {0,1,2}] [-ldb LIST_ENTRIES_DB]
    # cli_parse.py: error: argument -ldb/--list_entries_db: expected one argument

    # specify DB to scan / update - - - - - - - - - - - - - - - - - - - - - - - - -
    # --specify_db NON optional_target
    # -db /path/    print list of file extension found on path
    parser.add_argument("-db", "--specify_db", type=open, help="specify PATH of DB to scan / update")

    # list entries in a pickleDB   - - - - - - - - - - - - - - - - - - - - - - - - -
    # --list_new_entries_in_dir NON optional_target
    # -lnd /path/    print list of file extension found on path
    parser.add_argument("-lnd", "--list_new_entries_in_dir", type=open, help="scan PATH for new media & in specified DB")

    # --extension_scan optional_target       - - - - - - - - - - - - - - - - - - -
    # -ec             print list of file extension found on default target
    # -ec /path/    print list of file extension found on path


    # --push comment       - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # -p comnt
    # -p handle missing val
    parser.add_argument("-p", "--push", type=ascii, help="push commits to remote with COMMENT")


    # list of values    - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # file1.cpp file2.cpp file3.c

    # --update --dummy    - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # -u -d
    # -ud

    commit_comment = None
    try:
        args = parser.parse_args()      # returns Namespace()
    except Exception as e:
        pprint(vars(e))
        pprint(e)
        pprint(e.argument_name)
        pprint(sys.argv)
        args = None
        if '-p' in e.argument_name:
            commit_comment = input("Commit comment:")   # user forgot comment collect and continue

        # need to re-parse
        sys.argv.remove('-p')               # remove offending arg
        args = parser.parse_args()          # retry & let argparse report other issues if any issue
        #args.add('push', commit_comment)   # handle some other way

    print(vars(args))
    if commit_comment:
        print(f"Commit comment: {commit_comment}")


# missing a commit comment
# $ ./scripts/cli_parse.py /forty/five 90 -v 2 -db /Volumes/Osx4T/tor/__media_data2/medialib2.pickle -p
#
# {'argument_name': '-p/--push', 'message': 'expected one argument'}
# ArgumentError(_StoreAction(option_strings=['-p', '--push'], dest='push', nargs=None, const=None, default=None, type=<built-in function ascii>, choices=None, help='push commits to remote with COMMENT', metavar=None), 'expected one argument')
# '-p/--push'
# ['./scripts/cli_parse.py',
#  '/forty/five',
#  '90',
#  '-v',
#  '2',
#  '-db',
#  '/Volumes/Osx4T/tor/__media_data2/medialib2.pickle',
#  '-p']
# Commit comment:ardvaark

# final args object + collected comment
# {'argv_1': '/forty/five', 'argv_2': 90, 'update': False, 'dummy': False, 'verbosity': 2, 'list_entries_db': None, 'specify_db': <_io.TextIOWrapper name='/Volumes/Osx4T/tor/__media_data2/medialib2.pickle' mode='r' encoding='UTF-8'>, 'list_new_entries_in_dir': None, 'push': None}
# Commit comment: ardvaark




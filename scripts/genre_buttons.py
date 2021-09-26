#! /usr/bin/env python

# see notes at head of thrd_sk_producer.py

# button_html = "<button type='submit' class='btn-genre' name='sort_type' formmethod='post' value='genre_type'>button_text</button>"
#
# genre_type = ['history','war','sci-fi','music','sport','romance','adventure','action','mystery','thriller','documentary','musical','biography','news','fantasy','animation','family','crime','drama','comedy','horror','western']
#
# for g in genre_type:
#     s1 = button_html.replace("genre_type",g)
#     s2 = s1.replace("button_text",g)
#     print(s2)
#
# ## # # # #
# from pathlib import Path
#
# USER_DB_FILE = Path('./moviepicker/userDB.json')
#
# json_db = None
# with open(USER_DB_FILE, 'r') as f:
#     json_db = f.read()
#
#
# make_upper = ['History','War','Sci-Fi','Music','Sport','Romance','Adventure','Action','Mystery','Thriller','Documentary','Musical','Biography','News','Fantasy','Animation','Family','Crime','Drama','Comedy','Horror','Western']
#
# print(json_db)
#
# for genre in make_upper:
#     gl = genre.lower()
#     json_db = json_db.replace(gl, genre)
#
# print(json_db)
#
# with open(USER_DB_FILE, 'w') as f:
#     f.write(json_db)

# short_list no dupes multiple mentions at the top

from collections import Counter

sl = [0,1,2,3,4,1,6,2,2,4,7,4,6,6,3,5,2,4,5,3,5,7,2,3,4,8]

print(sl)
# [0, 1, 2, 3, 4, 1, 6, 2, 2, 4, 7, 4, 6, 6, 3, 5, 2, 4, 5, 3, 5, 7, 2, 3, 4, 8]

print(sorted(sl))
# [0, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 4, 5, 5, 5, 6, 6, 6, 7, 7, 8]
#  1    2         5             4            5           3        3       2   1

print('-')
print(Counter(sl))
# Counter({2: 5, 4: 5, 3: 4, 6: 3, 5: 3, 1: 2, 7: 2, 0: 1, 8: 1})

print(Counter(sl).most_common())
# [(2, 5), (4, 5), (3, 4), (6, 3), (5, 3), (1, 2), (7, 2), (0, 1), (8, 1)]

print([ n for n,count in Counter(sl).most_common() ])
#[2, 4, 3, 6, 5, 1, 7, 0, 8]   # ordered by frequency and if thats the same by first encountered


s2 = [7,2,3,4,8]
s2.remove(3)
print(s2)
print('removing not present cause exception? - YES ValueError: list.remove(x): x not in list' )
#s2.remove(3)
#print(s2)

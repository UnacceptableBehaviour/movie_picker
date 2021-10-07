#! /usr/bin/env python
from pathlib import Path
import shutil
from pprint import pprint




# const FILES_TO_CACHE = [
#   '/static/offline.html',
# ];

# def get_list_of_potential_files_to_cache(search_path, cache_root):
#     paths = []
#     dir_before_root = str(search_path).split('/')[str(search_path).split('/').index(cache_root)-1]
#
#     print('const FILES_TO_CACHE = [')
#
#     for p in search_path.glob('**/*'):
#         if p.is_dir() or '.DS_Store' in str(p): continue
#         comps = str(p).split(dir_before_root)
#         cache_targets = Path(comps[1])
#         print(f"  '{cache_targets}',")
#         paths.append(cache_targets)
#
#     print('];')
#
#     return paths

from_disc = Path('/Volumes/Osx4T/tor')
to_disc = Path('/Volumes/nfs/nfs_C1_2TB_THX1138/tor')

def compare_discs(from_disc, to_disc):
    f_gen = Path(from_disc).glob('**/*')
    t_gen = Path(to_disc).glob('**/*')

    from_files = []
    to_files = []

    show_count = 500
    cnt = 0
    from_root = str(from_disc)
    print(f"from_files: {from_root} - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
    for f in f_gen:
        cnt += 1
        from_files.append(str(f).replace(from_root,''))
        #if cnt > show_count: break

    cnt = 0
    to_root = str(to_disc)
    print(f"to_files {to_root} - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
    for f in t_gen:
        cnt += 1
        no_root = str(f).replace(to_root,'')
        #print(f"{cnt} - {no_root}\n\t{from_files[cnt]}")
        if no_root in from_files:
            #print(f"\tfound in source ({cnt}): {no_root}")
            from_files.remove(no_root)
        else:
            #print(f"\tnot in target ({cnt}): {no_root}")
            to_files.append(no_root)
        #if cnt > show_count: break

    print(f"files to copy: {len(from_files)}")

    # return files on the from_disc not on the to_disc
    return(from_files)

def copy_missing_files(from_disc, missing_files, to_disc):
    print('tag_debug_2')
    f = 'arse'
    print(f"from: {Path(from_disc,f)}\nto:{(Path(to_disc,f))}")
    # return
    for f in missing_files:
        whole_p = str(to_disc) + f
        target_dir = Path(whole_p).parent
        print(f"td_w: {target_dir}")
        from_file = Path( str(from_disc) + f )
        to_file = Path( str(to_disc) + f )
        print(f"td_f: {from_file}")
        print(f"td_t: {to_file}")

        if not target_dir.exists():
            print(f"mkdir: {target_dir}")
            Path(target_dir).mkdir(parents=True, exist_ok=True)

        if from_file.is_dir():
            print(f"\tmkdir: {from_file}")
            Path(from_file).mkdir(parents=True, exist_ok=True)
        else:
            print(f"\tcopy from: {from_file}\n\t\tto:{to_file}")
            shutil.copy(from_file, to_file)




def main():
    pass


if __name__ == '__main__':

    #paths = get_list_of_potential_files_to_cache(project_root, 'static')
    missing_files = compare_discs(from_disc, to_disc)
    copy_missing_files(from_disc, missing_files, to_disc)
    print(f"files to copy: {len(missing_files)}")

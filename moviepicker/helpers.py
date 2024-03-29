import os
import platform
from datetime import datetime


def creation_date(path_to_file):
    """
    Try to get the date that a file was created, falling back to when it was
    last modified if that isn't possible.
    See http://stackoverflow.com/a/39501288/1709587 for explanation.
    """
    if platform.system() == 'Windows':
        return os.path.getctime(path_to_file)
    else:
        stat = os.stat(path_to_file)
        try:
            return stat.st_birthtime
        except AttributeError:
            # We're probably on Linux. No easy way to get creation dates here,
            # so we'll settle for when its content was last modified.
            return stat.st_mtime


def hr_readable_from_nix(nix_time):
    if nix_time:
        return datetime.utcfromtimestamp(nix_time).strftime("%Y %m %d %H%M")

def hr_readable_from_nix_no_space(nix_time):
    if nix_time:
        return datetime.utcfromtimestamp(nix_time).strftime("%Y%m%d%H%M")

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil
import tarfile

TAR_FILE='flash_player_npapi_linux.x86_64.tar.gz'
PLUGIN_FILE='libflashplayer.so'
DIR_TO='/usr/lib/flashplugin-nonfree/'

def main():
    if not os.path.exists(TAR_FILE):
        print("%s not found" % TAR_FILE)
        return -1
    
    tar = tarfile.open(TAR_FILE)
    tar.extract(PLUGIN_FILE)
    path_to = os.path.join(DIR_TO,PLUGIN_FILE)
    if os.path.exists(path_to):
        os.remove(path_to)
    shutil.move(PLUGIN_FILE,DIR_TO)
    
    print("finished")
    return 0

if __name__ == '__main__':
    main()


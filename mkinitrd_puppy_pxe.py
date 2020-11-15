#!/usr/bin/env python3

import shutil
import os
from yoshi.util import exec_command
import re
import glob

#定数
INITRD='initrd.gz'
INITRD_BIG='initrd_big.gz'
SRC_DIR=os.path.abspath('.')
TMP_DIR='temp'
USER='yoshi'
GROUP='yoshi'

def main():
    #create TMP_DIR
    if os.path.exists(TMP_DIR):
        shutil.rmtree(TMP_DIR)
    if os.path.exists(INITRD_BIG):
        os.remove(INITRD_BIG)
    os.mkdir(TMP_DIR)
           
    #copy .sfs to TMP_DIR
    re1=re.compile(r'.+\.(sfs|SFS)$')
    print("copying *.sfs to temp dir:")
    for file in glob.glob(os.path.join(SRC_DIR,'*')):
        if re1.match(file):
            print(file)
            shutil.copy(file,TMP_DIR)
    
    #add .sfs to new initrd.gz
    os.chdir(TMP_DIR)
    print("extracting %s" % INITRD)
    command = 'zcat %s | cpio -i -H newc -d' % os.path.join(SRC_DIR,INITRD)
    retcode,stdout,stderr=exec_command(command,'utf-8' )
    print(stdout,stderr,end="")
    if retcode != 0:
        raise Exception("error at [{}]".format(command))
    print("making %s" % INITRD_BIG)
    command = 'find | cpio -o -H newc | gzip -4 > ../%s' % INITRD_BIG
    retcode,stdout,stderr=exec_command(command,'utf-8')
    print(stdout,stderr,end="")
    if retcode != 0:
        raise Exception("error at [{}]".format(command) )
    os.chdir('..')
    shutil.chown(INITRD_BIG,USER,GROUP)

    shutil.rmtree(TMP_DIR)
    print("%s created" % INITRD_BIG)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)

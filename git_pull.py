#!/usr/bin/env python3
"""
exec "git pull" in directories under current directory
"""

import os
from yoshi.util import exec_command

def list_git_dirs(start_dir):
    dirs = []
    for dir in os.listdir(start_dir):
        path = os.path.join(dir,".git")
        if os.path.exists(path):
            dirs.append(os.path.abspath(dir))
    return dirs

def main():
    cwd = os.getcwd()
    for dir in list_git_dirs("."):
        print(dir+":")
        os.chdir(dir)
        retcode,stdout,stderr=exec_command("git pull",'utf-8' )
        if retcode:
            raise Exception(stderr)
        else:
            print(stdout)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)


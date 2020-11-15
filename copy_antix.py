#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os.path
import shutil
from pathlib import Path
import subprocess
import yaml
import traceback
import itertools
import threading
import time
from yoshi.util import copy_with_progress

CONF_FILE = ".config/copy_antix.conf"

class Process:

    def __init__(self,src,dst,add_new):
        self.SRC_DIR = src
        self.DST_DIR = dst
        self.ADD_NEW = add_new

    def copy_files(self):
        if not os.path.exists(self.SRC_DIR):
            raise Exception("%s not found" % self.SRC_DIR)

        if not os.path.exists(self.DST_DIR):
            raise Exception("%s not found" % self.DST_DIR)

        print("coping from {} to {}".format(self.SRC_DIR,self.DST_DIR))
        for name in ["linuxfs","rootfs"]:
            if self.ADD_NEW !='y':
                src_file = os.path.join(self.SRC_DIR,name+".new")
            else:
                src_file = os.path.join(self.SRC_DIR,name)
            if not os.path.exists(src_file):
                raise Exception("%s not found" % src_file)

            dst_file = os.path.join(self.DST_DIR,name+".new")
            copy_with_progress(src=src_file,dst=dst_file)

    def main(self):
        self.copy_files() 

def read_conf():
    if not os.path.exists(CONF_FILE):
        raise Exception("{} not found.".format(CONF_FILE))
    with open(CONF_FILE,"r",encoding="utf-8") as f:
        return yaml.safe_load(f) 

if __name__ == '__main__':

    config = read_conf()

    while True:
        settings = list(config.keys())
        for i in range(1,len(settings)+1):
            setting = settings[i-1]
            print("{}:{} [{} → {},{}]".format(
                i,
                setting,
                config[setting]["SRC_DIR"],
                config[setting]["DST_DIR"],
                "add .new" if  config[setting]["ADD_NEW"] == 'y' else "copy .new"
                ))
        print("select setting(1-{})/'q' to quit:".format(len(settings)),end="")
        c = input()
        if c.isdecimal() and int(c)>0 and int(c) <= len(settings):
            setting = settings[int(c)-1]
        elif c == 'q':
            exit(0)
        else:
            continue

        proc=Process(
            config[setting]["SRC_DIR"],
            config[setting]["DST_DIR"],
            config[setting]["ADD_NEW"]
            )
        err=False
        try:
            proc.main()
            print("completed")
        except Exception as e:
            print("error:{}".format(e))
            err=True
        if not err:
            break


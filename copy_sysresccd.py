#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os.path
import shutil
from pathlib import Path
import configparser
import traceback
import yaml
import subprocess
from yoshi.util import copy_with_progress

CONF_FILE='.config/copy_sysresccd.conf'
DIR_SYSRESCCD='sysresccd'
ISO_PATTERN='systemrescue-*.iso'
#When TYPE=ISO,iso iamage file is copied to this file
ISO_FILE='systemrecsue.iso'

class Process:


    def __init__(self,type,dir_to):
        self.type = type
        self.DIR_ISO = config["DIR_ISO"]
        self.DIR_TO = dir_to
        self.DIR_MOUNT = config["DIR_MOUNT"]
        self.iso =""

    def find_iso(self):
        if not os.path.exists(self.DIR_ISO):
            raise Exception("%s not found" % self.DIR_ISO)

        p = Path(self.DIR_ISO)
        isos = list(p.glob(ISO_PATTERN))
        if len(isos) == 0:
            raise Exception(ISO_PATTERN+" not found")

        self.iso = isos[0]
        print("found '%s'" % self.iso)

    def mount_iso(self):
        #mount iso
        if not os.path.exists(self.DIR_MOUNT):
            raise Exception("%s not found" % self.DIR_MOUNT)

        if os.path.ismount(self.DIR_MOUNT):
            raise Exception("%s is already mounted" % self.DIR_MOUNT)

        cmd = "mount {} {}".format(self.iso,self.DIR_MOUNT)
        if subprocess.call(cmd, shell=True):
            raise Exception("'%s' failed" % cmd)

    def copy_dir(self,dir_from,dir_to):
        #check copy from dir
        if not os.path.exists(dir_from):
            raise Exception("src-dir %s not found" % dir_from)

        #remove old dir
        if os.path.exists(dir_to):
            shutil.rmtree(dir_to)

        #copy dir
        print("copying from '{}' to '{}'".format(dir_from,dir_to))
        shutil.copytree(dir_from,dir_to,copy_function=copy_with_progress)

    def umount_iso(self):
        if not os.path.ismount(self.DIR_MOUNT):
            return
            
        #umount iso
        cmd = "umount {}".format(self.DIR_MOUNT)
        if subprocess.call(cmd, shell=True):
            print("'%s' failed" % cmd)

    def main(self):
        err = None
        if self.type == 'DIR':
            try:
                self.find_iso()
                self.mount_iso()
                dir_from = os.path.join(self.DIR_MOUNT,DIR_SYSRESCCD)
                dir_to = os.path.join(self.DIR_TO,DIR_SYSRESCCD)
                self.copy_dir(dir_from,dir_to)
            
            except Exception as e:
                err = e
            finally:
                self.umount_iso()
        
        elif self.type == 'ISO':
            try:
                self.find_iso()
                src_file = os.path.join(self.DIR_ISO,self.iso)
                dst_file = os.path.join(self.DIR_TO,ISO_FILE)
                copy_with_progress(src=src_file,dst=dst_file)
            
            except Exception as e:
                err = e
                print("error==>\n{}<==".format(traceback.format_exc()))

        if err:
            raise err

def read_conf():
    if not os.path.exists(CONF_FILE):
        raise Exception("{} not found.".format(CONF_FILE))
    with open(CONF_FILE,"r",encoding="utf-8") as f:
        return yaml.safe_load(f) 

if __name__ == '__main__':
    config = read_conf()
    print("DIR_ISO:{}".format(config["DIR_ISO"]))
    while True:
        settings = list(config["settings"].keys())
        for i in range(1,len(settings)+1):
            setting = settings[i-1]
            print("{}:{} {} {}".format(
                i,
                setting,
                "copy-dir" if config["settings"][setting]["TYPE"] == "DIR" else "copy-iso",
                config["settings"][setting]["DIR_TO"],
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
            config["settings"][setting]["TYPE"],
            config["settings"][setting]["DIR_TO"]
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


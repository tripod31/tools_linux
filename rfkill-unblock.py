#!/usr/bin/env python3
#rfkill unblock

import configparser
import os
import syslog
import subprocess
import json

MSG_TITLE='rfkill-unblock'
DEV_TYPES=('wlan','bluetooth')

class Process:

    def __init__(self):
        pass

    def get_states(self):
        """
        get rfkill softblock state
        returns:{dev_type:unblock or block}
        """
        ret = {}
        proc = subprocess.run("rfkill -J", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if proc.returncode != 0:
            raise Exception("rfkill exec err")
        
        info = json.loads(proc.stdout)
        if not '' in info:
            raise Exception("rfkill parse err:key('')not exists")
        for dev in info['']:
            if not 'type' in dev:
                raise Exception("rfkill parse err:key('type') not exists")
            for type in DEV_TYPES:
                if dev['type'] == type:
                    ret[type] = dev['soft']
        return ret

    def unblock(self,type):
        proc = subprocess.run("rfkill unblock {}".format(type), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if proc.returncode != 0:
            raise Exception("rfkill exec err")

    def main(self):
        #os.chdir(os.path.dirname(__file__)) #chdir to script path
        syslog.openlog(MSG_TITLE)   
        states = self.get_states()
        for type in DEV_TYPES:
            if type in states and states[type] == 'blocked':
                self.unblock(type)     
                syslog.syslog("unblock {}".format(type))

if __name__ == '__main__':
    obj = Process()
    obj.main()

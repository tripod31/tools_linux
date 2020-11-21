#!/usr/bin/env python3
#log CPU temp

import configparser
import traceback
import sys
import time
import os
import logging
import subprocess

class Process:
    CONF_FILE=".config/log_temp.conf"

    def __init__(self):
        self.TEMP_FILE=""
        self.INTERVAL_MIN=10

    def read_config(self):
        if not os.path.exists(Process.CONF_FILE):
            raise Exception("%s not found" % Process.CONF_FILE)
        config = configparser.ConfigParser()
        with open(Process.CONF_FILE,'r') as f:
            config.read_file(f)
            f.close()
        self.TEMP_FILE=config["settings"]["temp_file"]
        self.INTERVAL_MIN=int(config["settings"]["interval_min"])

    def check_already_running(self):
        """
        check if process is already running
        Returns
        -------
            : bool
        """
        file_name = os.path.basename(__file__)
        p1 = subprocess.Popen(["ps", "-ef"], stdout=subprocess.PIPE)
        p2 = subprocess.Popen(["grep", file_name], stdin=p1.stdout, stdout=subprocess.PIPE)
        p3 = subprocess.Popen(["grep", "python3"], stdin=p2.stdout, stdout=subprocess.PIPE)
        p4 = subprocess.Popen(["wc", "-l"], stdin=p3.stdout, stdout=subprocess.PIPE)
        p1.stdout.close()
        p2.stdout.close()
        p3.stdout.close()
        output = p4.communicate()[0].decode("utf8").replace('\n','')
        return True if int(output != 1) else False

    def main(self):
        if self.check_already_running():
            print("already running.exit.")
            sys.exit(-1)

        os.chdir(os.path.dirname(__file__)) #chdir to script path
        self.read_config()
        logging.basicConfig(
            filename='log/log_temp.log',
            format='%(asctime)-15s %(message)s',
            level=logging.DEBUG)
        logging.info("start logging")
        while True:
            with open(self.TEMP_FILE,'r') as f:
                temp = f.read()
                logging.info(temp.strip())
            time.sleep(60 * self.INTERVAL_MIN)

if __name__ == '__main__':
    obj = Process()
    obj.main()

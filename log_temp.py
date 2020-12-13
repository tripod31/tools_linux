#!/usr/bin/env python3
#log CPU temp

import configparser
import os
import logging

class Process:
    CONF_FILE=".config/log_temp.conf"

    def __init__(self):
        self.TEMP_FILE=""

    def read_config(self):
        if not os.path.exists(Process.CONF_FILE):
            raise Exception("%s not found" % Process.CONF_FILE)
        config = configparser.ConfigParser()
        with open(Process.CONF_FILE,'r') as f:
            config.read_file(f)
            f.close()
        self.TEMP_FILE=config["settings"]["temp_file"]

    def main(self):
        os.chdir(os.path.dirname(__file__)) #chdir to script path
        self.read_config()
        logging.basicConfig(
            filename='log/log_temp.log',
            format='%(asctime)-15s %(message)s',
            level=logging.DEBUG)

        with open(self.TEMP_FILE,'r') as f:
            temp = f.read()
            logging.info(temp.strip())

if __name__ == '__main__':
    obj = Process()
    obj.main()

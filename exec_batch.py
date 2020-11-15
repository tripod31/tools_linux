#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
バッチ起動メニュー
ARGV[1]   メニューの定義ファイル(YAML形式)
'''
import sys
import os
import yaml
from yoshi.util import exec_command
import argparse
import platform
import pprint

#グローバル
g_settings ={}

def get_system_encoding():
    system = platform.system()
    enc = ""
    if system == "Windows":
        enc = "cp932"
    elif system == "Linux":
        enc = "utf-8"
    return enc

def exec_task(task):
    print("[実行:%s]" % g_settings["tasks"][task]["desc"])
        
    commands=g_settings["tasks"][task]["command"]
    for command in commands:
        try:
            cmd= command.format(**g_settings["vars"])
        except Exception as e:
            print(e)
            break
        
        print ("コマンド実行 :[%s]" % cmd)
        ret,stdout,stderr =exec_command(cmd,get_system_encoding())
        if len(stdout)>0:
            print (stdout)
        if ret !=0:
            print ("[コマンド実行中エラー]\n%s" % stderr)
            break

def print_task(task):
    print("[処理内容:%s %s]" % (task,g_settings["tasks"][task]["desc"]))
        
    commands=g_settings["tasks"][task]["command"]
    for command in commands:
        try:
            cmd= command.format(**g_settings["vars"])   #eval variable in command
        except Exception as e:
            print(e)
            break
        
        print ( cmd)
        
def read_yaml(yamlf):
    global g_settings
    try:
        #yamlf =os.path.join(os.path.dirname(__file__),yamlf)
        if not os.path.exists(yamlf):
            raise Exception("%sがありません" % yamlf)
        with open(yamlf,"r") as f:
            g_settings = yaml.safe_load(f) 

    except Exception as e:
        print("%s読込エラー:%s" % (args.yamlfile,e))
        return -1

    if g_settings["vars"] is None:
        g_settings["vars"]={}

    #print("[vars]")
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint( g_settings["vars"])
    """
    for k,v in g_settings["vars"].items():
        print ("%-20s%s" % (k,v))
    """
    return 0

def print_tasks():
    for task in sorted(g_settings["tasks"].keys()):
        print( "%-10s%s"%(task,g_settings["tasks"][task]["desc"]))
        print("---")
        for command in g_settings["tasks"][task]["command"]:
            print (command)
        print("")

if __name__ == '__main__':
    #引数
    parser = argparse.ArgumentParser()
    parser.add_argument('yamlfile')
    args=parser.parse_args()
    
    if read_yaml(args.yamlfile) != 0:
        print("Enterを入力:",end="")
        dummy = input()
        sys.exit()

    while True:
        print ("[メニュー]") 
        for task in sorted(g_settings["tasks"].keys()):
            print( "%-10s%s"%(task+":",g_settings["tasks"][task]["desc"]))
    
        task=""
        while True:
            task = input("[タスク番号？(p+タスク番号:タスク内容表示 r:タスク再読込 q:終了)]:")
            if len(task) == 0:
                continue

            if task[0] == 'p':
                task = task[1:]
                if task in g_settings["tasks"].keys():
                    print_task(task)
                break
            
            if task == 'r':
                print ("[タスク再読込]")
                read_yaml(args.yamlfile)
                break
            
            if task == 'q':
                print("[終了]")
                sys.exit()
            
            if task in g_settings["tasks"].keys():
                exec_task(task)
                break

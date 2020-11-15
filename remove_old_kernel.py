#!/usr/bin/env python3

import os
import sys
import re
from jinja2 import Environment, FileSystemLoader
from yoshi.util import exec_command

SH_FILE="./test/remove_old_kernel.sh"

def get_pkg_list():
    '''
    list packages which names are linux-(image|headers)
    '''
    ret,out,_err= exec_command("dpkg -l",'utf-8')
    if ret!=0:
        raise Exception("exec dpkg failed.")

    lines = out.split('\n')
    re1 = re.compile(r'linux-(image|headers)-([^ ]+)')
    pkgs =[]
    for line in lines:
        cols = re.split(' +',line)
        if len(cols)<4:
            continue
        name=cols[1]
        m=re1.match(name)
        if not m:
            continue
        ver = m.groups()[1]
        pkgs.append({"name":name,"ver":ver})
    return pkgs

def get_cur_ver():
    _ret,out,_err= exec_command("uname -r",'utf-8')
    m = re.search(r'[\d\.\-]+',out.strip())
    if m:
        cur_ver=m.group()
        if cur_ver[-1]=='-':
            cur_ver=cur_ver[:-1]
        print("current version:[{}]".format(cur_ver))
        return cur_ver
    else:
        print("can't get current version")
        return None

def is_cur_pkg(cur_ver,pkg_name):
    if re.search(cur_ver,pkg_name):
        return True
    if not re.search(r'\-[\d\.]+\-',pkg_name):
        #print("{} is cur_ver".format(pkg_name))
        return True
    return False

def write_script(pkgs):
    env = Environment(loader=FileSystemLoader('./templates', encoding='utf8'))
    tmpl = env.get_template('remove_old_kernel.tmpl')
    script = tmpl.render({'pkgs':pkgs,})
    with open(SH_FILE,mode='w') as f:
        f.write(str(script))
    os.chmod(SH_FILE,0o755)
    
if __name__ == '__main__':
    cur_ver=get_cur_ver()
    if cur_ver is None:
        sys.exit()

    pkgs = get_pkg_list()
    #print(pkgs)
    
    pkgs_kept = []
    pkgs_del = []
    for pkg in pkgs:
        if is_cur_pkg(cur_ver,pkg['name']):
            pkgs_kept.append(pkg["name"])
        else:
            pkgs_del.append(pkg["name"])

    pkgs_kept.sort()
    pkgs_del.sort()
    print("=== these packages are kept ===")
    for pkg in pkgs_kept:
        print (pkg)
    print("=== these packages are removed ===")
    for pkg in pkgs_del:
        print (pkg)

    if len(pkgs_del) == 0:
        print("no packages are removed.")
        sys.exit()

    write_script(pkgs_del)
    print("run {} to remove old kernel.".format(SH_FILE))

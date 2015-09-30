# coding=utf-8
__author__ = 'kk'

import subprocess
import time
import threading
import os

def rrr():
        print "hello world"
        global t        #Notice: use global variable!
        # pro = subprocess.Popen("python D:\\PyProjects\\sspider\\robot\\robotCTR.py", stdout=subprocess.PIPE,shell = True)

        os.system("python D:\\PyProjects\\sspider\\robot\\robotCTR.py")
        t = threading.Timer(30.0, rrr)
        t.start()



if __name__ == '__main__':
    os.system("python D:\\PyProjects\\sspider\\robot\\robotCTR.py")
    t = threading.Timer(30.0, rrr)
    t.start()


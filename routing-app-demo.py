#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#About: a routing application demo script
#

import sys
import getopt
import numpy as np
from datetime import datetime
from socket import *

REMOTE_HOST = '127.0.0.1'
LTE_PORT = 60000
WIFI_PORT = 60001
FG_PORT = 60002

bufsize = 8096 # Modify to suit your needs

#===========================================
def main():
#===========================================
    opts, argv = getopt.getopt(sys.argv[1:],'h',['help'])	
    print 'commandline parameters:'
    print 'argv:', argv
    print 'opts:', opts
    for o in opts:
    	if o in ("-h", "--help"):
	    helpInfo()

    robotControlSocket = socket(AF_INET, SOCK_DGRAM)
    robotControlSocket.bind((REMOTE_HOST, LTE_PORT))
    while True:
        data, addr = robotControlSocket.recvfrom(bufsize)
        print 'receive', len(data), 'bytes from', addr, ':', data





#===========================================
def bubbleSort(dataIndex, memory):
#===========================================
    print 'a function'


#===========================================
def helpInfo():
#===========================================
    print 'input argument error, please input the side lengths of 2 triangles'

if __name__ == '__main__':
    main()



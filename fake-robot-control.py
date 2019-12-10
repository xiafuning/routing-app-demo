#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# About: a fake script to simulate the behaviour of a robot control program
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

#===========================================
def main():
#===========================================
    opts, argv = getopt.getopt(sys.argv[1:],'hlwf',['help', 'lte', 'wifi', 'fiveg'])	
    print 'commandline parameters:'
    print 'argv:', argv
    print 'opts:', opts
    for o in opts:
    	if o in ("-h", "--help"):
	    helpInfo()
            exit()
    	if o in ("-l", "--lte"):
            exit()
	if o in ("-w", "--wifi"):
            exit()
	if o in ("-f", "--fiveg"):
            exit()



	




    robotControlSocket = socket(AF_INET, SOCK_DGRAM)
    data = 'a message'
    numBytesTx = robotControlSocket.sendto(data, (REMOTE_HOST, 60000))
    print 'send', numBytesTx, 'bytes'
#===========================================
def bubbleSort(dataIndex, memory):
#===========================================
    print 'a function'


#===========================================
def helpInfo():
#===========================================
    print 'usage:'

if __name__ == '__main__':
    main()



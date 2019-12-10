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
import fcntl, os
import errno
from time import sleep

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
    for name, value in opts:
        if name in ("-h", "--help"):
	    helpInfo()
            exit()

    lteSocket = socket(AF_INET, SOCK_DGRAM)
    lteSocket.bind((REMOTE_HOST, LTE_PORT))
    lteSocket.setblocking(False)

    wifiSocket = socket(AF_INET, SOCK_DGRAM)
    wifiSocket.bind((REMOTE_HOST, WIFI_PORT))
    wifiSocket.setblocking(False)

    fgSocket = socket(AF_INET, SOCK_DGRAM)
    fgSocket.bind((REMOTE_HOST, FG_PORT))
    fgSocket.setblocking(False)

    while True:
        # try to receive from lte socket
        try:
            data, addr = lteSocket.recvfrom(bufsize)
        except error, e:
            err = e.args[0]
            if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
                pass
            else:
                # a "real" error occurred
                print e
                sys.exit(1)
        else:
            print 'receive', len(data), 'bytes from', addr, ':', data

        # try to receive from wifi socket
        try:
            data, addr = wifiSocket.recvfrom(bufsize)
        except error, e:
            err = e.args[0]
            if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
                pass
            else:
                # a "real" error occurred
                print e
                sys.exit(1)
        else:
            print 'receive', len(data), 'bytes from', addr, ':', data

        # try to receive from 5g socket
        try:
            data, addr = fgSocket.recvfrom(bufsize)
        except error, e:
            err = e.args[0]
            if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
                pass
            else:
                # a "real" error occurred
                print e
                sys.exit(1)
        else:
            print 'receive', len(data), 'bytes from', addr, ':', data



#===========================================
def forward(rat):
#===========================================
    # TODO: implement forwarding functionality
    pass


#===========================================
def helpInfo():
#===========================================
    print 'Usage:'

if __name__ == '__main__':
    main()



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

NUM_PKTS = 500

#===========================================
def main():
#===========================================
    opts, argv = getopt.getopt(sys.argv[1:],'-h-l-w-f',['help', 'lte', 'wifi', 'fiveg'])
    print 'commandline parameters:'
    print 'argv:', argv
    print 'opts:', opts

    if len(opts) == 0:
        helpInfo()
        exit()
    for name, value in opts:
        if name in ("-h", "--help"):
	    helpInfo()
            exit()
        if name in ("-l", "--lte"):
            send('lte')
            exit()
        if name in ("-w", "--wifi"):
            send('wifi')
            exit()
        if name in ("-f", "--fiveg"):
            send('5g')
            exit()
    helpInfo()
    exit()


#===========================================
def send(rat):
#===========================================
    robotControlSocket = socket(AF_INET, SOCK_DGRAM)
    if rat == 'lte':
        for seq in range(NUM_PKTS):
            data = 'lte' + str(seq) + 'message'
            numBytesTx = robotControlSocket.sendto(data, (REMOTE_HOST, LTE_PORT))
    elif rat == 'wifi':
        for seq in range(NUM_PKTS):
            data = 'wifi' + str(seq) + 'message'
            numBytesTx = robotControlSocket.sendto(data, (REMOTE_HOST, WIFI_PORT))
    elif rat == '5g':
        for seq in range(NUM_PKTS):
            data = '5g' + str(seq) + 'message'
            numBytesTx = robotControlSocket.sendto(data, (REMOTE_HOST, FG_PORT))


#===========================================
def helpInfo():
#===========================================
    print 'Usage: [ -l --lte ] [-w --wifi] [-f --fiveg]'

if __name__ == '__main__':
    main()



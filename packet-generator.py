#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# About: a packet generator to simulate the behaviour of BS/TS
#

import sys
import getopt
import numpy as np
from datetime import datetime
from socket import *

REMOTE_HOST = '127.0.0.1'
BUFSIZE = 8096
NUM_PKTS = 10

#===========================================
def main():
#===========================================
    opts, argv = getopt.getopt(sys.argv[1:],'-h-b-t',['help', 'base', 'terminal'])
    print 'commandline parameters:'
    print 'argv:', argv
    print 'opts:',  opts
    if len(opts) == 0:
        helpInfo()
        exit()
    for name, value in opts:
        if name in ("-h", "--help"):
	    helpInfo()
            exit()
        if name in ("-b", "--base"):
            generator('base')
            exit()
        if name in ("-t", "--terminal"):
            generator('terminal')
            exit()


#===========================================
def generator(station):
#===========================================
    print 'generator running as', station, 'station'
    if station == 'base':
        txPort = 4000
        rxPort = 8000
    elif station == 'terminal':
        txPort = 3000
        rxPort = 9000

    txSocket = socket(AF_INET, SOCK_DGRAM)
    for seq in range(NUM_PKTS):
        data = 'message' + str(seq)
        numBytesTx = txSocket.sendto(data, (REMOTE_HOST, txPort))
 
'''
        for seq in range(NUM_PKTS):
            data = 'lte' + str(seq) + 'message'`:w

            numBytesTx = robotControlSocket.sendto(data, (REMOTE_HOST, LTE_PORT))
    elif rat == 'wifi':
        for seq in range(NUM_PKTS):
            data = 'wifi' + str(seq) + 'message'
            numBytesTx = robotControlSocket.sendto(data, (REMOTE_HOST, WIFI_PORT))
    elif rat == '5g':
        for seq in range(NUM_PKTS):
            data = '5g' + str(seq) + 'message'
            numBytesTx = robotControlSocket.sendto(data, (REMOTE_HOST, FG_PORT))
'''

#===========================================
def helpInfo():
#===========================================
    print 'Usage: [-h --help] [-b --base] [-t --terminal]'

if __name__ == '__main__':
    main()


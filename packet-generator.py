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
import threading
import random

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
            station('base')
            exit()
        if name in ("-t", "--terminal"):
            station('terminal')
            exit()


#===========================================
def station(station):
#===========================================
    print 'running as', station, 'station'
    if station == 'base':
        txPort = 4000
        rxPort = 8000
        decisionPort = 6666
    elif station == 'terminal':
        txPort = 3000
        rxPort = 9000
        decisionPort = 7777

    # create rx thread
    rxThread = threading.Thread(target=rxLoop, args=(station, rxPort, ), name='rxThread')
    rxThread.setDaemon(True)
    rxThread.start()

    # send some packets
    txSocket = socket(AF_INET, SOCK_DGRAM)
    txSocket.sendto('wifi', (REMOTE_HOST, decisionPort))
    '''
    for seq in range(NUM_PKTS):
        data = 'message' + str(seq)
        numBytesTx = txSocket.sendto(data, (REMOTE_HOST, txPort))
    '''
    seq = 0
    rat = ['lte', 'wifi', '5g']
    while True:
        try:
            data = 'message' + str(seq)
            numBytesTx = txSocket.sendto(data, (REMOTE_HOST, txPort))
            seq = seq + 1
            if seq % 100 == 0:
                txSocket.sendto(rat[random.randint(0,2)], (REMOTE_HOST, decisionPort))
        except KeyboardInterrupt:
            print "Sending kill to threads..."
            exit()

#===========================================
def rxLoop(devType, rxPort):
#===========================================
    rxSocket = socket(AF_INET, SOCK_DGRAM)
    rxSocket.bind((REMOTE_HOST, rxPort))
    #rxSocket.setblocking(False)
    while True:
        data, addr = rxSocket.recvfrom(BUFSIZE)
        print devType, 'station receive', len(data), 'bytes from', addr, ':', data


#===========================================
def helpInfo():
#===========================================
    print 'Usage: [-h --help] [-b --base] [-t --terminal]'

if __name__ == '__main__':
    main()


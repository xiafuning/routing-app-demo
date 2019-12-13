#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# About: testbench for the routing application demo
#

import sys
import getopt
import numpy as np
from datetime import datetime
from socket import *
import thread
import threading
import time
import fcntl, os
import errno

#REMOTE_HOST = '127.0.0.1'
REMOTE_HOST = gethostname()
NUM_PKTS = 5
BUFSIZE = 8096
TEST_MODE = False

#===========================================
def main():
#===========================================
    opts, argv = getopt.getopt(sys.argv[1:],'-h-d-u-m',['help', 'downlink', 'uplink', 'mix'])
    print 'commandline parameters:'
    print 'argv:', argv
    print 'opts:', opts
    if len(opts) == 0:
        helpInfo()
        exit()
    for name, value in opts:
        if name in ('h', '--help'):
	    helpInfo()
            exit()
        if name in ('-d', '--downlink'):
            bsThread = threading.Thread(target=station, args=(('BS', True, )), name='bsThread')
            tsThread = threading.Thread(target=station, args=(('TS', False, )), name='tsThread')
            bsThread.start()
            tsThread.start()
        if name in ('-u', '--uplink'):
            bsThread = threading.Thread(target=station, args=(('BS', False, )), name='bsThread')
            tsThread = threading.Thread(target=station, args=(('TS', True, )), name='tsThread')
            bsThread.start()
            tsThread.start()
        if name in ('-m', '--mix'):
            bsThread = threading.Thread(target=station, args=(('BS', True, )), name='bsThread')
            tsThread = threading.Thread(target=station, args=(('TS', True, )), name='tsThread')
            bsThread.start()
            tsThread.start()
    while True:
        pass

#===========================================
def station(devType, sendEnable):
#===========================================
    # socket init
    if devType == 'BS':
        print 'start BS APP with sendEnable =', sendEnable
        rxPort = 8000
        if TEST_MODE == True:
            txPort = 9000
        else:
            txPort = 4000
        decisionPort = 12321
    elif devType == 'TS':
        print 'start TS APP with sendEnable =', sendEnable
        rxPort = 9000
        if TEST_MODE == True:
            txPort = 8000
        else:
            txPort = 3000
        decisionPort = 23432
 
    # start rx thread
    thread.start_new_thread(rxLoop, (devType, rxPort, ))

    if sendEnable == True:
        txSocket = socket(AF_INET, SOCK_DGRAM)
        decision = 'lte'
        txSocket.sendto(decision, (REMOTE_HOST, decisionPort))
        sendData(decision, txPort)
        
        decision = 'wifi'
        txSocket.sendto(decision, (REMOTE_HOST, decisionPort))
        sendData(decision, txPort)
       
        decision = '5g'
        txSocket.sendto(decision, (REMOTE_HOST, decisionPort))
        sendData(decision, txPort)
    
    while True:
        pass


#===========================================
def rxLoop(devType, port):
#===========================================
    rxSocket = socket(AF_INET, SOCK_DGRAM)
    rxSocket.bind((REMOTE_HOST, port))
    rxSocket.setblocking(False)
    while True:
        try:
            data, addr = rxSocket.recvfrom(BUFSIZE)
        except error, e:
            err = e.args[0]
            if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
                pass
            else:
                # a "real" error occurred
                print e
                sys.exit(1)
        else:
            print devType, 'receive', len(data), 'bytes from', addr, ':', data


#===========================================
def sendData(rat, port):
#===========================================
    txSocket = socket(AF_INET, SOCK_DGRAM)
    if rat == 'lte':
        for seq in range(NUM_PKTS):
            data = 'lte' + str(seq) + 'message'
            numBytesTx = txSocket.sendto(data, (REMOTE_HOST, port))
    elif rat == 'wifi':
        for seq in range(NUM_PKTS):
            data = 'wifi' + str(seq) + 'message'
            numBytesTx = txSocket.sendto(data, (REMOTE_HOST, port))
    elif rat == '5g':
        for seq in range(NUM_PKTS):
            data = '5g' + str(seq) + 'message'
            numBytesTx = txSocket.sendto(data, (REMOTE_HOST, port))


#===========================================
def helpInfo():
#===========================================
    print 'Usage: [-h --help] [-d --downlink] [-u --uplink] [-m --mix]'

if __name__ == '__main__':
    main()

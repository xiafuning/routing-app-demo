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
import time

REMOTE_HOST = '127.0.0.1'
NUM_PKTS = 5

#===========================================
def main():
#===========================================
    opts, argv = getopt.getopt(sys.argv[1:],'-h-d-u-m',['help', 'downlink', 'uplink', 'mix'])
    print 'commandline parameters:'
    print 'argv:', argv
    print 'opts:', opts

    for name, value in opts:
        if name in ("-h", "--help"):
	    helpInfo()
            exit()
        if name in ("-d", "--downlink"):
            print 'enter d'
            thread.start_new_thread(bs, (True, ))
            thread.start_new_thread(ts, (False, ))
        if name in ("-u", "--uplink"):
	    thread.start_new_thread(bs, (False, ))
            thread.start_new_thread(ts, (True, ))
        if name in ("-m", "--mix"):
            thread.start_new_thread(bs, (True, ))
            thread.start_new_thread(ts, (True, ))

    while True:
        pass


#===========================================
def bs(sendEnable):
#===========================================
    # socket init
    print 'start bs with sendEnable =', sendEnable
    bsRxPort = 8000
    bsTxPort = 4000
    bsDecisionPort = 6000
    
    bsTxSocket = socket(AF_INET, SOCK_DGRAM)
    bsRxSocket = socket(AF_INET, SOCK_DGRAM)
    bsRxSocket.bind((REMOTE_HOST, bsRxPort))

    decision = 'lte'
    bsTxSocket.sendto(decision, (REMOTE_HOST, bsDecisionPort))
    for seq in range(NUM_PKTS):
        data = decision + str(seq) + 'message'
        bsTxSocket.sendto(data, (REMOTE_HOST, bsTxPort))

    time.sleep(1)
    print 'bs end'

#===========================================
def ts(sendEnable):
#===========================================
    # socket init
    print 'start ts with sendEnable =', sendEnable
    tsSocket = socket(AF_INET, SOCK_DGRAM)
    tsDecisionSocket = socket(AF_INET, SOCK_DGRAM)
    time.sleep(1)
    print 'ts end'




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



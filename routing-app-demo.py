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
import time
import threading

# import TestMan modules
from Server import UDP_Server
from signalslot import Slot

REMOTE_HOST = '127.0.0.1'
BUFSIZE = 16000 # Modify to suit your needs

# set default rat
decision = 'lte'


#===========================================
def main():
#===========================================
    opts, argv = getopt.getopt(sys.argv[1:],'-h-b-t',['help', 'base', 'terminal', 'testman'])	
    print 'commandline parameters:'
    print 'argv:', argv
    print 'opts:', opts
    if len(opts) == 0:
        helpInfo()
        exit()
    
    # cmd arguments initialization
    devType = 'BS'
    testmanEnabled = False
    
    for name, value in opts:
        if name in ('-h', '--help'):
	    helpInfo()
            exit()
        elif name in ('-b', '--base'):
            devType = 'BS'
        elif name in ('-t', '--terminal'):
            devType = 'TS'
        elif name in ('--testman'):
            testmanEnabled = True
            print 'testman enabled'
        else:
            helpInfo()
            exit()
    
    # run routing function
    routing(devType, testmanEnabled)


#===========================================
def routing(devType, testmanEnabled):
#===========================================
    if devType == 'BS':
        print 'start BS routing app'
        listenDataPort = 4000
        listenDecisionPort = 6666
        ltePortTx = 8990
        wifiPortTx = 8991
        fgPortTx = 8992
        ltePortRx = 7990
        wifiPortRX = 7991
        fgPortRx = 7992
        rxFwdPort = 8000
    elif devType == 'TS':
        print 'start TS routing app'
        listenDataPort = 3000
        listenDecisionPort = 7777
        ltePortTx = 7990
        wifiPortTx = 7991
        fgPortTx = 7992
        ltePortRx = 8990
        wifiPortRX = 8991
        fgPortRx = 8992
        rxFwdPort = 9000
 
    # set default rat
    global decision

    '''
    # create uplink thread
    ulThread = threading.Thread(target=ulForward, args=(ltePortRx, wifiPortRX, fgPortRx, rxFwdPort, ), name='ulThread')
    ulThread.setDaemon(True)
    ulThread.start()
    '''
    # create lte uplink thread
    ulLteThread = threading.Thread(target=ulForward, args=(ltePortRx, rxFwdPort, ), name='ulLteThread')
    ulLteThread.setDaemon(True)
    ulLteThread.start()

    # create wifi uplink thread
    ulWifiThread = threading.Thread(target=ulForward, args=(wifiPortRX, rxFwdPort, ), name='ulWifiThread')
    ulWifiThread.setDaemon(True)
    ulWifiThread.start()

    # create 5g uplink thread
    ul5gThread = threading.Thread(target=ulForward, args=(fgPortRx, rxFwdPort, ), name='ul5gThread')
    ul5gThread.setDaemon(True)
    ul5gThread.start()

    # create downlink data thread
    dlDataThread = threading.Thread(target=dlDataForward, args=(devType, listenDataPort, ltePortTx, wifiPortTx, fgPortTx, ), name='dlDataThread')
    dlDataThread.setDaemon(True)
    dlDataThread.start()

    # listen for decision
    if testmanEnabled == False:
        # use UDP socket
        listenDecisionSocket = socket(AF_INET, SOCK_DGRAM)
        listenDecisionSocket.bind((REMOTE_HOST, listenDecisionPort))
        while True:
            try:
                data, addr = listenDecisionSocket.recvfrom(BUFSIZE)
                decision = data
            except KeyboardInterrupt:
                print "Sending kill to threads..."
                exit()
    elif testmanEnabled == True:
        # use TestMan
        S = UDP_Server(ip="224.5.6.7", port=listenDecisionPort, ttl=1, type_=2, id_=1)
        print("Server started..")
        # Connect to packet receive callback handler.
        S.packet_received.connect(Slot(testmanCallback))
        print("Receive-Handler established")
        while True:
            try:
                time.sleep(1000)
            except KeyboardInterrupt:
                print "Sending kill to threads..."
                exit()

#===========================================
def testmanCallback(packet):
#===========================================
    print("\n=== Received packet ==============")
    # print type(packet.Command), packet.Command
    global decision
    decision = str(packet.Command)
    print type(decision), decision


#===========================================
def ulForward(PortRx, rxFwdPort):
#===========================================
    rxSocket = socket(AF_INET, SOCK_DGRAM)
    rxSocket.bind((REMOTE_HOST, PortRx))

    rxFwdSocket = socket(AF_INET, SOCK_DGRAM)

    while True:
        data, addr = rxSocket.recvfrom(BUFSIZE)
        print 'forward', len(data), 'bytes to', (REMOTE_HOST, rxFwdPort)
        rxFwdSocket.sendto(data, (REMOTE_HOST, rxFwdPort))

'''
#===========================================
def ulForward(ltePortRx, wifiPortRX, fgPortRx, rxFwdPort):
#===========================================
    lteSocket = socket(AF_INET, SOCK_DGRAM)
    lteSocket.bind((REMOTE_HOST, ltePortRx))
    lteSocket.setblocking(False)

    wifiSocket = socket(AF_INET, SOCK_DGRAM)
    wifiSocket.bind((REMOTE_HOST, wifiPortRX))
    wifiSocket.setblocking(False)

    fgSocket = socket(AF_INET, SOCK_DGRAM)
    fgSocket.bind((REMOTE_HOST, fgPortRx))
    fgSocket.setblocking(False)

    rxFwdSocket = socket(AF_INET, SOCK_DGRAM)

    while True:
        # try to receive from lte socket
        try:
            data, addr = lteSocket.recvfrom(BUFSIZE)
        except error, e:
            err = e.args[0]
            if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
                pass
            else:
                # a "real" error occurred
                print e
                sys.exit(1)
        else:
            print 'forward', len(data), 'bytes to', (REMOTE_HOST, rxFwdPort)
            rxFwdSocket.sendto(data, (REMOTE_HOST, rxFwdPort))

        # try to receive from wifi socket
        try:
            data, addr = wifiSocket.recvfrom(BUFSIZE)
        except error, e:
            err = e.args[0]
            if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
                pass
            else:
                # a "real" error occurred
                print e
                sys.exit(1)
        else:
            print 'forward', len(data), 'bytes to', (REMOTE_HOST, rxFwdPort)
            rxFwdSocket.sendto(data, (REMOTE_HOST, rxFwdPort))

        # try to receive from 5g socket
        try:
            data, addr = fgSocket.recvfrom(BUFSIZE)
        except error, e:
            err = e.args[0]
            if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
                pass
            else:
                # a "real" error occurred
                print e
                sys.exit(1)
        else:
            print 'forward', len(data), 'bytes to', (REMOTE_HOST, rxFwdPort)
            rxFwdSocket.sendto(data, (REMOTE_HOST, rxFwdPort))
        time.sleep(0.001)
'''

#===========================================
def dlDataForward(devType, listenDataPort, ltePortTx, wifiPortTx, fgPortTx):
#===========================================
    global decision
    listenDataSocket = socket(AF_INET, SOCK_DGRAM)
    listenDataSocket.bind((REMOTE_HOST, listenDataPort))

    while True:
        data, addr = listenDataSocket.recvfrom(BUFSIZE)
        print devType, 'forward a packet using', decision
        sendData(data, decision, ltePortTx, wifiPortTx, fgPortTx)


#===========================================
def sendData(data, rat, ltePortTx, wifiPortTx, fgPortTx):
#===========================================
    txSocket = socket(AF_INET, SOCK_DGRAM)
    if rat == 'lte':
        numBytesTx = txSocket.sendto(data, (REMOTE_HOST, ltePortTx))
    elif rat == 'wifi':
        numBytesTx = txSocket.sendto(data, (REMOTE_HOST, wifiPortTx))
    elif rat == '5g':
        numBytesTx = txSocket.sendto(data, (REMOTE_HOST, fgPortTx))
    else:
        print 'Error: RAT type unknown!'

#===========================================
def helpInfo():
#===========================================
    print 'Usage: [-h --help] [-b --base] [-t --terminal]'

if __name__ == '__main__':
    main()



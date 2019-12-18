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
BS_IP = ''
TS_IP = ''
FG_BS_IP = ''
FG_TS_IP = ''
BUFSIZE = 16000 # Modify to suit your needs

# set default rat
decision = 'lte'


#===========================================
def main():
#===========================================
    opts, argv = getopt.getopt(sys.argv[1:],'-h-b-t',['help', 'base', 'terminal', 'testman', 'testmode'])
    print 'commandline parameters:'
    print 'argv:', argv
    print 'opts:', opts
    if len(opts) == 0:
        helpInfo()
        exit()
    addressTable = {'BS':{'ipAddr':BS_IP, 'ip5gAddr':FG_BS_IP, 'listenDataPort':59998, 'listenDecisionPort':6666, 'ltePortTx':60000, 'wifiPortTx':60001, 'fgPortTx':60002, 'ltePortRx':60010, 'wifiPortRX':60011, 'fgPortRx':60012, 'rxFwdPort':59999}, 'TS':{'ipAddr':TS_IP, 'ip5gAddr':FG_TS_IP, 'listenDataPort':59998, 'listenDecisionPort':7777, 'ltePortTx':60010, 'wifiPortTx':60011, 'fgPortTx':60012, 'ltePortRx':60000, 'wifiPortRX':60001, 'fgPortRx':60002, 'rxFwdPort':59999}}
    # cmd arguments initialization
    devType = 'BS'
    testmanEnabled = False
    testModeEnabled = False

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
        elif name in ('--testmode'):
            testModeEnabled = True
        else:
            helpInfo()
            exit()
    
    # run routing function
    routing(devType, testmanEnabled, testModeEnabled, addressTable[devType])


#===========================================
def routing(devType, testmanEnabled, testModeEnabled, addressTable):
#===========================================
    if devType == 'BS':
        if testModeEnabled == True:
            print 'start BS routing app in test mode'
            ipAddr = REMOTE_HOST
            ip5gAddr = REMOTE_HOST
            listenDataPort = 4000
            listenDecisionPort = 6666
            ltePortTx = 8990
            wifiPortTx = 8991
            fgPortTx = 8992
            ltePortRx = 7990
            wifiPortRX = 7991
            fgPortRx = 7992
            rxFwdPort = 8000
        else:
            print 'start BS routing app in real mode'
            ipAddr = addressTable['ipAddr']
            ip5gAddr = addressTable['ip5gAddr']
            listenDataPort = addressTable['listenDataPort']
            listenDecisionPort = addressTable['listenDecisionPort']
            ltePortTx = addressTable['ltePortTx']
            wifiPortTx = addressTable['wifiPortTx']
            fgPortTx = addressTable['fgPortTx']
            ltePortRx = addressTable['ltePortRx']
            wifiPortRX = addressTable['wifiPortRX']
            fgPortRx = addressTable['fgPortRx']
            rxFwdPort = addressTable['rxFwdPort']
            #print addressTable
            #exit()
    elif devType == 'TS':
        if testModeEnabled == True:
            print 'start TS routing app in test mode'
            ipAddr = REMOTE_HOST
            ip5gAddr = REMOTE_HOST
            listenDataPort = 3000
            listenDecisionPort = 7777
            ltePortTx = 7990
            wifiPortTx = 7991
            fgPortTx = 7992
            ltePortRx = 8990
            wifiPortRX = 8991
            fgPortRx = 8992
            rxFwdPort = 9000
        else:
            print 'start TS routing app in real mode'
            ipAddr = addressTable['ipAddr']
            ip5gAddr = addressTable['ip5gAddr']
            listenDataPort = addressTable['listenDataPort']
            listenDecisionPort = addressTable['listenDecisionPort']
            ltePortTx = addressTable['ltePortTx']
            wifiPortTx = addressTable['wifiPortTx']
            fgPortTx = addressTable['fgPortTx']
            ltePortRx = addressTable['ltePortRx']
            wifiPortRX = addressTable['wifiPortRX']
            fgPortRx = addressTable['fgPortRx']
            rxFwdPort = addressTable['rxFwdPort']
            #print addressTable
            #exit()

    # set default rat
    global decision

    # create lte uplink thread
    ulLteThread = threading.Thread(target=ulForward, args=(ipAddr, ltePortRx, rxFwdPort, ), name='ulLteThread')
    ulLteThread.setDaemon(True)
    ulLteThread.start()

    # create wifi uplink thread
    ulWifiThread = threading.Thread(target=ulForward, args=(ipAddr, wifiPortRX, rxFwdPort, ), name='ulWifiThread')
    ulWifiThread.setDaemon(True)
    ulWifiThread.start()

    # create 5g uplink thread
    ul5gThread = threading.Thread(target=ulForward, args=(ip5gAddr, fgPortRx, rxFwdPort, ), name='ul5gThread')
    ul5gThread.setDaemon(True)
    ul5gThread.start()

    # create downlink data thread
    dlDataThread = threading.Thread(target=dlDataForward, args=(devType, listenDataPort, ipAddr, ip5gAddr, ltePortTx, wifiPortTx, fgPortTx, ), name='dlDataThread')
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
                print 'Sending kill to threads...'
                exit()
    elif testmanEnabled == True:
        # use TestMan
        S = UDP_Server(ip='224.5.6.7', port=listenDecisionPort, ttl=1, type_=2, id_=1)
        print 'Server started..'
        # Connect to packet receive callback handler.
        S.packet_received.connect(Slot(testmanCallback))
        print 'Receive-Handler established'
        while True:
            try:
                time.sleep(1000)
            except KeyboardInterrupt:
                print 'Sending kill to threads...'
                exit()


#===========================================
def testmanCallback(packet):
#===========================================
    print '\n=== Received packet =============='
    # print type(packet.Command), packet.Command
    global decision
    decision = str(packet.Command)
    print type(decision), decision


#===========================================
def ulForward(ipRx, PortRx, rxFwdPort):
#===========================================
    rxSocket = socket(AF_INET, SOCK_DGRAM)
    rxSocket.bind((ipRx, PortRx))

    rxFwdSocket = socket(AF_INET, SOCK_DGRAM)

    while True:
        data, addr = rxSocket.recvfrom(BUFSIZE)
        print 'forward', len(data), 'bytes to', (REMOTE_HOST, rxFwdPort)
        rxFwdSocket.sendto(data, (REMOTE_HOST, rxFwdPort))


#===========================================
def dlDataForward(devType, listenDataPort, ipTx, ip5gTx, ltePortTx, wifiPortTx, fgPortTx):
#===========================================
    global decision
    listenDataSocket = socket(AF_INET, SOCK_DGRAM)
    listenDataSocket.bind((REMOTE_HOST, listenDataPort))

    while True:
        data, addr = listenDataSocket.recvfrom(BUFSIZE)
        print devType, 'forward a packet using', decision
        sendData(data, decision,ipTx, ip5gTx, ltePortTx, wifiPortTx, fgPortTx)


#===========================================
def sendData(data, rat, ipTx, ip5gTx, ltePortTx, wifiPortTx, fgPortTx):
#===========================================
    txSocket = socket(AF_INET, SOCK_DGRAM)
    if rat == 'lte':
        numBytesTx = txSocket.sendto(data, (ipTx, ltePortTx))
    elif rat == 'wifi':
        numBytesTx = txSocket.sendto(data, (ipTx, wifiPortTx))
    elif rat == '5g':
        numBytesTx = txSocket.sendto(data, (ip5gTx, fgPortTx))
    else:
        print 'Error: RAT type unknown!'
        exit()


#===========================================
def helpInfo():
#===========================================
    print 'Usage: [-h --help] [-b --base] [-t --terminal] [--testman] [--testmode]'

if __name__ == '__main__':
    main()

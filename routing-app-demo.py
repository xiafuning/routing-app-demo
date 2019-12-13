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

REMOTE_HOST = '127.0.0.1'
BUFSIZE = 8096 # Modify to suit your needs

#===========================================
def main():
#===========================================
    opts, argv = getopt.getopt(sys.argv[1:],'-h-b-t',['help', 'base', 'terminal'])	
    print 'commandline parameters:'
    print 'argv:', argv
    print 'opts:', opts
    if len(opts) == 0:
        helpInfo()
        exit()
    for name, value in opts:
        if name in ('-h', '--help'):
	    helpInfo()
            exit()
        if name in ('-b', '--base'):
            routing('BS')
        if name in ('-t', '--terminal'):
            routing('TS')


#===========================================
def routing(devType):
#===========================================
    if devType == 'BS':
        print 'start BS routing app'
        listenDataPort = 4000
        listenDecisionPort = 12321
        ltePort = 8990
        wifiPort = 8991
        fgPort = 8992
        rxFwdPort = 8000
    elif devType == 'TS':
        print 'start TS routing app'
        listenDataPort = 3000
        listenDecisionPort = 23432
        ltePort = 7990
        wifiPort = 7991
        fgPort = 7992
        rxFwdPort = 9000

    ulThread = threading.Thread(target=ulForward, args=(ltePort, wifiPort, fgPort, rxFwdPort, ))

    # set default rat
    decision = 'lte'

    listenDataSocket = socket(AF_INET, SOCK_DGRAM)
    listenDataSocket.bind((REMOTE_HOST, listenDataPort))
    listenDataSocket.setblocking(False)

    listenDecisionSocket = socket(AF_INET, SOCK_DGRAM)
    listenDecisionSocket.bind((REMOTE_HOST, listenDecisionPort))
    listenDecisionSocket.setblocking(False)

    while True:
        # try to receive a data packet and forward it
        try:
            data, addr = listenDataSocket.recvfrom(BUFSIZE)
        except error, e:
            err = e.args[0]
            if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
                pass
            else:
                # a "real" error occurred
                print e
                sys.exit(1)
        else:
            print devType, 'forward the packet using', decision
            sendData(data, decision, ltePort, wifiPort, fgPort)

        # try to receive a decision packet
        try:
            data, addr = listenDecisionSocket.recvfrom(BUFSIZE)
        except error, e:
            err = e.args[0]
            if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
                pass
            else:
                # a "real" error occurred
                print e
                sys.exit(1)
        else:
            # update decision
            decision = data

#===========================================
def ulForward(ltePort, wifiPort, fgPort, rxFwdPort):
#===========================================
    lteSocket = socket(AF_INET, SOCK_DGRAM)
    lteSocket.bind((REMOTE_HOST, ltePort))
    lteSocket.setblocking(False)

    wifiSocket = socket(AF_INET, SOCK_DGRAM)
    wifiSocket.bind((REMOTE_HOST, wifiPort))
    wifiSocket.setblocking(False)

    fgSocket = socket(AF_INET, SOCK_DGRAM)
    fgSocket.bind((REMOTE_HOST, fgPort))
    fgSocket.setblocking(False)

    rxFwdSocket = socket(AF_INET, SOCK_DGRAM)

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
            print 'forward', len(data), 'bytes to', (REMOTE_HOST, rxFwdPort), ':', data
            rxFwdSocket.sendto(data, (REMOTE_HOST, rxFwdPort))

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
            print 'forward', len(data), 'bytes to', (REMOTE_HOST, rxFwdPort), ':', data
            rxFwdSocket.sendto(data, (REMOTE_HOST, rxFwdPort))

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
            print 'forward', len(data), 'bytes to', (REMOTE_HOST, rxFwdPort), ':', data
            rxFwdSocket.sendto(data, (REMOTE_HOST, rxFwdPort))


#===========================================
def sendData(data, rat, ltePort, wifiPort, fgPort):
#===========================================
    txSocket = socket(AF_INET, SOCK_DGRAM)
    if rat == 'lte':
        numBytesTx = txSocket.sendto(data, (REMOTE_HOST, ltePort))
    elif rat == 'wifi':
        numBytesTx = txSocket.sendto(data, (REMOTE_HOST, wifiPort))
    elif rat == '5g':
        numBytesTx = txSocket.sendto(data, (REMOTE_HOST, fgPort))


#===========================================
def helpInfo():
#===========================================
    print 'Usage: [-h --help] [-b --base] [-t --terminal]'

if __name__ == '__main__':
    main()



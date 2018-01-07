#!/usr/bin/env python3
#
# Filename: nmapExampleCode.py
#
# Not from the book. This is sample code that was used to get a quick feel for the python-nmap module.
# It is included here simply for reference. It is hard coded to "localhost' and ports '25-631'
# NOTE: This is a modified version of the nmap code example from pages 40 through 41.
#
# Author: Daniel Raphael
#
# ---------------------------------------------------------------------------------------------------------------------
#

import nmap

nm = nmap.PortScanner()
nm.scan('localhost', '25-631')
print('nmap commandline: {}'.format(nm.command_line()))
print('nmap scaninfo: {}'.format(nm.scaninfo()))
print('nmap all hosts: {}'.format(nm.all_hosts()))
hosts = nm.all_hosts()
for host in hosts:
    print('nmap scan.state == {}'.format(nm[host]))
    print('nmap hostname: {}'.format(nm[host].hostname()))
    print('nmap state: {}'.format(nm[host].state()))
    print('nmap protocols: {}'.format(nm[host].all_protocols()))
    print('nmap port keys: {}\n'.format(nm[host]['tcp'].keys()))

    # This is a List Comprehension. If you are not familiar with the construct, it is a for loop that creates
    # a list from an iterable object. In this case nm[host]['tcp'].keys() is returns an iterable that contains all
    # the ports found on "host".
    keys = [key for key in nm[host]['tcp'].keys()]
    for port in keys:
        print('has tcp {}: {}'.format(port, nm[host].has_tcp(port)))
        print('get info host:{} {}'.format(port, nm[host]['tcp'][port]))
        print('get state of host:{} {}\n'.format(port, nm[host]['tcp'][port]['state']))

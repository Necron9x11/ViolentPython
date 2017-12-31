#!/usr/bin/env python3
#
# Filename: vulnscanner.py
#
# Violent Python - A Cookbook for Hackers,Forensic Analysts,Penetration Testers and Security Engineers
# Chapter 1 | Port Scanner Example - version 1
#
# NOTE: This is a modified version of the final version of the vulnerability scanner built up from pages 7 through 20.
#       The original version supplied with the book and downloaded from:
#
#       https://booksite.elsevier.com/9781597499576/?ISBN=9781597499576
#
#       and is saved here, for comparison, as vulnscanner_v2.py
#
# Original Author: TJ O'Connor
# Modified to run under Python 3.x by: Daniel Raphael
#
# This was originally coded for Python 2.x.
# Mods made to run under Python 3.6 follow. These include stylistic as well as functional code modifications.
# - var banner : Byte data returned by socket.recv().
#       Initial reference to banner updated to use the decode method:
#
#           banner.decode("utf-8")
#
#       This way all other references to "banner" receive a string object and not a byte object.
#
# - try/except :  Original code used a bare except clause. Python 3 considers this to be to generalized.
#       Updated the except clause to the more robust form:
#
#           except OSError as e:
#
#       Note that this was actually addressed in the supplied source file though not in the book itself.
#
# - var/function naming style : Original code used camel case style naming.
#       Updated to use the underscore style:
#           retBanner became ret_banner, etc.
#
# - print - Converted all Python 2.x style print statements to use the Python 3.x print() function and
#   the .format string method instead of the string concatenations originally employed.
#
#   print '[+] ' + ip + ' : ' + banner          became:     print('[+] {} : {}'.format(ip, banner))
#
# - exit() - converted all instances of "exit()" to "sys.exit()" as "exit()" is meant for the interactive
#   environment and "sys.exit()" is preferred for use in source files that will be executed from the command line.
#
# - f = open(filename, 'r') - changed this to use the more Pythonic form: with open(filename, 'rU') as f:
#
#
import socket
import os
import sys


def ret_banner(ip, port):
    try:
        socket.setdefaulttimeout(2)
        s = socket.socket()
        s.connect((ip, port))
        banner = s.recv(1024)
        return banner.decode("utf-8")       # decode the banner from byte type to a utf-8 string before passing it back.
    except OSError as e:                    # this saves us from having to do the conversion in multiple places later.
        print('[-] Error: {}'.format(e))    # Better error handling. We are just blanket catching the errors and
        return                              # reporting them, but it is better than nothing for now.


def check_vulns(banner, filename):
    # f = open(filename, 'r')
    with open(filename, 'rU') as f:  # Modified the file read to use the correct Pythonic method.
        for line in f:
            if line.strip('\n') in banner:
                print('[+] Server is vulnerable: {}'.format(banner.strip('\n')))


def main():
    if len(sys.argv) == 2:
        filename = sys.argv[1]
        if not os.path.isfile(filename):
            print('[-] {} does not exist.'.format(filename))
            sys.exit(0)  # "sys.exit()" should be used in source files. "exit()" is meant for the interactive shell.
        if not os.access(filename, os.R_OK):
            print('[-] {} access denied'.format(filename))
            sys.exit(0)  # "sys.exit()" should be used in source files. "exit()" is meant for the interactive shell.
    else:
        print('[-] Usage: {} <vuln filename>'.format(sys.argv[0]))
        sys.exit(0)     # "sys.exit()" should be used in source files. "exit()" is meant for the interactive shell.

    port_list = [21, 22, 25, 80, 110, 443]
    for x in range(145, 255):
        ip = '192.168.0.' + str(x)
        for port in port_list:
            banner = ret_banner(ip, port)
            if banner:
                print('[+] {}: {}'.format(ip, banner.strip('\n')))  # strip newline causing annoying gap in the output.
                check_vulns(banner, filename)

    print('End Run')


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
#
# Filename: portScanner.py
#
# Violent Python - A Cookbook for Hackers,Forensic Analysts,Penetration Testers and Security Engineers
# Chapter 2 | Port Scanner Portion of the Morris Work Lookalike - version 1
#
# NOTE: This is a modified version of the code from pages 31 through 41.
#
#       The original version supplied with the book can be downloaded from:
#
#       https://booksite.elsevier.com/9781597499576/?ISBN=9781597499576
#
#       and is saved here, for comparison, in the publishedCode sub-folder
#
# Original Author: TJ O'Connor
# Modified to run under Python 3.x by: Daniel Raphael
#
# ---------------------------------------------------------------------------------------------------------------------
#
# Introduces the  socket module:
#
# Introduces the threading module:
#
# Introduces the argparse module:
# The argparse module makes it easy to write user-friendly command-line interfaces. The program defines what arguments
# it requires, and argparse will figure out how to parse those out of sys.argv. The argparse module also automatically
# generates help and usage messages and issues errors when users give the program invalid arguments.
#
# https://docs.python.org/3.5/library/argparse.html?highlight=argparse#module-argparse
#
# Note that in the book there is code that checks to make sure neither option is == None and, if so, exit the program.
# This has been omitted as with argparse we can specify the "required=True" option and the module will handle this
# for us.
#
# I replaced optpares with argpares in the code as optparse has been  deprecated since v2.7:
# https://www.python.org/dev/peps/pep-0389/
#
# Uses the sys module
# This module provides access to some variables used or maintained by the interpreter and to functions that interact
#  strongly with the interpreter. It is always available.
#
# https://docs.python.org/3.5/library/sys.html?highlight=sys#module-sys
#
# ---------------------------------------------------------------------------------------------------------------------
#
# Mods made to run under Python 3.x follow. These include stylistic as well as functional code modifications.
#
# - int() : had to convert the target_port variable to an int.
#
# - encoding : had to convert the string sent to the remote server to byte encoding from utf-8:
#
#   socket_connection.send('ViolentPython\r\n') became socket_connection.send(b'ViolentPython\r\n')
#                                                                             ^
#
# - try/except :  Original code used a bare except clause. Python 3 considers this to be to generalized.
#       Updated the except clause to the more robust form:
#
#           except <exception type>  as e:
#
# - var/function naming style : Original code used camel case style naming.
#       Updated to use the underscore style:
#           retBanner became ret_banner, etc.
#
# - print : Converted all Python 2.x style print statements to use the Python 3.x print() function and
#   the .format string method instead of the string concatenations originally employed. I did this as it is
#   better performance wise and is more feature rich. For instance it does type conversion without the need to
#   call functions like str() and int() all the time.
#
#   print '[+] ' + ip + ' : ' + banner          became:     print('[+] {} : {}'.format(ip, banner))
#
# - exit() : converted all instances of "exit()" to "sys.exit()" as "exit()" is meant for the interactive
#   environment and "sys.exit()" is preferred for use in source files that will be executed from the command line.
#
# - f = open(filename, 'r') : changed this to use the more Pythonic form: with open(filename, 'rU') as f:
#
# - optparse code converted to argparse code. This is not required to run under v3.x but optparse is deprecated since
#   v2.7 and moving to argparse is in keeping with my goal of not only converting v2.x specific code to v3.x but also
#   doing my best to make the code more modern and more Pythonic by current standards.
#
#
# ---------------------------------------------------------------------------------------------------------------------
#
# Functional Changes
#
# Added code to check for Python3.x and exit if not available.

# Python3 is expected:
#
import sys
if sys.version_info[0] != 3 or sys.version_info[1] < 5:
    sys.exit('This program needs Python3.5.0+')

# print('Python version is: {}'.format(sys.version_info))


# ---------------------------------------------------------------------------------------------------------------------
#
# Initial code - p.34 - The command line options handler
#
# import argparse
#
# Note that in the book there is code that checks to make sure neither option is == None and, if so, exit the program.
# This has been omitted as with argparse we can specify the "required=True" option and the module will handle this
# for us.
#
# Also the variable assignment the book used for the options passed in omitted as the argparse.parser.args() method
# assigns all the arguments stored in +++ RRR +++ to an object whos local data stored the opts as .<switch name>.
#
# parser = argparse.ArgumentParser()
#
# parser.add_argument('-H', '--host',
#                     type=str,
#                     required=True,
#                     help='specify target host')
#
# parser.add_argument('-p', '--port',
#                     type=int,
#                     help='specify target port(s)')
#
# args = parser.parse_args()
#
# # note that now args.host holds the name of the host passed in from the cli and args.ports holds the port
#
# target_host = args.host
# target_port = args.port

# ---------------------------------------------------------------------------------------------------------------------
#
# the port connection and port scanner functions - pp.34-35
#
# from socket import *
#
#
# def scan_connection(target_host, target_port):
#     try:
#         connect_socket = socket(AF_INET, SOCK_STREAM)
#         connect_socket.connect((target_host, target_port))
#         print('[+] {}/tcp open'.format(target_port))
#
#     except OSError:
#         print('[-] {}/tcp closed'.format(target_port))
#
#
# def scan_port(target_host, target_ports):
#     try:
#         target_ip = gethostbyname(target_host)
#
#     except OSError:
#         print('[-] Cannot resolve {}: Unknown host'.format(target_host))
#         return
#
#     try:
#         target_name = gethostbyaddr(target_ip)
#         print('\n[+] Scan Results for: {}'.format(target_name[0]))
#
#     except OSError:
#         print('\n[+] Scan Results for: {}'.target_ip)
#     setdefaulttimeout(1)
#     for target_port in target_ports:
#         print('Scanning Port {}'.format(target_port))
#         scan_connection(target_host, int(target_port))

# ---------------------------------------------------------------------------------------------------------------------
#
# the banner grabbing function - pp.35-36
#
# import argparse
# import socket
# from socket import *
#
#
# def scan_connection(target_host, target_port):
#     try:
#         socket_connection = socket(AF_INET, SOCK_STREAM)
#         socket_connection.connect((target_host, target_port))
#         socket_connection.send(b'ViolentPython\r\n')                      # Had to convert this to byte. Was string.
#         results = socket_connection.recv(100)
#         print('[+] {}/tcp open'.format(target_port))
#         print('[+] {}'.format(results))
#         socket_connection.close()
#
#     except OSError:
#         print('[-] {}/tcp closed'.format(target_port))
#
#
# def scan_port(target_host, target_ports):
#     try:
#         target_ip = gethostbyname(target_host)
#     except OSError:
#         print('[-] Cannot resolve {}: Unknown Host'.format(target_host))
#         return
#
#     try:
#         target_name = gethostbyaddr(target_ip)
#         print('\n[+] Scan Results for: {}'.format(target_name[0]))
#
#     except OSError:
#         print('\n[+] Scan Results for: '.format(target_ip))
#
#     setdefaulttimeout(1)
#
#     for target_port in target_ports:
#         print('Scanning port {}'.format(target_port))
#         scan_connection(target_host, int(target_port))
#
#
# def main():
#
#     parser = argparse.ArgumentParser()
#
#     parser.add_argument('-H', '--host',
#                         type=str,
#                         required=True,
#                         help='specify target host')
#
#     parser.add_argument('-p', '--port',
#                         type=str,
#                         help='specify target ports, separated by commas')
#
#     args = parser.parse_args()
#
#     # note that now args.host holds the name of the host passed in from the cli and args.ports holds the port
#
#     target_host = args.host
#     target_port = str(args.port).split(',')
#
#     # print(target_port)
#     # sys.exit()
#
#     # target_host = "centos01"
#     # target_port = []
#     # target_port.append(22,)
#     # target_port = "22"
#
#     scan_port(target_host, target_port)
#
#
# if __name__ == '__main__':
#     main()


# ---------------------------------------------------------------------------------------------------------------------
#
# Threading code pp.37-38
#
# It was no in the book at this point but, to use threading, you much import the threading module
#
# from threading import *
#
# Following are the mods that need to be made to the scan_port() function. Code is the same as it was for Python 2.x
#
# for target_port in target_ports:
#     t = Thread(target=scan_connection)
#     t.start()
#
# Following are the mods that need be made to the scan_connection() function
#
# screen_lock = Semaphore(value=1)
#
# def scan_connection(target_host, target_port):
#     try:
#         socket_connection = socket(AF_INET, SOCK_STREAM)
#         socket_connection.connect((target_host, target_port))
#         socket_connection.send(b'ViolentPython\r\n')                      # Had to convert this to byte. Was string.
#         results = socket_connection.recv(100)
#         screen_lock.acquire()
#         print('[+] {}/tcp open'.format(target_port))
#         print('[+] {}'.format(results))
#
#     except OSError:
#         screen_lock.acquire()
#         print('[-] {}/tcp closed'.format(target_port))
#
#     finally:
#         screen_lock.release()
#         socket_connection.close()

# ---------------------------------------------------------------------------------------------------------------------
#
# Final complete port scanner code pp.38-39
#
import argparse
from socket import *
from threading import *


screen_lock = Semaphore(value=1)


def scan_connection(target_host, target_port):
    try:
        socket_connection = socket(AF_INET, SOCK_STREAM)
        socket_connection.connect((target_host, int(target_port)))          # Had to convert this to int. Was string.
        socket_connection.send(b'ViolentPython\r\n')                        # Had to convert this to byte. Was string.
        results = socket_connection.recv(100)
        screen_lock.acquire()
        print('[+] {}/tcp open'.format(target_port))
        print('[+] {}'.format(results))

    except OSError:
        screen_lock.acquire()
        print('[-] {}/tcp closed'.format(target_port))
    finally:
        screen_lock.release()
        socket_connection.close()


def scan_port(target_host, target_ports):
    try:
        target_ip = gethostbyname(target_host)
    except OSError:
        print('[-] Cannot resolve {}: Unknown Host'.format(target_host))
        return

    try:
        target_name = gethostbyaddr(target_ip)
        print('\n[+] Scan Results for: {}'.format(target_name[0]))

    except OSError:
        print('\n[+] Scan Results for: '.format(target_ip))

    setdefaulttimeout(1)

    for target_port in target_ports:
        t = Thread(target=scan_connection, args=(target_host, target_port))
        t.start()


def main():

    # Begin Parser ------------------------------------------------------------------------------------------------
    parser = argparse.ArgumentParser()

    parser.add_argument('-H', '--host',
                        type=str,
                        required=True,
                        help='specify target host')

    parser.add_argument('-p', '--port',
                        type=str,
                        help='specify target ports, separated by commas (NO spaces: 22,80,443,etc.')

    args = parser.parse_args()

    # note that now args.host holds the name of the host passed in from the cli and args.ports holds the port

    target_host = args.host
    target_port = str(args.port).split(',')

    # End Parser --------------------------------------------------------------------------------------------------

    # If you comment out the parser code above and uncomment the below two lines you can hard code a specific target
    # and a range of ports to scan. This was in here for initial testing but I left it because I found it useful.
    # It is not par of the original book code.

    # target_host = "centos01"
    # target_port = [x for x in range(1, 8092)]

    scan_port(target_host, target_port)


if __name__ == '__main__':
    main()

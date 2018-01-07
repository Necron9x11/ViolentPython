#!/usr/bin/env python3
#
# Filename: nmap_code_snippet.py
#
# Violent Python - A Cookbook for Hackers,Forensic Analysts,Penetration Testers and Security Engineers
# Chapter 2 | Port Scanner Portion of the Morris Work Lookalike - version 1
#
# NOTE: This is a modified version of the nmap code example from pages 40 through 41.
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
# Introduces the nmap module:
# This is a python class to use nmap and access scan results from python3
#
# python-nmap is not native and needs to be installed.
# It can be downloaded from: http://xael.org/pages/python-nmap-en.html or installed via "pip3: sudo -H pip3 python-nmap"
#
# https://pypi.python.org/pypi/python-nmap
#
# ---------------------------------------------------------------------------------------------------------------------
#
# Mods made to run under Python 3.x follow. These include stylistic as well as functional code modifications.
#
# - var/function naming style : Original code used camel case style naming.
#       Updated to use the underscore style:
#           tgtHost became target_host, etc.
#
# - print - Converted all Python 2.x style print statements to use the Python 3.x print() function and
#   the .format string method instead of the string concatenations originally employed. I did this as it is
#   better performance wise and is more feature rich. For instance it does type conversion without the need to
#   call functions like str() and int() all the time.
#
#   print '[+] ' + ip + ' : ' + banner          became:     print('[+] {} : {}'.format(ip, banner))
#
# - optparse code converted to argparse code. This is not required to run under v3.x but optparse is deprecated since
#   v2.7 and moving to argparse is in keeping with my goal of not only converting v2.x specific code to v3.x but also
#   doing my best to make the code more modern and more Pythonic by current standards.
#
# ---------------------------------------------------------------------------------------------------------------------
#
# Functional Changes
#
# The "-p" (port) options flag has been replaced with a positional parameter which avails itself of the "args='+'"
# parameter to the argparser .add_argument method. This allows for passing any number of ports in from the commandline
# without having to worry about comma placement or spacing (in case you are a sometimes sloppy keyboardist like myself).
#
# There are also a few informational print statements which have been added as well.
#
import nmap
import argparse


def netmap_scan(target_host,  target_port):
    print('DBG: *** IN netmap_scan(target_host,  target_port):')
    nmap_scan = nmap.PortScanner()
    print('[*] Scanning host: {} ({}) on port: {} ({})'.format(target_host, type(target_host),
                                                               target_port, type(target_port)))
    nmap_scan.scan(target_host, target_port)

    port_state = nmap_scan[target_host]['tcp'][int(target_port)]['state']
    print('[*]  {} tcp/{} {}'.format(target_host, target_port, port_state))

    print('\n')


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-H', '--host',
                        type=str,
                        required=True,
                        help='specify target host')

    # this was changed from the original flag to a positional parameter so to leverage the "nargs='+'" parameter which
    # allows us to supply as many ports, separated by spaces, on the cli as we want. The original code required ports
    # to be entered on the cli in the format "22, 25, 80" (without the parentheses) and later code that parsed this
    # would throw an exception if there was not a comma and exactly one space between each port number. This format
    # for allows any number of ports to be supplied on the cli and any number of spaces could be between them.
    parser.add_argument('ports',
                        type=str,
                        nargs='+',
                        help='specify target port[s]')

    args = parser.parse_args()

    # note that now args.host holds the name of the host passed in from the cli and args.ports holds the port

    target_host = args.host
    # the original code expected a comma separated list of port numbers and then created a list by splitting on the
    # commas: tgtPorts = str(options.tgtPort).split(', '). Because ports was implemented as a positional parameter
    # with the "args='+'" option, instead of a flag, the following line of code assigns a list to target_ports.
    target_ports = args.ports

    for target_port in target_ports:
        netmap_scan(target_host, target_port)


if __name__ == '__main__':
    main()

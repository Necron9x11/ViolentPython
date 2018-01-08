#!/usr/bin/env python3
#
# pexpect module Example Code
#
# Original Author: Noah Spurrier (I suppose)
#
# From: http://pexpect.readthedocs.io/en/latest/overview.html
# This connects to the openbsd ftp site and
# downloads the recursive directory listing.
#
# Modifications by Daniel Raphael
#
# The server at ftp.openbsd.org only accepts http/https requests for sometime now so the server used was switched to
# mirrors.mit.edu.
#
# In this version I have removed print statements included on pexpect-example-012.py that were used to display text
# output by the ftp server. In their place I have used the .logfile method to direct the connected servers output
# to stdout. This makes for shorter much more readable code if you do not need to see any output unless debugging.
#
# Note to self: A better server to test against would be test.rebex.net:
#
# test.rebex.net:22 | demo/password | Includes HTTP, SSH, FTP/SSL, FTP, IMAP, POP3 and Time protocols. | Read-only
#
# ---------------------------------------------------------------------------------------------------------------------
#
# Original Listing:
#
# import pexpect
# child = pexpect.spawn('ftp ftp.openbsd.org')
# child.expect('Name .*: ')
# child.sendline('anonymous')
# child.expect('Password:')
# child.sendline('noah@example.com')
# child.expect('ftp> ')
# child.sendline('lcd /tmp')
# child.expect('ftp> ')
# child.sendline('cd pub/OpenBSD')
# child.expect('ftp> ')
# child.sendline('get README')
# child.expect('ftp> ')
# child.sendline('bye')
#
# ---------------------------------------------------------------------------------------------------------------------
#


# ---------------------------------------------------------------------------------------------------------------------
#
import pexpect
import sys

child = pexpect.spawn('ftp mirrors.mit.edu')
child.logfile = sys.stdout.buffer

child.expect('Name .*: ')
child.sendline('anonymous')             # enter "anonymous" when prompted for a username.

child.expect('Password:')
child.sendline('noah@example.com')      # send bogus email account as a password for user anonymous

child.expect('ftp> ')
child.sendline('pass')                  # set to passive mode to avoid:
#                                         #   Illegal PORT command.
#                                         #   bind: Address already in use\r\n@'

child.expect('ftp> ')
child.sendline('cd pub/OpenBSD')        # change directory to pub/OpenBSD

child.expect('ftp> ')
child.sendline('binary')                # set transfer mode to binary

child.expect('ftp> ')
child.sendline('prompt')                # issue a prompt command to disable interactive prompting

child.expect('ftp> ')
child.sendline('get README')            # use "get to download file README.TXT

child.expect('ftp> ')
child.sendline('ls -alm')               # retrieve a directory listing

child.expect('ftp> ')
child.sendline('bye')                   # log off by closing the ftp client

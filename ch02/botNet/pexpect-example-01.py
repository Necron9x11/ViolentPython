#!/usr/bin/env python3
#
# pexpect module Example Code
#
# Author: Noah Spurrier (I suppose)
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
# In this version I have added print statements to display the text output by the ftp server. Otherwise nothing at all
# displays on the screen while the program is running unless there is an error. pexpect-example-02.py omits these
# statements and instead uses the .logfile method to direct the connected servers output to the stdout.
#
# You can see from the output that what is being received is binary encoded (indicated by the "b" that precedes
# each string: b'anonymous\r\n331 Please specify the password.\r\n'
#              ^
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
import pexpect

child = pexpect.spawn('ftp mirrors.mit.edu')

child.expect('Name .*: ')
print(child.before)
print('{}\n'.format(child.after))
child.sendline('anonymous')             # enter "anonymous" when prompted for a username.

child.expect('Password:')
print(child.before)
print('{}\n'.format(child.after))
child.sendline('noah@example.com')      # send bogus email account as a password for user anonymous

child.expect('ftp> ')
print(child.before)
print('{}\n'.format(child.after))
child.sendline('pass')                  # set to passive mode to avoid:
#                                         #   Illegal PORT command.
#                                         #   bind: Address already in use\r\n@'

child.expect('ftp> ')
print(child.before)
print('{}\n'.format(child.after))
child.sendline('cd pub/OpenBSD')        # change directory to pub/OpenBSD

child.expect('ftp> ')
print(child.before)
print('{}\n'.format(child.after))
child.sendline('binary')                # set transfer mode to binary

child.expect('ftp> ')
print(child.before)
print('{}\n'.format(child.after))
child.sendline('prompt')                # issue a prompt command to disable interactive prompting

child.expect('ftp> ')
print(child.before)
print('{}\n'.format(child.after))
child.sendline('get README')            # use "get to download file README.TXT

child.expect('ftp> ')
print(child.before)
print('{}\n'.format(child.after))
child.sendline('ls -alm')               # retrieve a directory listing

child.expect('ftp> ')
print(child.before)
print('{}\n'.format(child.after))

child.sendline('bye')                   # log off by closing the ftp client



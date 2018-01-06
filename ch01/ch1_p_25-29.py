#!/usr/bin/env python3
#
# Filename: vulnscanner.py
#
# Violent Python - A Cookbook for Hackers,Forensic Analysts,Penetration Testers and Security Engineers
# Chapter 1 | Zip File Password Cracker Workup - version 1
# pp.25-29
#
# ---------------------------------------------------------------------------------------------------------------------
#
# Introduces the zipfile module:
# "This module does not currently handle multi-disk ZIP files. It can handle ZIP files that use the ZIP64 extensions
# (that is ZIP files that are more than 4 GiB in size). It supports decryption of encrypted files in ZIP archives,
# but it currently cannot create an encrypted file. Decryption is extremely slow as it is implemented in native Python
# rather than C."
#
# https://docs.python.org/3.5/library/zipfile.html
#
# Introduces the argparse module:
# The argparse module makes it easy to write user-friendly command-line interfaces. The program defines what arguments
# it requires, and argparse will figure out how to parse those out of sys.argv. The argparse module also automatically
# generates help and usage messages and issues errors when users give the program invalid arguments.
#
# https://docs.python.org/3.5/library/argparse.html?highlight=argparse#module-argparse
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
#   the .format string method instead of the string concatenations originally employed. I did this as it is
#   better performance wise and is more feature rich. For instance it does type conversion without the need to
#   call functions like str() and int() all the time.
#
#   print '[+] ' + ip + ' : ' + banner          became:     print('[+] {} : {}'.format(ip, banner))
#
# - exit() - converted all instances of "exit()" to "sys.exit()" as "exit()" is meant for the interactive
#   environment and "sys.exit()" is preferred for use in source files that will be executed from the command line.
#
# - f = open(filename, 'r') - changed this to use the more Pythonic form: with open(filename, 'rU') as f:
#
# Original Author: TJ O'Connor
# Modified to run under Python 3.x by: Daniel Raphael
#
# ---------------------------------------------------------------------------------------------------------------------
#
# Python3 is expected:
#
import sys
if sys.version_info[0] != 3 or sys.version_info[1] < 5:
    sys.exit('This program needs Python3.5.0+')

# print('Python version is: {}'.format(sys.version_info))


# ---------------------------------------------------------------------------------------------------------------------
#
# Initial code - p.25
#
# import zipfile
# zip_file = zipfile.ZipFile("evil.zip")
# zip_file.extractall(pwd=b"secret")

# ---------------------------------------------------------------------------------------------------------------------
#
# p.26 Code Expansion
#
# import zipfile
# zip_file = zipfile.ZipFile("evil.zip")
#
# try:
#     zip_file.extractall(pwd=b"oranges")
#
# except RuntimeError as e:                         # Modified: was except Exception which is too general an exception
#     print(e)                                      # for 3.x code

# ---------------------------------------------------------------------------------------------------------------------
#
# p.26 Continue to expand on initial code
#
# import zipfile
# zip_file = zipfile.ZipFile("evil.zip")
# with open("dictionary.txt", "rU") as pass_file:    # Modified the file read to use the correct Pythonic method.
#     for line in pass_file.readlines():
#         password = line.strip('\n')
#         try:
#             zip_file.extractall(pwd=password.encode())
#             print('[+] Password = {}\n'.format(password))
#             sys.exit(0)                             # Should use the sys form of exit() from within source files
#
#         except RuntimeError as e:                   # Modified: was except Exception which is too general an exception
#             pass                                    # for 3.x code

# ---------------------------------------------------------------------------------------------------------------------
#
# p.27 Modularize initial linear version of code
#
# import zipfile
#
#
# def extract_file(zip_file, password):
#     try:
#         zip_file.extractall(pwd=password.encode())
#         return password
#
#     except RuntimeError:                               # Modified: was except Exception which is too general an
#         return                                         # exception for 3.x code
#
#
# def main():
#     zip_file = zipfile.ZipFile("evil.zip")
#     with open("dictionary.txt", "rU") as pass_file:    # Modified the file read to use the correct Pythonic method.
#         for line in pass_file.readlines():
#             password = line.strip('\n')
#             guess = extract_file(zip_file, password)
#             if guess:
#                 print('[+] Password = {}\n'.format(password))
#                 exit(0)
#
#
# if __name__ == '__main__':
#     main()

# ---------------------------------------------------------------------------------------------------------------------
#
# pp.27-28 Modify to increase program performance by utilizing threads
#
# import zipfile
# from threading import Thread
#
#
# def extract_file(zip_file, password):
#     try:
#         zip_file.extractall(pwd=password.encode())
#         print('[+] Found password: {}\n'.format(password))
#
#     except RuntimeError:                               # Modified: was except Exception which is too general an
#         pass                                           # exception for 3.x code
#
#
# def main():
#     zip_file = zipfile.ZipFile("evil.zip")
#     with open("dictionary.txt", "rU") as pass_file:    # Modified the file read to use the correct Pythonic method.
#         for line in pass_file.readlines():
#             password = line.strip('\n')
#             t = Thread(target=extract_file, args=(zip_file, password))
#             t.start()
#
#
# if __name__ == '__main__':
#     main()

# ---------------------------------------------------------------------------------------------------------------------
#
# start()
# pp.28-29 Modify program to take commandline switches by adding the argparse library.
# The book's initial code used the optparse library which is deprecated since v2.7
#
from threading import Thread
import zipfile
import argparse


def extract_file(zip_file, password):
    try:
        zip_file.extractall(pwd=password.encode())
        print('[+] Found password: {}\n'.format(password))

    except RuntimeError:                               # Modified: was except Exception which is too general an
        pass                                           # exception for 3.x code


def main():
    # Setup argparse parser
    parser = argparse.ArgumentParser(description="takes the name of an encrypted zip file and the name of a password "
                                                 "dictionary file as arguments and then attempts a brute force "
                                                 "password attack on the archive. Currently only attempts to crack "
                                                 "using the words in the dict line for line. No functionality for"
                                                 "using word combinations or patterns is currently implemented.",
                                     epilog="Does not handle multi zip files."
                                     )

    parser.add_argument("-f", "--file",
                        type=str,
                        required=True,
                        help="specify zip file to crack")

    parser.add_argument("-d", "--dictionary",
                        type=str,
                        required=True,
                        help="specify dictionary file to use")

    args = parser.parse_args()

    zip_file = zipfile.ZipFile(args.file)
    with open(args.dictionary, "rU") as pass_file:    # Modified the file read to use the correct Pythonic method.
        for line in pass_file.readlines():
            password = line.strip('\n')
            t = Thread(target=extract_file, args=(zip_file, password))
            t.start()


if __name__ == '__main__':
    main()

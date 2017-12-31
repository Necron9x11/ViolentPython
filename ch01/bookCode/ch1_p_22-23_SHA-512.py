#!/usr/bin/env python3
#
# Filename: vulnscanner.py
#
# Violent Python - A Cookbook for Hackers,Forensic Analysts,Penetration Testers and Security Engineers
#
# From pp.22-23
#
# Original Author: TJ O'Connor
# Modified to run under Python 3.x by: Daniel Raphael
#

import crypt

def test_pass(crypt_pass):
    salt = crypt_pass[0:2]
    with open('dictionary.txt', 'rU') as dict_file:
        for word in dict_file:
            word = word.strip('\n')
            crypt_word = crypt.crypt(word, salt)
            if (crypt_word == crypt_pass):
                print('[+] Found Password: {}'.format(word))
                return
        print('[-] Password Not Found.')
        return
def main():
    with open('passwords.txt', 'rU') as pass_file:
        for line in pass_file:
            if ':' in line:
                user = line.split(':')[0]
                crypt_pass = line.split(':')[1].strip(' ')
                print('[*] Cracking Password For: {}'.format(user))
                test_pass(crypt_pass)


if __name__ == '__main__':
    main()



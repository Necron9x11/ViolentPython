#!/usr/bin/env python3

import socket


def ret_banner(ip, port):
    try:
        socket.setdefaulttimeout(5)
        s = socket.socket()
        s.connect((ip, port))
        banner = s.recv(1024)
        return banner
    except Exception as e:
        print('[-] Error: {}'.format(e))
        return


def check_vulns(banner):
    if 'FreeFloat Ftp Server (Version 1.00)' in banner.decode("utf-8"):
        print('[+] FreeFloat FTP Server is vulnerable.')
    elif '3Com 3CDameon FTP Server Version 2.0' in banner.decode("utf-8"):
        print('[+] 3CDameon FTP Server is vulnerable.')
    elif 'Ability Server 2.34' in banner.decode("utf-8"):
        print('[+] Ability FTP Server is vulnerable.')
    elif 'Sami FTP Server 2.0.2' in banner.decode("utf-8"):
        print('Sami FTP Server is vulnerable')
    else:
        print('[-] FTP Server is not vulnerable')


def main():
    ip1 = '192.168.0.145'
    ip2 = '192.168.0.147'
    ip3 = '192.168.0.50'
    port = 22
    banner1 = ret_banner(ip1, port)
    if banner1:
        print('[+] {} : {}'.format(ip1, banner1))
    banner2 = ret_banner(ip2, port)
    if banner2:
        print('[+] {} : {}'.format(ip2, banner2))
    banner3 = ret_banner(ip3, port)
    if banner3:
        print('[+] {} : {}'.format(ip3, banner3))


if __name__ == '__main__':
    main()

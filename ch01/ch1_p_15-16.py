#!/usr/bin/env python3

import socket


def ret_banner(ip, port):
    try:
        socket.setdefaulttimeout(2)
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
    port_list = [21, 22, 25, 80, 110, 443]
    for x in range(1, 255):
        ip = '192.168.0.' + str(x)
        for port in port_list:
            banner = ret_banner(ip, port)
            if banner:
                print('[+] {}: {}'.format(ip, banner))
                check_vulns(banner)

    print('End Run')


if __name__ == '__main__':
    main()

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

def main():
    ip1 = '192.168.0.145'
    ip2 = '192.168.0.147'
    port = 22
    banner1 = ret_banner(ip1, port)
    if banner1:
        print('[+] {} : {}'.format(ip1, banner1))
    banner2 = ret_banner(ip1, port)
    if banner2:
        print('[+] {} : {}'.format(ip2, banner2))


if __name__ == '__main__':
    main()
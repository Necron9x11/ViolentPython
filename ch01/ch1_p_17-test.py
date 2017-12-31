#!/usr/bin/env python3

import socket


def ret_banner(ip, port):
    try:
        socket.setdefaulttimeout(2)
        s = socket.socket()
        s.connect((ip, port))
        banner = s.recv(1024)
        return banner.decode("utf-8")   # decode the banner from byte type to a utf-8 string before passing it back.
    except Exception as e:              # this saves us from having to do the conversion in multiple places later.
        print('[-] Error: {}'.format(e))
        return


def check_vulns(banner):
    f = open('vuln_banners.txt', 'r')
    for line in f.readlines():
        if line.strip('\n') in banner:
            print('[+] Server is vulnerable: {}'.format(banner.strip('\n')))


def main():
    port_list = [21, 22, 25, 80, 110, 443]
    for x in range(144, 151):           # focus on just the few servers I have for testing
        ip = '192.168.0.' + str(x)
        for port in port_list:
            banner = ret_banner(ip, port)
            if banner:
                print('[+] {}: {}'.format(ip, banner.strip('\n')))  # strip newline causing annoying gap in the output.
                check_vulns(banner)

    print('End Run')


if __name__ == '__main__':
    main()

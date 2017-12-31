#!/usr/bin/env python3

import sys
import os


if len(sys.argv) == 2:
    filename = sys.argv[1]
    if not os.path.isfile(filename):
        print('[-] {} does not exist.'.format(filename))
        sys.exit(0)
    if not os.access(filename, os.R_OK):
        print('[-] {} access denied'.format(filename))
        exit(0)
    print('[+] Reading vulnerabilities from {}'.format(filename))


# OUTPUT:
# programmer$ python ./ch1_p_18-2.py vuln_banners.txt
# [+] Reading vulnerabilities from vuln_banners.txt

# programmer$ python ./ch1_p_18-2.py vuln_banners2.txt
# [-] vuln_banners2.txt does not exist.

# programmer$ python ./ch1_p_18-2.py vuln_banners.txt
# [-] vuln_banners.txt access denied


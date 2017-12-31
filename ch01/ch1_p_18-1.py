#!/usr/bin/env python3

import sys

if len(sys.argv) == 2:
    filename = sys.argv[1]
    print('[+] Reading vulnerabilities from {}'.format(filename))

# OUTPUT:
# programmer$ python ./ch1_p_18.py vuln_banners.txt
# [+] Reading vulnerabilities from vuln_banners.txt
# programmer$

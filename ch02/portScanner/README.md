Port Scanner Module Breakdown
-----------------------------

In the book, the port scanner portion of the worm code is broken down into five distinct sections by the author.

First the script needs to accept a hostname/ip and a list of ports to scan.

Second the program mus translate the hostname into an IPv4 address.

Third, the program has to connect to each port at the given address.

And last the program will send garbage data to any port it connects to. This is done so it can read the banner sent back, from which we can identify what application we have connected to on that port.

Author: Ch4ni
Date: 2012, March 10

This is the simple python task I was asked to complete for a job interview
It is a simple python module that makes parsing a torrent file rather easy.
Included is a very quick, very dirty, test application (tparse)  that will print out most things you would ever
want to know are included in the torrent file (unless, of course, you're a sick puppy and want to
also view the piece hashes).

The library was written using python 2.7.2, x86_64 on OSX 10.6.8.

I used the following site to look up the torrent specification for the purposes of writing this library:
http://wiki.theory.org/BitTorrentSpecification

If you visit that site, you will notice that there is a list of reference implementations for decoding
the bencoded data present in a torrent file. I did not look at this reference implementation until I
was happy with my own (which I designed for succinctness and clarity of expression, rather than speed).
You will notice that my implementation starts from the start of the string and works its way inwards,
whereas the reference implementation for python starts from the end and works its way backwards (basically,
by dissecting the tree).

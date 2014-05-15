GRC Bit Converter
=================

GRC Bit Converter (grc_bit_converter.py) is a python script for parsing and printing data produced by [GNU-Radio Companion](http://gnuradio.org/redmine/projects/gnuradio/wiki/GNURadioCompanion)'s Clock Recovery MM and Binary Slicer blocks. This script takes a file with bits represented as bytes (a 0 represented as 0x00 and a 1 represented as 0x01) and combines them into their intended byte representation. Once combined the script provides several capabilities for packetizing, inverting, shifting, identify Correlated Access Encoded packets, and searching the data.

Author: Don C. Weber (cutaway) - [@cutaway](http://twitter.com/cutaway)
Company: [InGuardians, Inc.](http://inguardians.com)
Start Date: May 15, 2014
Contributers: Be the first

## Usage:

```
grc_bit_converter.py: 
    -f <file>:       Input file (required)"
    -p <size>:       Size of the packet (defaults to 250)"
    -s <string>:     Search for a string. This will also supress packet printing."
    -i:              Invert the bits of the byte. This may be necessary if high"
                     actually represents a 0 instead of a 1 and visa versa."
    -c:              Data is coded. Therefore look for 2's and 3's as packet markers."
    -b <number>:     Bypass this number of BITS. NOTE: only used for non-coded parsing."
```

## Todo: 
* modualize for use in other scripts
* search for user provided preamble
* search for user provided SyncWords
* handle dynamic length bytes for packet printing
* document code better
* remove dependancy on bitarray 0.8, if possible

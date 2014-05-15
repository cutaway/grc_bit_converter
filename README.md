GRC Bit Converter
=================

GRC Bit Converter (grc_bit_converter.py) is a python script for parsing and printing data produced by [GNU-Radio Companion](http://gnuradio.org/redmine/projects/gnuradio/wiki/GNURadioCompanion)'s Clock Recovery MM and Binary Slicer blocks. This script takes a file with bits represented as bytes (a 0 represented as 0x00 and a 1 represented as 0x01) and combines them into their intended byte representation. Once combined the script provides several capabilities for packetizing, inverting, shifting, identify Correlated Access Encoded packets, and searching the data.

* Author: Don C. Weber (cutaway) - [@cutaway](http://twitter.com/cutaway)
* Company: [InGuardians, Inc.](http://inguardians.com)
* Start Date: May 15, 2014
* Contributers: Be the first

## Requirements:

* [Python BitArray](https://pypi.python.org/pypi/bitarray) -  Version 0.8
** Ubuntu may try to install a really old version of BitArray. Don't be fooled, it will not work.

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

## Example:
The following is an example of parsing captured data as outlined in [Converting Radio Signals to Data Packets](http://www.inguardians.com/pubs/GRC_signal_analysis_InGuardians_v1.pdf).

```
cutaway> python ~/InG-Storage/Research/Dev/grc_bit_converter/grc_bit_converter.py -c -p 18 -f blog_demod_1e6_905.99e6_gfsk_76721_lfp_hackrf_coded.dat
Starting Packet Parsing.

New Packet: 0
Size: 17
Occurances: 1
xV4H��� U��;

\x0f\x78\x56\x34\x10\x48\xb9\xcc\xf7\x20\x03\x55\x01\x1d\xea\xff\x3b

New Packet: 1
Size: 17
Occurances: 1
xV4H��� V!��▒

\x0f\x78\x56\x34\x10\x48\xb9\xcc\xf7\x20\x03\x56\x01\x21\xe5\xfa\x1a

New Packet: 2
Size: 17
Occurances: 1
xV4H��� W)��

\x0f\x78\x56\x34\x10\x48\xb9\xcc\xf7\x20\x03\x57\x01\x29\xe0\xf3\x04


```

## Todo: 
* modualize for use in other scripts
* search for user provided preamble
* search for user provided SyncWords
* handle dynamic length bytes for packet printing
* document code better
* remove dependancy on bitarray 0.8, if possible

# grc_bit_converter.py - functions to parse and modify data produced
#                        by GNU-Radio Companion's Clock Recovery MM and
#                        Binary Slicer blocks.
# 
# Copyright (c) 2014, InGuardians, Inc. <consulting@inguardians.com>
# This file is part of Foobar.
# 
# Foobar is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# Foobar is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Point Of Contact:    Don C. Weber <don@inguardians.com>


# Requirement is bitarry 0.8
# https://pypi.python.org/pypi/bitarray/0.8.1
from bitarray import bitarray
import os, sys
import re

def str2hex(data):
    '''Convert a string to their hex representation'''
    tmp = ''
    for e in range(0,len(data),2):
        # Grab 2 characters and decode them as their hex values
        tmp += data[e:e+2].decode('hex_codec')
    return tmp

def print_data(data = ''):
    '''Returns the results of incoming data in human-readable and printable format'''
    if data == '':
        return ''
    tstring = []
    for e in data:
        tstring.append('\\\\x'.decode('string_escape') + hex(ord(e))[2:])
    for e in range(len(tstring)):
        if len(tstring[e]) == 3:
            tmp = list(tstring[e])
            tmp.insert(-1,'0')
            tstring[e] = ''.join(tmp)
    return ''.join(tstring)

# Help
def usage():
    print "bit_convert.py:  This script will take the demodulated wave output that has"
    print "                 been processed through gnuradio-companion's Clock Recovery MM,"
    print "                 Binary Slicer, and Correlate Access Code. Thes blocks generate"
    print "                 binary output where ones are 00000001 and zeros are 00000000."
    print "                 These must be combined to create a normal byte."
    print ""
    print "-f <file>:       Input file (required)"
    print "-p <size>:       Size of the packet (defaults to 250)"
    print "-s <string>:     Search for a string. This will also supress packet printing."
    print "-i:              Invert the bits of the byte. This may be necessary if high"
    print "                 actually represents a 0 instead of a 1 and visa versa."
    print "-c:              Data is coded. Therefore look for 2's and 3's as packet markers."
    print "-b <number>:     Bypass this number of BITS. NOTE: only used for non-coded parsing."
    sys.exit()

# Set values
inf        = ''         # input file
sdata      = ''         # data to search for
coded      = False
search     = False
invert     = False      # Is 0 High or 1 High? Inverting lets us switch back and forth
bypass     = 0
max_packet = 250        # Known value from test packets

# Control values
ind        = ''         # incoming file data
cnt        = 0          # counter
temp_byte  = ''         # Temp byte of bit string to be converted to actual byte
new_byte   = ''         # New data byte
packets    = []         # List of packets
dpackets   = []         # List of decoded packets
preambles  = ['\xaa\xaa','\x55\x55']
# 0xd391 in binary is 0b1101001110010001
syncwords  = ['\xd3\x91','\xa7\x22','\x4e\x44','\x9c\x88']

# Process Options
ops = ['-s','-i','-f','-p','-c','-b']

while len(sys.argv) > 1:
    op = sys.argv.pop(1)
    if op == '-f':
        inf = sys.argv.pop(1)
    if op == '-s':
        search = True
        sdata = sys.argv.pop(1)
    if op == '-i':
        print "Inverting data."
        invert = True
    if op == '-p':
        max_packet = int(sys.argv.pop(1))
    if op == '-c':
        coded = True
    if op == '-b':
        bypass = int(sys.argv.pop(1))
    if op not in ops:
        print "Unknown option:"
        usage()

# Grab file data
try:
    ind = open(inf,'r').read()
except:
    print "Error accessing file:",inf
    usage()

# If the byte is 2 or 3 then we have a packet.
if coded:
    # Process packets according to the leading 2 or 3
    for cnt in range(len(ind)):
        if ord(ind[cnt]) > 1:
            # Build each packet
            if cnt:
                packets.append(ind[cnt:cnt+(max_packet*8)])
            else:
                packets.append(ind[cnt:(cnt+1)+(max_packet*8)])
else:
    # Process all bytes as packets
    for cnt in range(bypass,len(ind),(max_packet*8)):
        if cnt:
            packets.append(ind[cnt:cnt+(max_packet*8)])
        else:
            packets.append(ind[cnt:(cnt+1)+(max_packet*8)])

# Process all packets
print "Starting Packet Parsing."
for packet in packets:
    #print "\nNew Packet:"

    # Process each packet by building an 8 bit string that represents a byte
    temp_byte = ''
    new_byte = ''
    dpacket = []
    for e in packet:

        # Convert each 8 bit string to an actual byte of data
        if len(temp_byte) == 8:
            # Data is just in binary, so convert with int
            #new_byte = int(temp_byte,2) 
            new_byte = bitarray(temp_byte)
            if invert:
                new_byte.invert()
            
            # For now we just want to see printable characters
            # TODO: Remove and write actual bytes to STDOUT so they can be redirected
            #if new_byte > 31 or new_byte < 126:
                #print chr(new_byte),
            #dpacket.append(chr(new_byte))
            dpacket.append(new_byte.tobytes())
            # Clear temp buffer
            temp_byte = ''
            new_byte = ''

        # Build temp byte by concantenation. Must clear lead bit if 2 or 3
        temp_byte += str(ord(e) & 1)

    # Store dpacket in dpackets
    indata = ''.join(dpacket)
    if search:
        if re.search(sdata,indata):
            #print "\nFound it!!"
            dpackets.append(indata)
    else:
        dpackets.append(indata)

for e in range(len(dpackets)):
    print "\nNew Packet:",e
    print "Size:",len(dpackets[e])
    print "Occurances:",str(dpackets.count(dpackets[e]))
    print dpackets[e]
    print ""
    print print_data(dpackets[e])

print "Done."


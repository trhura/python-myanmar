#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""

"""

import os
import sys 
import codecs
import fileinput
import myanmar.converter
from optparse import OptionParser

def convert ():
    
    parser = OptionParser(usage="Usage: %prog [OPTIONS...] [FILE...]",
                          version="%prog 0.1",
                          description="Convert between Myanmar legacy encodings and unicode.\n")

    parser.add_option("-l", "--list", dest="list",
                      action='store_true',
                      help="List supported encodings.")
    parser.add_option("-f", "--from", dest="fro",
                      action='store', type='string',
                      help="Convert characters from ENCODING", metavar="ENCODING")
    parser.add_option("-t", "--to", dest="to",
                      action='store', type='string',
                      help="Convert characters to ENCODING", metavar="ENCODING") 
    parser.add_option("-o", "--output", dest="output_file",
                      help="Write output to FILE", metavar="FILE")
    (options, args) = parser.parse_args()

    encodings = myanmar.converter.get_available_encodings ()
    if options.list:
        for e in encodings:
            print e
        sys.exit (0)

    if not options.fro:
        print "Please, supply the encoding of input chracters (--from)."
        sys.exit (-1)
        
    if not options.to:
        print "Please, supply the encoding for output chracters (--to)."
        sys.exit (-1)

    if not options.fro in encodings:
        print "Unkown encoding %s. Use -l to list supported encodings." %options.fro
        sys.exit (-1)

    data = u''
    if len (args) == 0:
        import select
        if select.select([sys.stdin,],[],[],0.0)[0]:        
            data = sys.stdin.read ()
    else:
        for fil in args:
            try:
                ifile = codecs.open (fil, 'r',encoding='utf8')
                data += ifile.read ()
                ifile.close ()
            except Exception, e:
                print e
                sys.exit (-1)

    print myanmar.converter.convert (data, options.fro, options.to).encode ('utf8'),

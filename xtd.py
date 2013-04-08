#!/usr/bin/env python

#XTD:xherma25

#------------------- MODULES -------------------
import re, sys, string, os
import argparse
import xml.etree.ElementTree as ET
#------------------- MODULES -------------------

#------------------- GLOBALS -------------------

#------------------- GLOBALS -------------------


#--------------------- MAIN --------------------
if __name__ == '__main__':
  #------------------------
  #---------- ARGS ---------
  #------------------------
  parser = argparse.ArgumentParser(description='XML2DDL.')         
  parser.add_argument('--input', dest='input', default=sys.stdin,
                   help='an integer for the accumulator')
  parser.add_argument('--output', dest='output', default="stdout",
                    help='output file (default: stdout)')
  parser.add_argument('--header', dest='header', default="",
                    help='header text (default: "")')
  parser.add_argument('--etc', dest='etc', default=-1,
                    help='max column count (default: inf)')
  parser.add_argument('-a', dest='a', default=0,
                    help='wont generate columns from XML atributes (default: false)')
  parser.add_argument('-b', dest='b', default=0,
                    help='what? (default: false)')
  parser.add_argument('-g', dest='g', default=0,
                    help='bla bla (default: false)')
                    
  args = parser.parse_args()
  print args.input
  print args.output
  print args.etc
  print args.a
  print args.b
  print args.g
  #------------------------
  #---------- ARGS ---------
  #------------------------
  tree = ET.parse(args.input)
  root = tree.getroot()
  #root = ET.fromstring(country_data_as_string)
  
#--------------------- MAIN --------------------
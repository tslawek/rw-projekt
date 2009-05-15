#! /usr/bin/env python

import os
import sys
import StringIO
from corpus import poland
from corpus import gim
from mwlib import parser
from mwlib.dummydb import DummyDB
from mwlib.uparser import parseString
import my_htmlwriter as htmlwriter


a = """	[[BR]]Ala ma kota
	adasdad
asdasdad
{|dasda|}"""
def main():
	print "Test parser test"
	#print poland.decode("utf-8")

	out = StringIO.StringIO()
	db = DummyDB()
	
	input = unicode(poland, 'utf-8')
#	input = unicode(open(sys.argv[1]).read(), 'utf-8')
	r = parseString(title="poland", raw=input, wikidb=db)
#	parser.show(sys.stdout, r)	
		
	w = htmlwriter.HTMLWriter(out,  {'no_table':True})
	w.write(r)

	print out.getvalue()



if __name__ == "__main__":
	main()

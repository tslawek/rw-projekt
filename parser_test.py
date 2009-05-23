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

from collections import defaultdict
t = """

[[Kategoria:Panstwa czlonkowskie Unii Europejskiej]]
[[Kategoria:Panstwa nalezace do NATO]]
[[Kategoria:Polska| ]]
[[Kategoria:Nowe|* ]]


[[Kategoria:Geografia Republiki Poludniowej Afryki]]
[[Kategoria:Przyladki Afryki|Igielny]]


"""
a = """	[[BR]]Ala ma kota
	adasdad
asdasdad
{|dasda|}"""


def writemetadata(metadata):

	tags = { 'metavalue_sep' : "::", 'metadata' : '$$', 'separator' : "#####", 'metakey_sep' : ":::" }
	append_text = ""
	text = ""

	for key in metadata.keys():
		meta_value = tags['metavalue_sep'].join(metadata[key])
		append_text += tags['metadata']+key+ tags['metakey_sep'] + meta_value + tags['metadata'] +"\n"
	append_text += text
	append_text += "\n"+ tags['separator']

	return append_text
	

def category_test():
	pass
def main(name):
	print "Test parser test"
	#print poland.decode("utf-8")

	out = StringIO.StringIO()
	db = DummyDB()
	
	input = unicode(name, 'utf-8')
#	input = unicode(open(sys.argv[1]).read(), 'utf-8')
	r = parseString(title='x', raw=input, wikidb=db)
#	parser.show(sys.stdout, r)	
	metadata = defaultdict(list)
	w = htmlwriter.HTMLWriter(out, metadata,  {'no_table':True, 'category' : True})
	print	w.getCategoryList(r)
	w.write(r)
	
	print metadata
	print out.getvalue()

	print "tu"
	print writemetadata(metadata)	


if __name__ == "__main__":
#	main(poland)
	main(t)

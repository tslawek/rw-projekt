import os
import sys
import StringIO
from mwlib import parser
from mwlib.dummydb import DummyDB
from mwlib.uparser import parseString
import my_htmlwriter as htmlwriter

from collections import defaultdict
class WikiParser():


	def __init__(self, options):
		self.options = options
		self.db = DummyDB()

	def parse(self, title, text):
		out = StringIO.StringIO()
		metadata = defaultdict(list)		

		parsed = parseString(title, raw=text, wikidb = self.db)
		w = htmlwriter.HTMLWriter(out, metadata ,  self.options)
		print metadata
		w.write(parsed)
#		meta_data = [ ('key-word', ['first']), ("category", ['pierwsza', 'druga', 'trzecia']) ]
		
		return (metadata, out.getvalue())


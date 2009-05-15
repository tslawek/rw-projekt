import os
import sys
import StringIO
from mwlib import parser
from mwlib.dummydb import DummyDB
from mwlib.uparser import parseString
import my_htmlwriter as htmlwriter


class WikiParser():


	def __init__(self, options):
		try:
			self.no_table = options['no_table']
		except:
			pass
		self.db = DummyDB()

	def parse(self, title, text):
		out = StringIO.StringIO()

		parsed = parseString(title, raw=text, wikidb = self.db)
		w = htmlwriter.HTMLWriter(out, no_table=self.no_table)
		w.write(parsed)


		return ("", out.getvalue())


#!/usr/bin/python
#-*- coding: utf-8 -*-
from lxml import etree
import sys
path = "./"



def create_file(name, content):
	out = open(path+name+".txt", 'w')
	out.write(content.encode('utf-8'))
	out.close()


def convert(infile):

	context = etree.iterparse(infile, events=("end",), tag='{http://www.mediawiki.org/xml/export-0.3/}text')
	counter, error_counter = 0,0
	for x, text in context:
	#	ret[title.text] = 0
	#	res.append(title.text.encode('utf-8'))
		counter +=1
		try:
			#p = title.getparent().getchildren()[-1].getchildren()[-1].text
			title = text.getparent().getparent().getchildren()[0].text
			id = text.getparent().getparent().getchildren()[1].text
			revision = text.getparent().getchildren()[0].text
			content = text.text
		except:
			
			error_counter +=1
			print "e -------- "
			print str(error_counter) + "/" + str(counter) + " is error"
			print "---" * 3
			continue

		text.clear()
		while text.getprevious() is not None:
			del text.getparent()[0]
		

		create_file(id+"-"+revision, content)

	print "OK: " + str(counter - error_counter)


if __name__ == "__main__":
	convert(sys.argv[1])

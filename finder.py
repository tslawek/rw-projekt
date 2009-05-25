#! /usr/bin/env python

from configuration import *
import re
wiki_text_file_name = read_configuration('Return')['name']
tags = read_configuration('Tags')


def parse_meta_data(meta_data):
	ret = {}
	for line in meta_data.splitlines():
		tmp = line.strip(tags['metadata']).split(tags['metakey_sep'])
		try:
			ret[tmp[0]] = tmp[1].split(tags['metavalue_sep'])
		except IndexError:
			pass

	return ret

def read_wikipedia():

	try:
		file = open(wiki_text_file_name)

	except IOError:
		"can't open file %s" % wiki_text_file_name  
	else:

		text = ""
		meta_data = ""
		start = True
		for line in file:
			if line == tags['separator'] + '\n':
				start = True
				yield( ( parse_meta_data(meta_data), text) )
			elif line.find(tags['metadata']) == 0:
				meta_data += line
			else:
				text += line
			
			if start:
				start = False
				text = ""
				meta_data = ""

		file.close()
	
	
def find_names(text):
	ret = []
	words_pattern = re.compile("\w+")
	p = re.compile("[\w+|\s]{1,30}(?= \(ur\.)")

	for candidate in p.findall(text):
		tmp = []
		ok = True
		for word in reversed(words_pattern.findall(candidate)):
			if word[0].isupper() and ok:
				tmp.append(word)
			else:
				ok = False
		if len(tmp) > 0:
			tmp.reverse()
			ret.append(tmp)
	return ret
			

def demo():

	counter = 0
	ok =0 
	error =0
	for i in read_wikipedia():
		try:
				
			names = find_names(i[1])
			counter +=1
			if len(names) > 0:
				print names
				ok +=1
			
		except:
			error +=1
			print "---" * 20
			print "error: %s / ok: %s" % (error, ok)
			exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
			traceback.print_exception(exceptionType, exceptionValue, exceptionTraceback, limit=9, file=sys.stdout)
		else:
			if (counter%1000) == 0:
				
				print "ok: %s / all: %s" %(ok, counter)

if __name__ == '__main__':
	demo()

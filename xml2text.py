#!/usr/bin/python
#-*- coding: utf-8 -*-
from lxml import etree
import sys, traceback
import os
import re
import string
start_path = os.curdir
path = "txt"
subdir_name_size = 2
zfill_size = 3



def find_file(name):
	
	tmp = name.split('_')
	id = tmp[0]
	revision = tmp[1]
	subdir = name[0:subdir_name_size]
	our_path = os.path.join( os.path.abspath(start_path), path, subdir )
	try:
		file_list = os.listdir(our_path)
	except OSError:
		# nie ma katalogu
		return False
	for file_name in file_list:
		if file_name.rfind(str(id)) == 0:
			if file_name.rfind(str(id) + "_" +str(revision) ) == 0:
				return True # dokladnie taki plik jest
				
			else:
				print "tu ", file_name
				return os.path.join(our_path, file_name) #< mamy pik o dobrym id, ale w innej rewizji, nalezy go uaktualnic
	return False 

def need_update(name):
#	try:
	file = find_file(name)
#	except OSError:
#		print 'error'
#		return True
	if file:
		if isinstance(file, str):
			#update
			try:
				os.remove(file)
				print "updating ", file
			except:
				pass
#			create_file(name, content)
			return True
		else:
			return False
	else:
#		create_file(name, content)
		return True




def create_file(name, content):
	subdir = name[0:subdir_name_size]
	out_path = os.path.join( os.path.abspath(start_path), path, subdir )
	if not os.path.isdir(out_path):
		os.makedirs(out_path)
	out_path_name = os.path.join(out_path, name+'.txt')
	out = open(out_path_name, 'w')
	out.write(content.encode('utf-8'))
	out.close()

def create_file_name(*args):
	def st(arg):
		if isinstance(arg, int):
			return str(arg)
		elif isinstance(arg, str):
			return arg
		elif isinstance(arg, unicode):
			return arg.encode('utf-8')
	return '_'.join(map(st, args))

def test_parser(content):
	print "c"
	return content

def convert(infile, parser, force):

	context = etree.iterparse(infile, events=("end",), tag='{http://www.mediawiki.org/xml/export-0.3/}text')
	counter, error_counter, update_counter = 0,0, 0
	for x, text in context:
	#	ret[title.text] = 0
	#	res.append(title.text.encode('utf-8'))
		counter +=1
		title = ''
		try:
			#p = title.getparent().getchildren()[-1].getchildren()[-1].text
			id = text.getparent().getparent().getchildren()[1].text
			revision = text.getparent().getchildren()[0].text				
			title = re.sub(r'/', '|', text.getparent().getparent().getchildren()[0].text)
			

			file_name = create_file_name(string.zfill(id, zfill_size), revision, title)
			#update or create file
			if force:
			
				content = parser(text.text)
				create_file(file_name, content)
			else:
				if need_update(file_name):
					content = parser(text.text)
					create_file(file_name, content)
		

		except:
			exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
			traceback.print_exception(exceptionType, exceptionValue, exceptionTraceback, limit=9, file=sys.stdout)

			error_counter +=1
			print "e -------- "
			print title
			print str(error_counter) + "/" + str(counter) + " is error"
			print "---" * 3
			continue

		text.clear()
		while text.getprevious() is not None:
			del text.getparent()[0]
		
	print "OK: " + str(counter - error_counter)



if __name__ == "__main__":
	convert(sys.argv[1], test_parser, True)

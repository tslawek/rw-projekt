#! /usr/bin/env python

from configuration import *
from collections import defaultdict
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
	
	
def find_names_in_text(text):
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
			


def context(word, text):
	all_words = [""] + [w.lower() for w in text.split()] + [""]
	pos = all_words.index(word)
	word_before = all_words[pos - 1]
	word_after = all_words[pos + 1]
	return word_before, word_after

def find_countries():

	COUNTRIES = set("polska niemiecka francuska belgijska czeska".split())
	prefixes, suffixes = defaultdict(int), defaultdict(int)

	for meta, text in read_wikipedia():
		words = set(w.lower() for w in text.split())
		if words & COUNTRIES:
			for word in words & COUNTRIES:
				cb, ca = context(word, text)
				if cb.isalpha():
					prefixes[cb] += 1
				if ca.isalpha():
					suffixes[ca] += 1
	#print 'PREFIXES:'
	#for n, w in sorted(((v, k) for (k, v) in prefixes.items()), reverse=True)[:20]:
		#print n, w
	#print 'SUFFIXES:'
	#for n, w in sorted(((v, k) for (k, v) in suffixes.items()), reverse=True)[:20]:
		#print n, w

	popular_prefixes = [word for n, word in sorted(((v, k) for (k, v) in prefixes.items()), reverse=True)[:100]]
	popular_suffixes = [word for n, word in sorted(((v, k) for (k, v) in suffixes.items()), reverse=True)[:100]]
	
	other_p, other_s = defaultdict(list), defaultdict(list)

	for _, text in read_wikipedia():
		words = text.lower().split()
		for prefix in popular_prefixes:
			if prefix.lower() in words and words[-1] != prefix:
				other_p[prefix].append(words[words.index(prefix) + 1])
				if len(other_p[prefix]) > 100:
					break
		
		for sufffix in popular_suffixes:
			if sufffix.lower() in words and words[0] != sufffix:
				other_s[sufffix].append(words[words.index(sufffix) - 1])
				if len(other_s[sufffix]) > 100:
					break

	discriminator_p, discriminator_s = defaultdict(list), defaultdict(list)
	for prefix, words in other_p.items():
		print 
#		print prefix.upper()
		i, all = 0.0 , 1.0
		for w in words:
			if len(w) > 2:
				all +=1
				if w in COUNTRIES:
					i +=1
		discriminator_p[prefix] = i/all


	for sufffix, words in other_s.items():
		print 
#		print sufffix.upper()


		i, all = 0.0 , 1.0
		for w in words:
			if len(w) > 2:
				all +=1
				if w in COUNTRIES:
					i +=1
		discriminator_s[sufffix] = i/all

	pref_ =  sorted(((v, k) for (k, v) in discriminator_p.items()), reverse=True)
	suff_ =  sorted(((v, k) for (k, v) in discriminator_s.items()), reverse=True)
		
	
	p = set()
	s = set()
	for i in range(10):
		p |= set(other_p[pref_[i][1]]) 
		s |= set(other_s[suff_[i][1]])
	
		#ret = set(other_p[pref_[i][1]]) & set(other_s[suff_[i][1]])
	#	print s
	#	print '-' * 80
	#	print p

	print '-' * 80
	print p & s
			

def find_names():

	counter = 0
	ok =0 
	error =0
	for i in read_wikipedia():
		try:
				
			names = find_names_in_text(i[1])
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
"""
COUNTRIES = set("polska niemiecka francuska belgijska czeska".split())


def demo2():
	prefixes, suffixes = defaultdict(int), defaultdict(int)

	for meta, text in read_wikipedia():
		words = set(w.lower() for w in text.split())
		if words & COUNTRIES:
			for word in words & COUNTRIES:
				cb, ca = context(word, text)
				if cb.isalpha():
					prefixes[cb] += 1
				if ca.isalpha():
					suffixes[ca] += 1
	#print 'PREFIXES:'
	#for n, w in sorted(((v, k) for (k, v) in prefixes.items()), reverse=True)[:20]:
		#print n, w
	#print 'SUFFIXES:'
	#for n, w in sorted(((v, k) for (k, v) in suffixes.items()), reverse=True)[:20]:
		#print n, w

	popular_prefixes = [word for n, word in sorted(((v, k) for (k, v) in prefixes.items()), reverse=True)[:100]]
	popular_suffixes = [word for n, word in sorted(((v, k) for (k, v) in suffixes.items()), reverse=True)[:100]]
	
	other_p, other_s = defaultdict(list), defaultdict(list)

	for _, text in read_wikipedia():
		words = text.lower().split()
		for prefix in popular_prefixes:
			if prefix.lower() in words and words[-1] != prefix:
				other_p[prefix].append(words[words.index(prefix) + 1])
				if len(other_p[prefix]) > 100:
					break
		
		for sufffix in popular_suffixes:
			if sufffix.lower() in words and words[0] != sufffix:
				other_s[sufffix].append(words[words.index(sufffix) - 1])
				if len(other_s[sufffix]) > 100:
					break

	for prefix, words in other_p.items():
		print 
		print prefix.upper()
		print "  ".join(words)

	for sufffix, words in other_s.items():
		print 
		print sufffix.upper()
		print "  ".join(words)
		
"""


				


if __name__ == '__main__':
	find_countries()
	find_names()

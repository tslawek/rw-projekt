#! /usr/bin/env python
import os
import sys
import re

try:
	import names
except:
	sys.path.append(os.path.abspath(os.curdir))
	import names

from finder import *
def test_find_names():
	assert find_names(names.name1)[0] == ['Adam', 'Nowak', 'Nowakowski']
	assert find_names(names.name4) == [['Jan', 'Kowalski'], ['Adam', 'Mickiewicz' ]]
	assert find_names(names.name2)[0] == ['Jan', 'Kowalski']
	assert find_names(names.name3)[0] == ['Tomasz', 'Gil']
	

def test_parse_meta_data():
	test_text = """$$Kategoria:::Organizacje standaryzacyjne$$
$$strong:::ANSI$$
$$title:::ANSI$$"""

	assert parse_meta_data(test_text) == {'Kategoria': ['Organizacje standaryzacyjne'], 'strong': ['ANSI'], 'title': ['ANSI']}





def ala():
	return "alal"

def test_ala():
	assert ala() == "alal"

if __name__ == "__main__":
	ala()
	test_ala()

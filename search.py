from  finder import read_wikipedia
from PredicateLogic import *
import re
def s():
	for meta, text in  read_wikipedia():
		for i in sentence_split(text):
			yield i


sub_pat = re.compile("((\s|^)([A-Z]|[a-z]|[0-9])|ur|ok|zm)\.")
def sentence_split(text):
	lines = text.split('\n')
	ret = []
	for l in lines:
		tmp = re.sub(sub_pat, r"\1@@", l).split('.') 
		ret += map(lambda x: re.sub("@@", '.', x).strip(), tmp)
	return filter(lambda x: x != '', ret)
			


def test_sentence_split():
	assert sentence_split("ala ur. 123 ma kota. Ala ola ula zm. dawno\nala jest ok. 123") == ["ala ur. 123 ma kota",  'Ala ola ula zm. dawno', 'ala jest ok. 123']
	assert sentence_split("A. b.") == ["A. b."]
	assert sentence_split("Adam M. jest skoczkiem.") == ["Adam M. jest skoczkiem"]

if __name__ == '__main__':
	matcher = 	Placed(Before(2), AnyWord(ExactWord("aktorka"))) & ~Placed(After(2), AnyWord(ExactWord("filmowa")))
	for i in s():
		ret =  find(matcher, i)
		if ret != []:
			print ret

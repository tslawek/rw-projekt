#ecoding=utf-8

import sys
import xml2text
from stripper import strip_wiki_markup

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "usage: main.py test.xml"
    else:
        xml2text.convert(sys.argv[1], strip_wiki_markup, True)

	#import finder
	#finder.demo()
	

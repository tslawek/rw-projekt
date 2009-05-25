#! /usr/bin/env python



def ala():
	print "alal"

def test_ala():
	assert ala() == "alal"

if __name__ == "__main__":
	ala()
	test_ala()

from ctypes import *
import sys

class Wrapper:


	def __init__(self,p):
		
		import sys
		path = p
		#path = "lib/libclp.so" 
		cdll.LoadLibrary(path)
		self.libc = CDLL(path)

		self.libc.clp_init()

	def version(self):

      		self.libc.printf("%s\n", self.libc.clp_ver())

#
#a = c_char_p("adada")
#s = create_string_buffer('\000' * 80)
#i = c_int(1109157)
#print a
#libc.clp_bform(i, s)
    
#print repr(s.value)
	def rec(self, napis):
		ta = c_int * 25
		tab = ta(0)
		wynik = c_int(0)
		ilosc = c_int(0)
		co = c_char_p(napis)
		self.libc.clp_rec(co, tab, pointer(ilosc))
		
		wynik = []
		for i in range(ilosc.value):
			wynik.append(int(tab[i]))
#		print napis + " " + str(wynik)
		return wynik
	
	def rec_utf(self, napis):
		ta = c_int * 25
		tab = ta(0)
		wynik = c_int(0)
		ilosc = c_int(0)
		co = c_char_p(napis.encode('iso-8859-2'))
		self.libc.clp_rec(co, tab, pointer(ilosc))
		
		wynik = []
		for i in range(ilosc.value):
			wynik.append(int(tab[i]))
#		print napis + " " + str(wynik)
		return wynik
	

	def forms(self, numer):
		s = create_string_buffer('\000' * 400 )
		i = c_int(numer)
		self.libc.clp_forms(i, s)
		return repr(s.value).strip("[',:]").split(":")
	
	def label(self, numer):
		s = create_string_buffer('\000' * 20)
		i = c_int(numer)
		self.libc.clp_label(i, s)
		return repr(s.value).strip("'")

	def bform(self, numer):
		s = create_string_buffer('\000' * 30)
		i = c_int(numer)
		self.libc.clp_bform(i, s)
		return repr(s.value).strip("'")

	def vec(self, numer, forma):
		i = c_int(numer)
		s = c_char_p(forma)
		o = c_int * 50
		out = o(0)
		out_len = c_int(0)
		self.libc.clp_vec(i, s, out, pointer(out_len))
		ret = []
		for i in range(out_len.value):
			ret.append(int(out[i]))
		return ret
	
	def all_forms(self, napis):
		wynik = []
		for i in self.rec(napis):
			for f in self.forms(i):
				wynik.append(f)
		return wynik


	def demo(self):
		print self.all_forms("zamek")	
	
def demo(path):
	x = Wrapper(path)
	a = x.rec("dom")
	for i in a:
		print x.label(i)
		print x.vec(i, "domu")

	print "-"*80
	print x.all_forms("zamek")
	
#demo(sys.argv[1])
"""
x = Wrapper()
x.version()
print x.forms(1109234)
print "LABEL\n"
print x.label(1109234)
#print x.bform(1109234)
a = x.bform(1012942)
print type(a)
print a
print len(a)
print x.rec("domowy")
print x.rec(a)
#print x.rec(x.bform(1012942))
print x.rec('zamek')
for i in x.rec('zamek'):
	print x.forms(i)
	
"""

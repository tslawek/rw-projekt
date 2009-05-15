import unittest

class TestXml(unittest.TestCase):
	
	def setUp(self):
		self.arg = [10, 100, "Test"]

	def testname(self):
		import xml2text
		name = xml2text.create_file_name(*self.arg)
		self.assertEqual(name, '10_100_Test')


if __name__ == '__main__':
	unittest.main()

import unittest
import random

import bdecode
import bencode

class TestBencoding(unittest.TestCase):
	strings = {"foobar": "6:foobar"}
	def setUp(self):
		pass

	def test_encodeString(self):
		""" test that we becode a string into a properly bencoded string """
		for key in self.strings:
			encoded_string = bencode.encode(key)
			self.assertEqual(encoded_string, self.strings[key])

	def test_encodeInt(self):
		""" bencode a random number of integers (fewer than 100), with random values (less than one million)
			and ensure that the encoding gives us the proper result
		"""
		for i in range(0, 100):
			num = random.randint(0,1000000)
			self.assertEqual(bencode.encode(num), "".join(['i', str(num), 'e']))

        def test_encodeSimpleList(self):
            unencodedList = ["string", 10]
            encodedList = "l6:stringi10ee"
            self.assertEqual(bencode.encode(unencodedList),encodedList)

        def test_encodeSimpleDict(self):
            unencodedDict = {"first":"string","second":10}
            encodedDict = "d5:first6:string6:secondi10ee" 
            result = bencode.encode(unencodedDict)
            self.assertEqual(result[0], 'd')
            self.assertEqual(result[-1], 'e')
            self.assertTrue("5:first6:string" in result)
            self.assertTrue("6:secondi10e" in result)
            self.assertEqual(len(encodedDict), len(result))

if __name__ == "__main__":
	unittest.main()

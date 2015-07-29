import unittest
import random

import bencode
import bdecode

class TestBdecoding(unittest.TestCase):
	strings = {"foobar": "6:foobar"}
	def setUp(self):
		pass

	def test_decodeString(self):
		""" test that we bdecode a bencoded string into the correct value string """
		for key in self.strings:
			decoded_string = bdecode.decode(self.strings[key])
			self.assertEqual(decoded_string['data'], key)

	def test_encode_decode_String(self):
		""" test that beconding a string, and bdecoding the result, ends up in the initial string """
		for key in self.strings:
			self.assertEqual(bdecode.decode(bencode.encode(key))['data'], key)

	def test_decodeInt(self):
		""" bdecode a random number of bencoded integer strings (fewer than 100) containing random
			integer values (less than one million) and ensure that the decoding gives us the proper
			integer result
		"""
		for i in range(0, 100):
			num = random.randint(0,1000000)
			self.assertEqual(int(bdecode.decode("".join(["i", str(num), "e"]))['data']), num)

        def test_decodeSimpleList(self):
            unencodedList = ["string", 10]
            encodedList = "l6:stringi10ee"
            self.assertEqual(bdecode.decode(encodedList)['data'],unencodedList)

        def test_decodeSimpleDict(self):
            unencodedDict = {"first":"string","second":10}
            encodedDict = "d5:first6:string6:secondi10ee" 
            self.assertEqual(bdecode.decode(encodedDict)['data'], unencodedDict)

if __name__ == "__main__":
	unittest.main()

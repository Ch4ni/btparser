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

	def test_decodeString(self):
		""" test that we bdecode a bencoded string into the correct value string """
		for key in self.strings:
			decoded_string = bdecode.decode(self.strings[key])
			self.assertEqual(decoded_string['data'], key)

	def test_encode_decode_String(self):
		""" test that beconding a string, and bdecoding the result, ends up in the initial string """
		for key in self.strings:
			self.assertEqual(bdecode.decode(bencode.encode(key))['data'], key)

	def test_encodeInt(self):
		""" bencode a random number of integers (fewer than 100), with random values (less than one million)
			and ensure that the encoding gives us the proper result
		"""
		for i in range(0, 100):
			num = random.randint(0,1000000)
			self.assertEqual(bencode.encode(num), "".join(['i', str(num), 'e']))

	def test_decodeInt(self):
		""" bdecode a random number of bencoded integer strings (fewer than 100) containing random
			integer values (less than one million) and ensure that the decoding gives us the proper
			integer result
		"""
		for i in range(0, 100):
			num = random.randint(0,1000000)
			self.assertEqual(int(bdecode.decode("".join(["i", str(num), "e"]))['data']), num)

        def test_encodeSimpleList(self):
            unencodedList = ["string", 10]
            encodedList = "l6:stringi10ee"
            self.assertEqual(bencode.encode(unencodedList),encodedList)

        def test_decodeSimpleList(self):
            unencodedList = ["string", 10]
            encodedList = "l6:stringi10ee"
            self.assertEqual(bdecode.decode(encodedList)['data'],unencodedList)

        def test_encodeSimpleDict(self):
            unencodedDict = {"first":"string","second":10}
            encodedDict = "d5:first6:string6:secondi10ee" 
            result = bencode.encode(unencodedDict)
            self.assertEqual(result[0], 'd')
            self.assertEqual(result[-1], 'e')
            self.assertTrue("5:first6:string" in result)
            self.assertTrue("6:secondi10e" in result)
            self.assertEqual(len(encodedDict), len(result))

        def test_decodeSimpleDict(self):
            unencodedDict = {"first":"string","second":10}
            encodedDict = "d5:first6:string6:secondi10ee" 
            self.assertEqual(bdecode.decode(encodedDict)['data'], unencodedDict)

if __name__ == "__main__":
	unittest.main()

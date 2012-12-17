""" The torrent spec (from http://wiki.theory.org/BitTorrentSpecification)
specifies that a torrent metafile contains a dictionary of bencoded values
(the dictionary itself also being bencoded). This is a helper module to
handle the task of decoding bencoded elements.
"""

def decode(ascii):
	"""
	Detect the type of bencoded string, and pass it off to the correct decoder
	function.
	"""

	decode_funcs = {"i":decodeInteger, "l":decodeList, "d":decodeDictionary}

	if ascii[0].isdigit():
		return decodeString(ascii)
	try:
		return decode_funcs[ascii[0]](ascii)
	except KeyError as e:
		print "invalid bencoding"
		raise e


def decodeString(ascii):
	"""
	Format: <n>:<d>
			<n>: a base 10 integer encoded as an ascii string
			<d>: data of length <n>

	This function splits up a string, gets the expected data length, and returns
	a dictionary containing the data, and the remainder of the supplied string
	argument.
	"""
	len_str = ascii.split(":")[0]
	start = len(len_str) + 1
	end = start + int(len_str)
	return {"data":ascii[start:end], "remainder":ascii[end:]}


def decodeInteger(ascii):
	"""
	Format: i<n>e
			<n>: a base 10 integer encoded as an ascii string

	This function parses out the integer value, and returns a dictionary
	containing the data (as a large integer), and the remainder of the 
	supplied string argument.
	"""
	num_end = ascii.index("e")
	return {"data":long(ascii[1:num_end]), "remainder":ascii[num_end + 1:]}


def decodeList(ascii):
	"""
	Format: l<list>e
			<list>: a list of bencoded values

	This function passes off decoding the next item in the list to the general
	"decode" function until it reaches the token denoting the end of the list
	"""
	list = []
	list_element = {"remainder": ascii[1:]}
	while list_element["remainder"][0] is not "e":
		list_element = decode(list_element["remainder"])
		list.append(list_element["data"])

	return {"data":list, "remainder":list_element["remainder"][1:]}


def decodeDictionary(ascii):
	"""
	Format: d<list>e
			<list>: a list in the form of: <key>:<value> where:
					<key>: a bencoded string
					<value>: a bencoded value

	This function handles decoding the key value, and passes off the value
	decoding to the general "decode" function, until it reaches the token
	denoting the end of the dict.
	"""
	dict = {}
	decode_result_data = {"remainder": ascii[1:], "data": None}
	decode_result_key = {}
	while decode_result_data["remainder"][0] is not "e":
		decode_result_key = decodeString(decode_result_data["remainder"])
		key = decode_result_key["data"]
		decode_result_data = decode(decode_result_key["remainder"])
		data = decode_result_data["data"]
		dict[key] = data

	return {"data":dict, "remainder":decode_result_data["remainder"][1:]}


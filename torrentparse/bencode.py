def encode(obj):
	encode_funcs = {type(""):encodeString, type(0):encodeInteger, type([]):encodeList, type({}):encodeDict}

	try:
		return encode_funcs[type(obj)](obj)
	except KeyError as e:
		print "Invalid python object, must be string, int, list, or dict"
		raise e

def encodeString(ascii):
	return "".join([str(len(ascii)), ":", ascii])

def encodeInteger(num):
	return "".join(["i", str(num), "e"])

def encodeList(lst):
	items = ["l"]
	for item in lst:
		items.append(encode(item))
	items.append("e")
	return "".join(items)

def encodeDict(dictionary):
	items=["d"]
	for key in dictionary:
		items.append(encode(key))
		items.append(encode(dictionary[key]))
	items.append("e")
	return "".join(items)

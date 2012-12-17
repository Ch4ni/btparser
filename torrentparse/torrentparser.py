from datetime import date
import bdecode

class TorrentParser:

	def __init__(self, torrentfile):
		""" To init we open the file that belongs to the supplied path,
		read in the entire contents, close the file, and then decode the contents
		and keep the decoded version around for later reference.
		"""
		file = open(torrentfile, "r")
		contents = file.read()
		file.close()
		self.data = bdecode.decode(contents)["data"]

	def getCreationDate(self):
		""" Creation Date is an optional field according to the torrent spec.
		If the creation date is not available, this will raise an AttributeError
		"""
		try:
			return date.fromtimestamp(self.data["creation date"])
		except KeyError:
			print "no \"creation date\" attribute available"
			raise AttributeError

	def getCreationClient(self):
		""" Creation client is an optional field according to the torrent
		spec. If the creation client is not avaialble, this will raise an
		AttributeError
		"""
		try:
			return self.data["created by"]
		except KeyError:
			print "no \"created by\" attribute available"
			raise AttributeError

	def getTracker(self):
		""" Retrieve the mandatory "announce" field of the torrent file """
		return self.data["announce"]

	def getTrackerList(self):
		""" Tracker list is an optional field according to the torrent
		spec. If the tracker list is not availabe, this will raise an
		AttributeError
		"""
		try:
			return self.data["announce-list"]
		except KeyError:
			print "no \"announce-list\" attribute available"
			raise AttributeError

	def getComment(self):
		""" Comment is an optional field according to the torrent spec.
		If comments are not available, this wil raise an AttributeError
		"""
		try:
			return self.data["comment"]
		except KeyError:
			print "no \"comment\" attribute available"
			raise AttributeError

	def getEncoding(self):
		""" Encoding is an optional field according to the torrent spec.
		If encoding is not available, this will raise an AttributeError
		"""
		try:
			return self.data["encoding"]
		except KeyError:
			print "no \"encoding\" attribute available"
			raise AttributeError

	def getFileAttrs(self, attr="path"):
		""" This method will move on regardless of whether or not an attribute is not
		available for a single file. The rationale is that we don"t want a single failure
		to halt processing for everything ... this should be up to an application designer
		to decide what to do in a failure case
		"""
		file_list = self.data["info"]["files"]
		attr_list = []
		for file in file_list:
			try:
				if attr is "length":
					attr_list.append(file[attr])
				else:
					attr_list.append(file[attr][0])
			except KeyError:
				print "No such attr: \"" + attr + "\" for file: " + str(file["path"])

		return attr_list

	def getFileNames(self):
		""" Retrieve the mandatory "path" field for all files listed in the torrent """
		return self.getFileAttrs(attr="path")

	def getFileLengths(self):
		""" Retrieve the mandatory "length" field for all files listed in the torrent.
		The length returned is in bytes
		"""
		return self.getFileAttrs(attr="length")

	def getFileChecksums(self):
		""" Checksums are an optional field of info->file according to the
		torrent spec. If no files have the md5sum attribute, this will raise
		an AttributeError
		"""
		checksums = self.getFileAttrs(attr="md5sum")
		if checksums is []:
			print "no \"md5sum\" attribute available"
			raise AttributeError


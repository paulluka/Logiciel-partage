import string, os

class Crypto:
	def __init__(self, filename, secret):
		self.file = filename
		self.secret = int(secret)
		self.coding_string = string.printable

	def encrypt(self):
		""" Encrypt the document """
		string = self.coding_string
		letter_position = []
		new_letter_position = []
		data_encrypted = ""
		try:
			with open(self.file, 'rb') as f:
				data = f.read()
				data = data.decode()
				f.close()
		except:
			print("Can't open {}".format(self.file))

		for words in data:
			for letter in str(words):
				letter_position.append(string.index(str(letter)))
		for position in letter_position:
			new_position = position + self.secret
			if new_position > len(string):
				new_position = new_position - len(string)
			new_letter_position.append(new_position)
		for position in new_letter_position:
			data_encrypted += string[position]
		with open(self.file, 'wb') as f:
			f.write(data_encrypted.encode())
			f.close()

	def decrypt(self):
		string = self.coding_string
		letter_position = []
		new_letter_position = []
		data_decrypted = ""

		try:
			with open(self.file, 'rb') as f:
				data = f.read()
				data = data.decode()
				f.close()

		except:
			print("Cannot find {}".format(self.file))


		for words in data:
			for letter in str(words):
				letter_position.append(string.index(str(letter)))
		for position in letter_position:
			new_position = position - self.secret
			if new_position < 0:
				new_position = len(string) + new_position
			new_letter_position.append(new_position)
		for position in new_letter_position:
			data_decrypted += string[position]
		with open(self.file, 'wb') as f:
			f.write(data_decrypted.encode())
			f.close()

	def decrypt_string(self):
		string = self.coding_string
		letter_position = []
		new_letter_position = []
		data_decrypted = ""
		data = self.file

		for words in data:
			for letter in str(words):
				letter_position.append(string.index(str(letter)))
		for position in letter_position:
			new_position = position - self.secret
			if new_position < 0:
				new_position = len(string) + new_position
			new_letter_position.append(new_position)
		for position in new_letter_position:
			data_decrypted += string[position]
		return data_decrypted

	def encrypt_string(self):
		string = self.coding_string
		letter_position = []
		new_letter_position = []
		data_encrypted = ""
		data = self.file
		
		for words in data:
			for letter in str(words):
				letter_position.append(string.index(str(letter)))
		for position in letter_position:
			new_position = position - self.secret
			if new_position > len(string):
				new_position = new_position - len(string)
			new_letter_position.append(new_position)
		for position in new_letter_position:
			data_encrypted += string[position]
		return data_encrypted
#!/usr/bin/env python3

from twisted.protocols.basic import LineReceiver
from twisted.internet.protocol import Factory
from twisted.internet import reactor
from twisted.internet import ssl
from OpenSSL import SSL

MAX_USERS = 100
MAX_MSG_LENGTH = 255
MAX_USER_LENGTH = 16
PORT = 8000

class ServerTLSContext(ssl.DefaultOpenSSLContextFactory):
	def __init__(self, *args, **kw):
		kw['sslmethod'] = SSL.TLS1_2_VERSION
		ssl.DefaultOpenSSLContextFactory.__init__(self, *args, **kw)

class ChatProtocol(LineReceiver):
	def __init__(self, factory):
		self.factory = factory
		self.name = None

	def connectionMade(self):
		"""A COMPLETAR POR EL/LA ESTUDIANTE:
		"""
		ftr = "FTR{}\r\n".format(" ".join(self.factory.features.values())).encode()
		self.sendLine(ftr)
		names = ""
		for key in self.factory.users:
			print(names)
			names += "{} ".format(key)
		
		user_list_encoded = 'USR {}\r\n'.format(names).encode()
		print("Sending user list: ", user_list_encoded)
		self.sendLine(user_list_encoded)


	def connectionLost(self, reason):
		"""A COMPLETAR POR EL/LA ESTUDIANTE:
		"""
		print("Connection with {} lost: ".format(self.name), reason)
		for u in self.factory.users:
			if (u!=self.name):
				print("Notifying {} that connection with {} was lost".format(u, self.name))
				self.notifyUserLeft(u, self.name)
		del self.factory.users[self.name]
	def notifyUserLeft(self, user:str, who:str):
		self.factory.users[user].sendLine("OUT{}\r\n".format(who).encode())
	def callLater(self):
		print("Call later")
	def lineReceived(self, line):
		"""A COMPLETAR POR EL/LA ESTUDIANTE:
		"""
		print("Line received: ", line)
		protocol = line[0:3]
		if (protocol == b"NME"):
			user = line[3:].decode().replace("\r\n", "")
			for key in self.factory.users:
				self.factory.users[key].sendLine("INN{}\r\n".format(user).encode())
			self.factory.users[user] = self
			print("User {} added to list".format(user))
			self.name = user
			self.sendLine(b'+\r\n')
		elif (protocol == b"OUT"):
			user = line[3:].decode().replace("\r\n", "")
			print("User {} was disconnected".format(user))
			for u in self.factory.users:
				if (u!=user):
					self.notifyUserLeft(u, user)
			del self.factory.users[user]
		elif (protocol == b"MSG"):
			message = line[3:].replace(b'\r\n', b'').decode()
			msg_letters = message.split(" ")
			new_msg = []
			for word in msg_letters:
				new_word = word
				if word in self.factory.forbidden_words:
					print("Removing forbidden word '{}' from message".format(word))
					word = "#" * len(word)
					new_word = word
				new_msg.append(new_word)
			message = " ".join(new_msg)
			print("Message was sent: ", message)
			for user in self.factory.users:
				if (True):
					self.factory.users[user].sendLine("MSG{} {}\r\n".format(self.name, message).encode())
			self.sendLine(b'+\r\n')
		elif (protocol == b"WRT"):
			user = self.name
			for u in self.factory.users:
				if (u!=user):
					self.factory.users[u].sendLine("WRT{}\r\n".format(user).encode())
		elif (protocol == b'TLS'):
			ctx = ServerTLSContext(
			privateKeyFileName='privkey.key',
			certificateFileName='cert.cert')
			self.transport.startTLS(ctx, self.factory)
			self.sendLine("+\r\n".encode())

class ChatFactory(Factory):
	def __init__(self):
		self.users:dict = {}
		self.features = { 'FILES':'0' , 'CEN':'1', 'NOP':'0', 'SSL':'1' }
		self.forbidden_words = []
		try:
			f = open("forbidden_words.list", "r")
			data = f.readlines()
			for word in data:
				self.forbidden_words.append(word.replace("\n", ""))
			f.close()
			print("Loaded forbidden words: ", self.forbidden_words)
		except Exception as e:
			print("Couldn't open forbidden words' list")

	def buildProtocol(self, addr):
		return ChatProtocol(self)






	

if __name__ == "__main__":
	reactor.listenTCP(PORT, ChatFactory())
	reactor.run()

#!/usr/bin/env python3

from twisted.protocols.basic import LineReceiver
from twisted.internet.protocol import Factory
from twisted.internet import reactor

MAX_USERS = 100
MAX_MSG_LENGTH = 255
MAX_USER_LENGTH = 16
PORT = 8000

class ChatProtocol(LineReceiver):
	def __init__(self, factory):
		self.factory = factory
		self.name = None

	def connectionMade(self):
		"""A COMPLETAR POR EL/LA ESTUDIANTE:
		"""
		print("Connection made: ")
		self.sendLine(b"FTR 0000\r\n")
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
			print("Message was sent: ", message)
			for user in self.factory.users:
				if (user != self.name):
					self.factory.users[user].sendLine("MSG{} {}\r\n".format(self.name, message).encode())
			self.sendLine(b'+\r\n')
class ChatFactory(Factory):
	def __init__(self):
		self.users:dict = {}
		self.features = { 'FILES':'0' , 'CEN':'0', 'NOP':'0', 'SSL':'0' }

	def buildProtocol(self, addr):
		return ChatProtocol(self)

if __name__ == "__main__":
	reactor.listenTCP(PORT, ChatFactory())
	reactor.run()

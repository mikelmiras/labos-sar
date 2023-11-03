#!/usr/bin/env python3

import socket, sys, os, signal
import szasar

PORT = 50000
FILES_PATH = "files"
MAX_FILE_SIZE = 10 * 1 << 20 # 10 MiB
SPACE_MARGIN = 50 * 1 << 20  # 50 MiB
USERS = ("anonimous", "sar", "sza")
PASSWORDS = ("", "sar", "sza")

class State:
	Identification, Authentication, Main, Downloading = range(4)

def sendOK( s, params="" ):
	s.sendall( ("OK{}\r\n".format( params )).encode( "ascii" ) )

def sendER( s, code=1 ):
	s.sendall( ("ER{}\r\n".format( code )).encode( "ascii" ) )

def session( s ):
	state = State.Identification

	while True:
		message = szasar.recvline( s ).decode( "ascii" )
		if not message:
			return

		if message.startswith( szasar.Command.User ):
			if( state != State.Identification ):
				sendER( s )
				continue
			try:
				user = USERS.index( message[4:] )
			except:
				sendER( s, 2 )
			else:
				sendOK( s )
				state = State.Authentication

		elif message.startswith( szasar.Command.Password ):
			if state != State.Authentication:
				sendER( s )
				continue
			if( user == 0 or PASSWORDS[user] == message[4:] ):
				sendOK( s )
				state = State.Main
			else:
				sendER( s, 3 )
				state = State.Identification

		elif message.startswith( szasar.Command.List ):
			if state != State.Main:
				sendER( s )
				continue
			try:
				message = "OK\r\n"
				for filename in os.listdir( FILES_PATH ):
					filesize = os.path.getsize( os.path.join( FILES_PATH, filename ) )
					message += "{}?{}\r\n".format( filename, filesize )
				message += "\r\n"
			except:
				sendER( s, 4 )
			else:
				s.sendall( message.encode( "ascii" ) )

		elif message.startswith( szasar.Command.Download ):
			if state != State.Main:
				sendER( s )
				continue
			filename = os.path.join( FILES_PATH, message[4:] )
			try:
				filesize = os.path.getsize( filename )
			except:
				sendER( s, 5 )
				continue
			else:
				sendOK( s, filesize )
				state = State.Downloading

		elif message.startswith( szasar.Command.Download2 ):
			if state != State.Downloading:
				sendER( s )
				continue
			state = State.Main
			try:
				with open( filename, "rb" ) as f:
					filedata = f.read()
			except:
				sendER( s, 6 )
			else:
				sendOK( s )
				s.sendall( filedata )

		elif message.startswith( szasar.Command.Delete ):
			if state != State.Main:
				sendER( s )
				continue
			if user == 0:
				sendER( s, 7 )
				continue
			try:
				os.remove( os.path.join( FILES_PATH, message[4:] ) )
			except:
				sendER( s, 8 )
			else:
				sendOK( s )
		elif message.startswith(szasar.Command.Upload):
			print("Solicitud de subida de archivo recibida")
			nombre = message[3:]
			print("Archivo solicitado: ", nombre)
			file_path = os.path.join("files", nombre)
			try:
				file_path = open(file_path, "rb")
				file_path.close()
				sendER(s, 9)
				continue
			except Exception as e:
				print(e)
				print("El fichero no existe, se puede subir")
				sendOK(s)
		elif message.startswith( szasar.Command.Exit ):
			sendOK( s )
			return

		else:
			sendER( s )

if __name__ == "__main__":
	s = socket.socket( socket.AF_INET, socket.SOCK_STREAM )

	s.bind( ('', PORT) )
	s.listen( 5 )

	signal.signal(signal.SIGCHLD, signal.SIG_IGN)

	while True:
		dialog, address = s.accept()
		print( "Conexión aceptada del socket {0[0]}:{0[1]}.".format( address ) )
		if( os.fork() ):
			dialog.close()
		else:
			s.close()
			session( dialog )
			dialog.close()
			exit( 0 )

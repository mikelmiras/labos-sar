class Command:
	User, Password, List, Download, Download2, Delete, Exit, Add, Add2 = ("USER", "PASS", "LIST", "DOWN", "DOW2", "DELE", "EXIT", "ADD", "ADD2")

"""
Reads exactly one line of text (delimited by '\r\n') from the socket s and returns it.
"""
def recvline( s, removeEOL = True ):
	line = b''
	CRreceived = False
	while True:
		c = s.recv( 1 )
		if c == b'':
			raise EOFError( "Connection closed by the peer before receiving an EOL." )
		line += c
		if c == b'\r':
			CRreceived = True
		elif c == b'\n' and CRreceived:
			if removeEOL:
				return line[:-2]
			else:
				return line
		else:
			CRreceived = False


"""
Reads exactly size bytes from socket s and returns them.
"""
def recvall(s, size):
    message = b''
    bytes_recd = 0
    

    while bytes_recd < size:
        chunk = s.recv(min(size - bytes_recd, 512))  # Se establece un tamaño máximo de lectura para evitar bloqueos
        if chunk == b'':  # Si no se recibe ningún dato, se sale del bucle
            raise EOFError("Connection closed by the peer before receiving the requested {} bytes.".format(size))
        message += chunk
        print('Mensaje')
        print(message)
        bytes_recd += len(chunk)

    return message


#!/usr/bin/env python3

import socket, sys

PORT = 50008

# Comprueba que se ha pasado un argumento.
if len( sys.argv ) != 2:
	print( "Uso: {} <servidor>".format( sys.argv[0] ) )
	exit( 1 )

"""A COMPLETAR POR EL/LA ESTUDIANTE:
Crear un socket y enviar peticion de conexion al servidor.
"""
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((sys.argv[1], PORT,))
while True:
	print( "Introduce el mensaje que quieres enviar (mensaje vacío para terminar):" )
	mensaje = input()
	if not mensaje:
		break
	print("Enviando el mensaje: ", mensaje)
	mensaje = mensaje.encode()
	s.sendall(mensaje)
	"""A COMPLETAR POR EL/LA ESTUDIANTE:
	Enviar mensaje y recibir 'eco'.
	Mostrar en pantalla lo recibido.
	¡Cuidado! Recuerda que no hay garantías de recibir
	el mensaje completo en una única lectura.
	"""
	print("Esperando respuesta...")
	buffer = b''
	while True:
		buf = s.recv(1024)
		buffer += buf
		if len(buffer) == len(mensaje):
			break
	print("Respuesta recibida: ", buffer.decode())
s.close()

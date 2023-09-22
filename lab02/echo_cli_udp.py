#!/usr/bin/env python3

import socket, sys

PORT = 50007

# Comprueba que se ha pasado un argumento.
if len( sys.argv ) != 2:
	print( "Uso: {} <servidor>".format( sys.argv[0] ) )
	exit( 1 )

"""A COMPLETAR POR EL/LA ESTUDIANTE:
Crear el socket.
"""

UDP_SERVER = sys.argv[1]

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print( "Introduce el mensaje que quieres enviar (mensaje vacío para terminar):" )
while True:
	mensaje = input()
	if not mensaje:
		s.close()
		break
	print("Enviando {} caracteres ({} bytes)".format(len(mensaje), len(mensaje.encode())))
	s.sendto(mensaje.encode(), (UDP_SERVER, PORT))

	resp = s.recv(1024)
	print(resp.decode())
	"""A COMPLETAR POR EL/LA ESTUDIANTE:
	Enviar mensaje y recibir 'eco'.
	Mostrar en pantalla lo recibido.
	"""
"""A COMPLETAR POR EL/LA ESTUDIANTE:
Cerrar socket.
"""
s.close()

#!/usr/bin/env python3

import socket, sys

PORT = 50007

# Comprueba que se ha pasado un argumento.
if len( sys.argv ) == 1:
	print( "Uso: {} <servidor> <puerto>".format( sys.argv[0] ) )
	exit( 1 )

"""A COMPLETAR POR EL/LA ESTUDIANTE:
Crear el socket.
"""
try:
	puerto = int(sys.argv[2])
except:
	puerto = int(input("¿Qué puerto utiliza el servidor UDP?\n"))
UDP_SERVER = sys.argv[1]



s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# print("Iniciado cliente UDP en {}:{}".format())
print( "Introduce el mensaje que quieres enviar (mensaje vacío para terminar):" )
while True:
	mensaje = input()
	if not mensaje:
		s.close()
		break
	if len(mensaje.encode()) > 8:
		print("No puedes enviar mensajes de más de 8 bytes")
		continue
	print("Enviando {} caracteres ({} bytes)".format(len(mensaje), len(mensaje.encode())))
	s.sendto(mensaje.encode(), (UDP_SERVER, puerto))
	print(s.getsockname())

	resp = s.recv(1024)
	print("Respuesta del servidor: ", resp.decode())
	"""A COMPLETAR POR EL/LA ESTUDIANTE:
	Enviar mensaje y recibir 'eco'.
	Mostrar en pantalla lo recibido.
	"""
"""A COMPLETAR POR EL/LA ESTUDIANTE:
Cerrar socket.
"""
s.close()

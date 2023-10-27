#!/usr/bin/env python3

import socket
import os
import signal
PORT = 50007

"""A COMPLETAR POR EL/LA ESTUDIANTE:
Crear un socket, asignarle su dirección y
convertirlo en socket de escucha.
"""
signal.signal(signal.SIGCHLD, signal.SIG_IGN)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', PORT))
s.listen(5)

while True:
	dialogo, direccion = s.accept()
	print("Solicitud recibida desde {}" .format(direccion))

	"""A COMPLETAR POR EL/LA ESTUDIANTE:
	Aceptar peticion de conexion.
	Mientras el cliente no cierre la conexion,
	recibir un mensaje y responder con el mismo.
	Cerrar conexión.
	"""
	if os.fork():
		dialogo.close()
	else:
		print("Creado nuevo proceso para atender la petición: PID {}".format(os.getpid()))
		while True:
			s.close()
			buffer = dialogo.recv(1024)
			if len(buffer) == 0:
				dialogo.close()
				break
			print("[PID {}]Mensaje recibido: ".format(os.getpid()), buffer.decode())
			dialogo.sendall(buffer)
		
		dialogo.close()
		print("Cerrando diálogo")
	
"""A COMPLETAR POR EL/LA ESTUDIANTE:
Cerrar socket de escucha.
"""
print("Cerrando el servidor")
s.close()

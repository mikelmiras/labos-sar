#!/usr/bin/env python3

import socket

PORT = 50007

"""A COMPLETAR POR EL/LA ESTUDIANTE:
Crear un socket y asignarle su direccion.
"""
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

s.bind(("", PORT))
while True:
	"""A COMPLETAR POR EL/LA ESTUDIANTE:
	Recibir un mensaje y responder con el mismo.
	"""
	data, addr = s.recvfrom(1024)
	if data:
		print("Received from {}: " .format(str(addr)) + data.decode())
		s.sendto(data, addr)
"""A COMPLETAR POR EL/LA ESTUDIANTE:
Cerrar socket.
"""

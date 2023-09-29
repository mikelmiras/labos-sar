#!/usr/bin/env python3

import socket, sys

# Mirar servidor DNS en fichero "/etc/resolv.conf"
DNS_DIR = '127.0.0.53'
DNS_PORT = 53

if len( sys.argv ) != 2:
	print( "Uso: python3 {} <Nombre DNS de máquina>".format( sys.argv[0] ) )
	exit( 1 )

nombre_dns = sys.argv[1]

serv_dns = (DNS_DIR, DNS_PORT)

s = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )

"""A COMPLETAR POR EL/LA ESTUDIANTE:
Preparar pregunta DNS
"""
buf = b''
num = 1
# Header section
# # ID
id = 232
buf += id.to_bytes(2, byteorder="big")
# # Flags
buf += b'0000000100000000'
# # QDCOUNT
buf+= num.to_bytes(2, byteorder="big")
# # ANCOUNT
buf += num.to_bytes(2, byteorder="big")
# # NSCOUNT
buf += num.to_bytes(2, byteorder="big")
# # ARCOUNT
buf += num.to_bytes(2, byteorder="big")
len(buf)
# Question section
# # QNAME
domain = "a.root-servers.net"
domain_s = domain.split(".")
name = b''
for part in domain_s:
	name += len(part).to_bytes(1, byteorder="big")
	name += part.encode()


name += b'\x00'

buf += name
num = 1
# # QTYPE. type = A
buf += num.to_bytes(2, byteorder="big")
# # QCLASS. class = IN
buf += num.to_bytes(2, byteorder="big")
# -- Pregunta DNS completa --
print( "Pregunta DNS a enviar:\r\n", buf )
# Enviar pregunta DNS
s.sendto( buf, serv_dns )
# Recibir respuesta
buf = s.recv( 1024 )
print( "Respuesta recibida:\r\n", buf )
"""A COMPLETAR POR EL/LA ESTUDIANTE:
Intrepretar respuesta
"""
exit()
# Header section
# # ID
# # Flags: |QR|   Opcode  |AA|TC|RD|RA|   Z    |   RCODE   |
# #        +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
# # QDCOUNT
# # ANCOUNT
# # NSCOUNT
# # ARCOUNT
# Question section
# # QNAME
# # QTYPE
# # QCLASS
# Answer section: 4.1.3. Resource record format
if not ancount:
	print( 'No se ha recibido ningún registro en la sección de respuestas!' )
else:
	# # NAME (Message compression?)
	# # TYPE
	# # CLASS
	# # TTL: a 32 bit unsigned integer
	# # RDLENGTH: an unsigned 16 bit integer
	# # RDATA
# Authority section: 4.1.3. Resource record format
# Additional section: 4.1.3. Resource record format
	s.close()
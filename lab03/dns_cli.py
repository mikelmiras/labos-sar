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
num = 1
# Header section
# # ID
id = 351
buf = id.to_bytes(2, byteorder="big")
# # Flags
num = 256
buf += num.to_bytes(2, byteorder="big")
num = 1
# # QDCOUNT
buf+= num.to_bytes(2, byteorder="big")
num = 0
# # ANCOUNT
buf += num.to_bytes(2, byteorder="big")
# # NSCOUNT
buf += num.to_bytes(2, byteorder="big")
# # ARCOUNT
buf += num.to_bytes(2, byteorder="big")
# Question section
# # QNAME


print('NOMBRE DNS:  ', nombre_dns)


domain_s = nombre_dns.split(".")
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


print("ENVIADO !! ")

# Recibir respuesta
buf = s.recv( 1024 )

print( "Respuesta recibida:\r\n", buf)
"""A COMPLETAR POR EL/LA ESTUDIANTE:
Intrepretar respuesta
"""






# Header section
# # ID
res_id = int.from_bytes(buf[0:2], 'big')
print(res_id)
# # Flags: |QR|   Opcode  |AA|TC|RD|RA|   Z    |   RCODE   |
# #        +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
# # QDCOUNT	
res_count = int.from_bytes(buf[2:4], 'big')
print(res_count)
# # ANCOUNT
res_ancount = int.from_bytes(buf[4:6], 'big')
print(res_ancount)
# # NSCOUNT
res_ancount = int.from_bytes(buf[6:8], 'big')
print("ANCOUNT: {} ({}) ".format(res_ancount > 0, res_ancount)) # ANCONT determina el número de direcciones IP resueltas. Algunos dominios 
# (por ejemplo los que usan el proxy de cloudflare, suelen tener 2 IP en el registro A)
# # ARCOUNT
ancount = res_ancount
res_arcount = bool(int.from_bytes(buf[8:10], 'big'))

# Question section
# # QNAME

qname = buf[12] 
res_ancount = res_ancount > 0 # Esto es true si el campo ANCOUNT devuelve algo mayor que 0 (lo que implica que ha encontrado registros para el dominio especificado)   

i = 13
print("Question section: ", buf[12:13])

qname_ = ""
while (qname != 0):
	qname = buf[i]
	c = chr(qname)
	if (qname < 97):
		qname_ += "."
	else:
		qname_ += str(c)
	i = i+1

qname_ = qname_[:-1] 
print("QNAME: ", qname_)
# # QTYPE
qtype = int.from_bytes(buf[i:i+2], 'big')
print("QTYPE: ", qtype) 
# # QCLASS
i = i+2
qclass = int.from_bytes(buf[i:i+2], 'big')
print("QCLASS: ", qclass) 
i = i+2 
# Answer section: 4.1.3. Resource record format
if not res_ancount:
	print( 'No se ha recibido ningún registro en la sección de respuestas!' )
else:
	# # NAME (Message compression?)
	p = buf[i]
	n = ""
	while (p!=0):
		n += chr(p)
		i = i+1 
		p = buf[i]
	print("NAME: ", n)  
	# # TYPE
	print("TYPE: ", int.from_bytes(buf[i:i+2], 'big'))
	i = i +2 
	# # CLASS
	print("CLASS: ", int.from_bytes(buf[i:i+2], 'big'))
	# # TTL: a 32 bit unsigned integer
	i = i +2
	print("TTL: ", int.from_bytes(buf[i:i+4], 'big'))
	i = i +4
	# # RDLENGTH: an unsigned 16 bit integer
	print("RDLENGTH: ", int.from_bytes(buf[i:i+2], 'big'))
	# # RDATA
	ip = ""
	ip += str(int.from_bytes(buf[len(buf) - 4 : len(buf) - 3], 'big')) + "."
	ip += str(int.from_bytes(buf[len(buf) - 3 : len(buf) - 2], 'big')) + "."
	ip += str(int.from_bytes(buf[len(buf) - 2 : len(buf) - 1], 'big')) + "."
	ip += str(int.from_bytes(buf[len(buf) - 1 : len(buf)] , 'big'))
	print("Ip completa: ", ip)
# Authority section: 4.1.3. Resource record format
# Additional section: 4.1.3. Resource record format
	s.close()

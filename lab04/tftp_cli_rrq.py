#!/usr/bin/env python3

import sys
import socket
import time

NULL = b'\x00'
RRQ = b'\x00\x01'
WRQ = b'\x00\x02'
DATA = b'\x00\x03'
ACK = b'\x00\x04'
ERROR = b'\x00\x05'

PORT = 50069
BLOCK_SIZE = 512


def get_file(s: socket.socket, serv_addr, filename: str):
    start = time.time()
    buf = b''
    num = 1
    buf += RRQ
    buf += filename.encode("ascii")
    num = 0
    buf += num.to_bytes(1, byteorder='big')
    buf += "octet".encode("ascii")
    buf += num.to_bytes(1, byteorder='big')
    s.sendto(buf, serv_addr)
    print("Enviada solicitud de lectura: ", buf)

    f = open(filename, 'wb')
    """A COMPLETAR POR EL/LA ESTUDIANTE:
	Enviar al servidor la petición de descarga de fichero (RRQ)
	"""

    expected_block = 1
    while True:
        """A COMPLETAR POR EL/LA ESTUDIANTE:
                Recibir respuesta del servidor y comprobar que tiene el código correcto (DATA), si no, terminar.
                Comprobar que el número de bloque es el correcto (expected_block), si no, volver al comienzo del bucle.
                Escribir en el fichero (f) el bloque de datos recibido.
                Responder al servidor con un ACK y el número de bloque correspondiente.
                Si el tamaño del bloque de datos es menor que BLOCK_SIZE es el último, por tanto, salir del bucle.
                Si no, incrementar en uno el número de bloque esperado (expected_block)
                """
        resp = s.recv(BLOCK_SIZE + 4)
        resp_code = resp[0:2]
        block_number = resp[2:4]
        print("Block_number: ", int.from_bytes(block_number, byteorder='big'))
        ACK_ = ACK
        block_number = int.from_bytes(block_number, byteorder='big')
        ACK_ += expected_block.to_bytes(2, byteorder='big')
        s.sendto(ACK_, serv_addr)
        resp_code = int.from_bytes(resp_code, byteorder='big')
        print("Respuesta recibida: ", resp_code)
        if resp_code == 3:
            longitud = len(resp)
            print("Leyendo bloque ", block_number)
            if block_number == expected_block:
                datos = resp[4:longitud - 1]
                f.write(datos)
                expected_block = expected_block + 1

            if longitud < 516:
                print("Archivo leído completamente")
                break
        else:
            print("Error al leer los datos")
            f.close()
            exit()

    f.close()
    elapsed = time.time() - start
    bytes_received = (expected_block - 1) * BLOCK_SIZE + len(datos)
    print('{} bytes received in {:.2e} seconds ({:.2e} b/s).'.format(bytes_received,
          elapsed, bytes_received * 8 / elapsed))


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: {} server filename'.format(sys.argv[0]))
        exit(1)

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serv_addr = (sys.argv[1], PORT)

    get_file(s, serv_addr, sys.argv[2])

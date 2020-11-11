#Cliente:

import socket as sock

#Se crea la conexión TCP para realizar todas las consultas:
direccionServidor = 'localhost'
puertoServidor = 50366
#Se crea el socket del cliente correspondiente:
socketCliente = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
socketCliente.connect((direccionServidor, puertoServidor))
#Se realizan todas las consultas correspondientes, hasta que se ingrese "terminate":
while True:
    consulta = input('Ingrese Consulta: ')
    #Se envía la consulta al servidor:
    socketCliente.send(consulta.encode())
    if consulta == 'terminate':
        break
    #Se recibe el puerto desde el servidor para generar la conexión UDP para recibir la respuesta:
    nuevoPuerto = int(socketCliente.recv(2048).decode())

    #Abro conexión UDP:
    socketClienteUDP = sock.socket(sock.AF_INET,sock.SOCK_DGRAM)
    #Se envía un "OK" al servidor para que proceda a enviar la respuesta a la consulta:
    socketClienteUDP.sendto('OK'.encode(), (direccionServidor,nuevoPuerto))
    #Se recibe la respuesta:
    respuesta,_ = socketClienteUDP.recvfrom(2048)

    #Guardo respuesta en el archivo "{URL}.txt" (se crea un archivo por consulta diferente, y si se repite la consulta 
    #se reescribe el archivo asociado con el nuevo header):
    archivo = open(consulta+'.txt','w')
    archivo.write(respuesta.decode())
    archivo.close()
    #Cierra conexión UDP:
    socketClienteUDP.close()

#Cierra conexión TCP luego de realizar todas las consultas:
socketCliente.close()

# Server:

import socket as sock

#Esta función realiza la consulta HTTP al puerto 80. Lo hace mediante conexión TCP entre el servidor y el servidor 
#de la página de la consulta (el servidor creado por nosotros pasa a ser un cliente):
def consulta_HTTP(url, cache):

    # Se revisa si la consulta está en el caché:
    for i in range(0,len(cache)):
        request, response = cache[i]
        if url == request:
            #Si la consulta está en el caché, se mueve al final de la lista "cache", indicando que se ha accedido 
            #recientemente a esa consulta:
            cache.pop(i)
            cache.append((request,response))
            print("Respuesta obtenida desde caché.")
            return response

    # En caso de que la consulta no esté en el caché se crea una conexión TCP a la url y se hace la consulta GET:
    clientSock = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
    serverAddress = (url, 80)
    clientSock.connect(serverAddress)

    #Se genera la consulta de tipo GET correspondiente:
    requestHeader = 'GET / HTTP/1.1\r\nHost: ' + url + '\r\n\r\n'
    #Se envía la consulta tipo GET:
    clientSock.send(requestHeader.encode())
    # Se recibe la respuesta y se decodifica:
    response = '' 
    recv = clientSock.recv(2048)
    if recv:
        response += recv.decode(encoding="cp437")
    
    #Se extrae el header:
    aux = response.split("\r\n")
    posicion = aux.index("")
    aux = aux[:posicion]
    response= "\n".join(aux)

    #Se guarda la consulta en el caché:
    #Si es que el caché está lleno, se borra el elemento correspondiente, y se agrega la nueva 
    #consulta a la lista "cache":
    if len(cache) == 5:
        cache.pop(0)
    cache.append((url,response))
    
    #Se cierra la conexión y se retorna la respuesta:
    clientSock.close()
    return response
    
    
#Se crea la lista "cache" que manejará el caché mientras el server está en ejecución, es decir, 
#que maneja la persistencia entre clientes:
cache = []  #Una vez que el server deje de ejecutarse, el caché quedará almacenado en el archivo "cache.txt" 
            #para hacerlo persistente entre ejecuciones del servidor.

#Se abre o crea el archivo "cache.txt" para guardar el caché de manera persistente 
#en caso de que el servidor se deje de ejecutar:
try:
    archivo = open("cache.txt","r") 
    lista = archivo.read().split("\n\n")
    #Se guarda la información en el formato de la lista "cache" para manejarlo en cada ejecución del cliente.
    for i in range(0,len(lista)-1,2):
        cache.append((lista[i],lista[i+1]))
    archivo.close()
except IOError: #En caso de que el archivo no exista, lo crea:
    archivo = open("cache.txt","w") 
    archivo.close()

# 49152 - 65535
puerto = 50366

#Se crea el socket del servidor para conexión vía TCP:
socketServidor = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
socketServidor.bind(('', puerto))
#Se comienza a esperar alguna conexión TCP:
while True:
    print("Esperando Cliente...")
    socketServidor.listen(1)
    #Se acepta la conexión y se genera el handshake:
    socketCliente, direccionCliente = socketServidor.accept()
    print("Cliente conectado.")
    #Comienza a esperar las consutas del cliente que se ha conectado:
    while True:
        print("Esperando consulta ...")
        consulta = socketCliente.recv(2048).decode()
        print("Consulta recibida")
        if consulta == 'terminate': #Si se obtiene un "terminate", se finaliza la conexión TCP con el cliente
            print('Ha finalizado la conexión con el cliente.')
            break
        #Se obtiene la respuesta de la consulta del cliente:
        respuesta = consulta_HTTP(consulta, cache)
        
        #Se envían los datos y se genera la conexión UDP:
        socketCliente.send('50367'.encode())
        socketServidorUDP = sock.socket(sock.AF_INET, sock.SOCK_DGRAM)
        socketServidorUDP.bind(('',50367))
        #Se recibe la confirmación "OK" del cliente para enviar la respuesta:
        confirmacion , direccionCliente = socketServidorUDP.recvfrom(2048)
        confirmacion = confirmacion.decode()
        if confirmacion == 'OK': #Se envía la respuesta:
            socketServidorUDP.sendto(respuesta.encode(),direccionCliente)
            print("Respuesta enviada.")
        socketServidorUDP.close()
    #Se cierra el socket del cliente:
    socketCliente.close()
    # Se actualiza el caché almacenado en "cache.txt" cuando un cliente se desconecta:
    archivo = open("cache.txt","w")
    for i in range(len(cache)):
        url , header = cache[i]
        archivo.write(url + "\n\n")
        archivo.write(header +"\n\n")
    archivo.close()
    
socketServidor.close()
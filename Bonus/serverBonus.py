import threading
import socket as sock

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


#Se instancia el candado "lock" utilizado para evitar errores al guardar el caché en el archivo "cache.txt":
lock = threading.Lock()

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

#Se crea la clase "hebra_cliente" que manejará la conexión TCP con cada uno de los clientes,
#y las consultas que cada cliente haga:
class hebra_cliente(threading.Thread):
    #Constructor de la clase:
    def __init__(self, socket):
        threading.Thread.__init__(self)
        self.socketCliente = socket

    def run(self):
        while True:
            print("Esperando consulta ...")
            consulta = self.socketCliente.recv(2048).decode()
            print("Consulta recibida")
            if consulta == 'terminate': #Si se obtiene un "terminate", se finaliza la conexión TCP con el cliente
                print('Ha finalizado la conexión con el cliente.')
                break
            #Se obtiene la respuesta de la consulta del cliente:
            respuesta = consulta_HTTP(consulta, cache)
            
            #Se envían los datos y se genera la conexión UDP:
            self.socketCliente.send('50367'.encode())
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
        self.socketCliente.close()
        
        # Se actualiza el caché almacenado en "cache.txt" cuando un cliente se desconecta:
        #Para esto, lo primero que se hace es asegurar el "lock" para que en ninguna otra hebra se intente 
        #acceder al archivo "cache.txt" mientras esta hebra lo está escribiendo:
        lock.acquire()
        archivo = open("cache.txt","w")
        for i in range(len(cache)):
            url , header = cache[i]
            archivo.write(url + "\n\n")
            archivo.write(header +"\n\n")
        archivo.close()
        #Se libera el "lock" cuando se ha termiando de escribir en el archivo "cache.txt"
        lock.release()

puerto = 50366
#Se crea el socket del servidor para conexión vía TCP:
socketServidor = sock.socket(sock.AF_INET, sock.SOCK_STREAM)

#Para asegurarse de que no haya ningún error cuando cada cliente intente comunicarse "al mismo tiempo" (o en tiempos
#demasiado cercanos) con el socket del servidor, se utiliza "SO_REUSEADDR" que permite que el socket del servidor
#pueda ser usado sin esperar a que expire su tiempo de espera natural si es que está esperando alguna respuesta de algún cliente.
socketServidor.setsockopt(sock.SOL_SOCKET, sock.SO_REUSEADDR, 1)
socketServidor.bind(('', puerto))

#Se comienza a esperar alguna conexión TCP:                      
while True:
    socketServidor.listen(1)
    #Se acepta la conexión y se genera el handshake:
    clientsocket, address = socketServidor.accept()
    print("Se acepta la conexión de: ", address[0],":",address[1])
    #Se crea una hebra con el socket del cliente y luego se ejecuta:
    #Cada vez que se conecte un nuevo cliente, se le asignará una nueva hebra.
    ct = hebra_cliente(clientsocket)
    ct.start()
    
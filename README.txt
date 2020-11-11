Laboratorio 1 - Redes de Computadores
-----------------------------------------
Integrantes:
	* Joaquín Castillo     201773520-1
	* María Paz Morales    201773505-8
-----------------------------------------
Archivo Lab1_Redes.pdf:
Contiene las respuestas de las preguntas de la sección Wireshark y el análisis del Bonus.

Instrucciones de ejecución:

-  Abrir dos terminales
-  En una de las terminales ejecutar el archivo "server.py"
-  En la otra terminal ejecutar el archivo "client.py" 
-  Interactuar con la terminal de usuario ingresando url válidas
-  Si desea terminar la interacción ingresar "terminate" como consulta

** Se creará un archivo {URL}.txt por cada cosulta realizada en el mismo directorio donde se encuentra el archivo "client.py"
** Si es que el cliente consulta por una URL ya consultada, el archivo {URL}.txt correspondiente será reescrito con el nuevo header.
** En la primera ejecución del servidor se creará el archivo "cache.txt" en el mismo directorio de "server.py"
** El archivo "cache.txt" sólo se actualiza cuando un cliente termina su conexión (ingresa "terminate")
** Los clientes son atendidos uno por uno, es decir, un cliente es atendido y cuando se desconceta ingresa el otro.


--------------------------------------------
Ejercicio Bonus: Los archivos correspondientes se encuentran en la carpeta "Bonus".
(El archivo "client.py" es el mismo que el utilizado en la pregunta normal del Laboratorio).

-  Abrir una terminal y ejecutar el archivo "serverBonus.py"
-  Abrir tantas terminales como clientes simultaneos se simularan. En cada una ejecutar el archivo "client.py"
-  Interactuar con la terminal de cada usuario ingrsando url válidos
-  Si desea terminar la interacción de un cliente con el servidor, ingresar "terminate" como consulta del cliente.
 
** Se creará un archivo {URL}.txt por cada cosulta realizada en el mismo directorio donde se ecnuentra el archivo "client.py"
** Si es que el cliente consulta por una URL ya consultada, el archivo {URL}.txt correspondiente será reescrito con el nuevo header.
** En la primera ejecución del servidor se creará el archivo "caché.txt" en el mismo directorio de "serverBonus.py"
** El archivo "cache.txt" sólo se actualiza cuando uno de los clientes termina su conexión (ingresa "terminate")


--------------------------------------------
Consideraciones:

** Sólo se ingresarán url válidas (existentes) por lo que no existe manejo de errores relacionados
** ** Las peticiones GET son del tipo:

				GET / HTTP/1.1
				Host: {URL}

   donde URL es la url consultada
** En caso del Bonus, se asume que cada cliente está en un directorio distinto. Por lo tanto, si dos o más clietes consultan por
   la misma url en el mismo instante (entiendase como que están diferenciadas por un tiempo muy acotado) cada uno escribirá su 
   archivo {URL}.txt en su carpeta evitando así errores al intentar editar un mismo archivo. Cabe destacar que en esta simulación 
   no debería ocurrir algún error de este tipo ya que el proceso es muy rápido y es dificil generar consultas simultáneas.
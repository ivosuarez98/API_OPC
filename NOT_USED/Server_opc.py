import random
import threading
from opcua import Server

# Crear un servidor OPC UA
server = Server()
server.set_endpoint("opc.tcp://192.168.0.95:4840/freeopcua/server/")

# Configurar el espacio de nombres
uri = "http://example.org/ns1"
idx = server.register_namespace(uri)

# Crear un nodo objeto
obj = server.nodes.objects.add_object(idx, "Equipo")

# Crear un nodo variable bajo el objeto
opc_Nombre_Equipo= obj.add_variable (idx,"Nombre de equipo",          "Cocina 1")                 #2  
estado          = obj.add_variable  (idx, "Estado de operacion",      "PRE-calentado")            #3  
temp_poducto    = obj.add_variable  (idx, "Temperatura de producto",  70.50)                      #4
temp_ingreso    = obj.add_variable  (idx, "Temperatura de ingreso",   25.16)                      #5
temp_equipo     = obj.add_variable  (idx, "Temperatura de agua",      85.92)                        #6
temp_chiller     = obj.add_variable (idx, "Temperatura de Chiller",   5.92)                         #7
nivel_agua      = obj.add_variable  (idx, "Nivel de agua",            1150)                         #8
numero_receta          = obj.add_variable  (idx, "Numero Receta",     "1")                          #9
NOMBRE_receta          = obj.add_variable  (idx, "Nombre Receta",     "Jamon 3 estaciones")         #10
Pasos_receta         = obj.add_variable  (idx,"Pasos",4)                                            #11
serp_vapor         = obj.add_variable  (idx,"Vapor serp",True)                                      #12
vivo_vapor         = obj.add_variable  (idx,"Vapor vivo",False)                                     #13
id_alarma         = obj.add_variable  (idx,"id alarma",14)                                          #14
Cantidad_alarma         = obj.add_variable  (idx,"Cantidad Alarma",20)                              #15     #





#receta          = obj.add_variable(idx, "Receta", "Nombre|Cantida de pasos|Corte 1|tiempo o tempartura|Temp agua|Corte 2|tiempo o tempartura|Temp agua|Corte 3|tiempo o tempartura|Temp agua|")


# Iniciar el servidor
server.start()

i=0
try:
    while True:
        i=i+1

finally:
    # Detener el servidor en caso de interrupción
    server.stop()
    server.shutdown()

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

# Crear nodos variables bajo el objeto
opc_Nombre_Equipo = obj.add_variable(idx, "Nombre de equipo", "Cocina 1")
estado = obj.add_variable(idx, "Estado de operacion", 0)
temp_poducto = obj.add_variable(idx, "Temperatura de producto", 70.50)
# Agrega tus otras variables aquí...

# Iniciar el servidor
server.start()

# Función para modificar valores en tiempo real
def modificar_valores():
    while True:
        # Solicitar al usuario que elija una variable para modificar
        print("Seleccione una variable para modificar:")
        print("1. Nombre de equipo")
        print("2. Estado de operacion")
        # Agrega las demás opciones según tus variables...

        opcion = int(input("Opción: "))

        if opcion == 1:
            nuevo_valor = input("Nuevo nombre de equipo: ")
            opc_Nombre_Equipo.set_value(nuevo_valor)
        elif opcion == 2:
            nuevo_valor = input("Nuevo estado de operación: ")
            estado.set_value(nuevo_valor)
        # Agrega las demás condiciones según tus variables...

# Crear un hilo para la función de modificación en tiempo real
hilo_modificacion = threading.Thread(target=modificar_valores)
hilo_modificacion.start()

try:
    while True:
        # Tu lógica principal aquí
        pass

finally:
    # Detener el servidor en caso de interrupción
    server.stop()
    server.shutdown()

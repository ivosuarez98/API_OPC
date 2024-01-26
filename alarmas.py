from opcua import Client
from config import *

from datetime import datetime
#Guardar en datos

class AlarmHandler(object):

    def __init__(self, alarmas_instance):
        self.alarmas_instance = alarmas_instance

    def event_notification(self, event):
        print("New event received:", event)

    def datachange_notification(self, node, val, data):
        print("Evento en",node, val)
        str_node = str(node)
        if "i=" in  str_node:
            try:
                valor_i = int(str_node.split("i=")[1])
                print("El valor de i es:", valor_i)
                
                # Busca el nombre del componente en el diccionario INDX_ALARMA_INV
                nombre_componente = INDX_ALARMA_INV.get(valor_i, None)
                
                if nombre_componente is not None:
                    print(f"ALARMA: {nombre_componente} Estado: {val}")
                    self.alarmas_instance.append(f"ALARMA: {nombre_componente} = {val};{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} ")

                else:
                    print(f"No se encontró un tag para el valor de i={valor_i}")
            except ValueError:
                print("Error al convertir el valor de i a un entero.")


class Alarmas:
    def __init__(self, url):
        self.client = None
        self.server_url = url
        self.nodos_monitoreados = []
        self.alarmas=[]
        self.alarm_handler = AlarmHandler(self.alarmas)
        self.subscription = None
        self.handle = None

    def cargar_nodos(self, index, ns):
        for alarma_id in index:
            print(INDX_ALARMA[alarma_id])
            self.nodos_monitoreados.append(f"ns={ns};i={INDX_ALARMA[alarma_id]}")

    def connect(self):
        try:
            self.client = Client(self.server_url)
            self.client.connect()
            print("Conexión exitosa al servidor OPC")

            # Ahora que la conexión se ha establecido, podemos crear la suscripción.
            subscription_interval = 500  # Intervalo de suscripción en milisegundos
            self.subscription = self.client.create_subscription(subscription_interval, self.alarm_handler)

        except Exception as e:
            print(f"Error en la conexión OPC: {str(e)}")

    def disconnect(self):
        if self.client is not None:
            self.client.disconnect()
            print("Desconexión exitosa del servidor OPC")

    def suscribirce(self):
        for node_path in self.nodos_monitoreados:
            node = self.client.get_node(node_path)
            self.handle = self.subscription.subscribe_data_change(node)
    def Print(self):
        for alarma in self.alarmas:
            print(alarma)
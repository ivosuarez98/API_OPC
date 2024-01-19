from opcua import Client
from dato_opc import Dato_OPC
from datetime import datetime

def Leer_OPC(url,node_index,variables):
    datos_OPC=[]
    print("Leer")

    try:
        client = Client(url)
        client.connect()

        node_list = [client.get_node(node_id) for node_id in node_index]
        values = client.get_values(node_list)

        for i, valor in enumerate(values):
            datos_OPC.append(Dato_OPC(variables[i],datetime.now(),valor))
        client.disconnect()

    except Exception as e:
        print(f"Error en la comunicación OPC: {str(e)}")
    
    return datos_OPC
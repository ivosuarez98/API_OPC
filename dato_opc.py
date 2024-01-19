from opcua import Client
import time
from datetime import datetime
from config import *
class nodo:
    def __init__(self,idx):
        self.Nombre_Equipo_idx          = idx["NombreEquipo"]
        self.Estado_idx                 = idx["Estado"]
        self.Temp_ingreso_idx           = idx["Temperatura de Ingreso"]
        self.Temp_producto_idx          = idx["Temperatura de Producto"]
        self.Temp_equipo_idx            = idx["Temperatura de Agua"]   
        self.Temp_chiller_idx           = idx["Temperatura de Chiller"]      
        self.Nivel_agua_idx             = idx["Nivel de Agua"]        
        self.Nombre_Receta_idx          = idx["Nombre Receta"]
        self.Numero_Receta_idx          = idx["Numero Receta"]
        self.numero_Pasos_idx           = idx["Numero de Pasos"]
        self.Serpentina_Vapor_idx       = idx["Serpentina Vapor"]
        self.Vivo_Vapor_idx             = idx["Vivo Vapor"]
        self.Ciclo_nombre_receta_idx    = idx["Ciclo Nombre de Receta"]
        self.Ciclo_nro_receta_idx       = idx["Ciclo Numero de Receta"]
        self.Cilclo_nro_torres_idx      = idx["Ciclo Numero de torres"]
        self.Ciclo_tipo_fin             = idx["Ciclo Tipo de fin"]
        self.Ciclo_tiempo_tras          = idx["Ciclo Tiempo Transcurrido"]
        self.Ciclo_pausas_totales       = idx["CicloPausas Totales"]


class Dato_OPC:
    def __init__(self,  tiempo, valor):
        self.tiempo = tiempo
        self.valor = valor
    
    def Get_Tiempo(self):
        return self.tiempo    
    
    def Get_Valor(self):
        return self.valor

    
class Equipo:
    def __init__(self,tipo,url,ns, id,index):


        self.server_url         = url
        self.client             = None
        self.tipo               = tipo

        self.NSpace             = ns
        self.id                 = id

        self.nodos              =nodo(index)
        self.nodos_inicio_ciclo_idx    =[  
                                        self.nodos.Estado_idx,
                                        self.nodos.Nombre_Equipo_idx,
                                        self.nodos.Cilclo_nro_torres_idx,
                                        self.nodos.Ciclo_nro_receta_idx,
                                        self.nodos.Ciclo_nombre_receta_idx
                                    ]
        self.nodos_inicio_ciclo        =[
          

                                        ]
        self.valores_inicio_ciclo       ={
                                         
                                        }

        self.nodos_datos_idx        =[  
                                        self.nodos.Temp_equipo_idx,
                                        self.nodos.Temp_producto_idx,
                                        self.nodos.Temp_ingreso_idx,
                                        self.nodos.Temp_chiller_idx,
                                        self.nodos.Nivel_agua_idx,
                                        self.nodos.Vivo_Vapor_idx
                                    ]
        self.nodos_datos            =[]
        
        self.nodos_cierre_ciclo_idx     =[  
                                        self.nodos.Ciclo_pausas_totales,
                                        self.nodos.Ciclo_tiempo_tras,
                                        self.nodos.Ciclo_tipo_fin
                                    ]
        self.nodos_cierre_ciclo        =[]

        self.datos              = {}
        self.arr_historico      = {}

    def connect(self):
        try:
            self.client = Client(self.server_url)
            self.client.connect()
            print("Conexión exitosa al servidor OPC")
        except Exception as e:
            print(f"Error en la conexión OPC: {str(e)}")

    def disconnect(self):
        if self.client is not None:
            self.client.disconnect()
            print("Desconexión exitosa del servidor OPC")
    
    def verificar_conexion(self):
        if self.client.is_connected():
            print("El cliente OPC está conectado.")
        else:
            print("El cliente OPC no está conectado. Intentando conectar...")
            try:
                self.client.connect()
                print("Conexión exitosa.")
            except Exception as e:
                print(f"No se pudo establecer la conexión. Error: {e}")
    
    def agregar_nodos_datos(self):
        for nodo_id in self.nodos_datos_idx:
            try:
                node_id_str = f"ns={self.NSpace};i={nodo_id}"
                nodo_valor = self.client.get_node(node_id_str)
                self.nodos_datos.append(nodo_valor)
                print(f"Nodo '{nodo_id}' agregado correctamente.")
            except Exception as e:
                print(f"Error al agregar nodo '{nodo_id}': {str(e)}")


    def agregar_nodos_cierre_ciclo(self):
        for nodo_id in self.nodos_cierre_ciclo_idx:
            try:
                node_id_str = f"ns={self.NSpace};i={nodo_id}"
                nodo_valor = self.client.get_node(node_id_str)
                self.nodos_cierre_ciclo.append(nodo_valor)
                print(f"Nodo '{nodo_id}' agregado correctamente.")
            except Exception as e:
                print(f"Error al agregar nodo '{nodo_id}': {str(e)}")

    def agregar_nodos_inicio_ciclo(self):
        for nodo_id in self.nodos_inicio_ciclo_idx:
            print(nodo_id)
            try:
                self.nodos_inicio_ciclo.append(f"ns={self.NSpace};i={nodo_id}")


                print(f"Nodo '{nodo_id}' agregado correctamente.")
            except Exception as e:
                print(f"Error al agregar nodo '{nodo_id}': {str(e)}")

    def reed_inicio(self):
        for i, nodo_idx in enumerate(self.nodos_inicio_ciclo_idx):
            nodo_tag = self.client.get_node(f"ns={self.NSpace};i={nodo_idx}")
            value = nodo_tag.get_value()
            self.valores_inicio_ciclo[i] = Dato_OPC(tiempo=datetime.now().strftime("%Y-%m-%d %H:%M"), valor=value)
    
    def read_equipo(self):
        pass

    def read_cierre(self):
        pass

    def read_data(self):
        try:
            if self.client is None :
                self.connect()

            # Filtrar solo los atributos cuyos nombres terminan con '_idx'
            relevant_attributes = [attr for attr in dir(self) if attr.endswith('_idx')]
            
            # Limpiar la lista de nodos antes de la lectura
            self.nodes = []

            for attribute_name in relevant_attributes:
                node_id = getattr(self, attribute_name)
                if node_id is not None:
                    node = self.client.get_node(f"ns={self.NSpace};i={node_id}")
                    self.nodes.append(node)

            # Leer los valores de todos los nodos en una sola llamada
            values = (self.client.get_values(self.nodes))
            self.datos = {attribute_name.replace('_idx', ''): (Dato_OPC(tiempo=datetime.now().strftime("%Y-%m-%d %H:%M"),valor=value)) for attribute_name, value in zip(relevant_attributes, values)}
            
            print(values)
        except Exception as e:
            print(f"Error al leer datos OPC: {str(e)}") 
        finally:
            #self.disconnect()
            pass

    def print(self):
        try:
            for variable_name, value in self.datos.items():
                print(f"{variable_name}: Tiempo={value.Get_Tiempo()}, Valor={value.Get_Valor()}")
        except Exception as e:
            print(f"Error al imprimir datos OPC: {str(e)}")

    def print_inicio(self):
        try:
            print("pase")
            for variable_name, value in self.valores_inicio_ciclo.items():
                print(f"{variable_name}: Tiempo={value.Get_Tiempo()}, Valor={value.Get_Valor()}")
        except Exception as e:
            print(f"Error al imprimir datos OPC: {str(e)}")


    def completar_historicos(self):
        try:
            if (str(self.datos.get("Estado").Get_Valor())!=0):
                for variable_name, value in self.datos.items():
                    if variable_name not in self.arr_historico:
                        self.arr_historico[variable_name] = []
                    self.arr_historico[variable_name].append(value)
        except Exception as e:
            print(f"Error al cargar datos en historico: {str(e)}")

    def print_historicos(self):
        try:
            for variable_name, values in self.arr_historico.items():
                print(variable_name)
                for value in values:
                    print(f"\tTiempo={value.Get_Tiempo()}, Valor={value.Get_Valor()}")
        except Exception as e:
            print(f"Error al imprimir datos en historico: {str(e)}")


    
    
    
    
    def report_home(self):
        return
    
    def report_dato(self):
        try:
            equipo_data = {
                "Nombre Equipo": str(self.datos.get("Nombre_Equipo").Get_Valor()),
                "Componentes": {
                    "s_temp_ingreso": {"value": str(self.datos.get("Temp_ingreso").Get_Valor())},
                    "s_temp_producto": {"value": str(self.datos.get("Temp_producto").Get_Valor())},
                    "s_temp_equipo": {"value": str(self.datos.get("Temp_equipo").Get_Valor())},
                    "s_temp_Chiller": {"value": str(self.datos.get("Temp_equipo").Get_Valor())},
                    "s_temp_equipo": {"value": str(self.datos.get("Temp_equipo").Get_Valor())},
                    "s_temp_equipo": {"value": str(self.datos.get("Temp_equipo").Get_Valor())},
                    "s_temp_equipo": {"value": str(self.datos.get("Temp_equipo").Get_Valor())},
                    "s_temp_equipo": {"value": str(self.datos.get("Temp_equipo").Get_Valor())},
                    "s_temp_equipo": {"value": str(self.datos.get("Temp_equipo").Get_Valor())},

                    "s_nivel_agua": {"value": str(self.datos.get("Nivel_agua").Get_Valor())},
                    "estado": {"value": str(self.datos.get("Estado").Get_Valor())}
        
                },
                "receta": str(self.datos.get("Receta").Get_Valor())
            }

            return equipo_data
        except Exception as e:
            print(f"Error al obtener datos del equipo: {str(e)}")
            return None
    

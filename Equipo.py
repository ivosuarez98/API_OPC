from opcua import Client
from datetime import datetime
from config import *
from DEFINE import *
from sql import*

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

#Guardar en base cuando termina el ciclo idddd

class Dato_OPC:
    def __init__(self,  tiempo, valor):
        self.tiempo = tiempo
        self.valor = valor
    
    def Get_Tiempo(self):
        return self.tiempo    
    
    def Get_Valor(self):
        return self.valor

    
class Equipo:
    def __init__(self,nombre,id,url,ns,index):


        self.server_url         = url
        self.client             = None
        
        self.id                 = id
        self.nombre             = nombre

        self.NSpace             = ns

        self.nodos              =nodo(index)
        #Aca se cargan los indices que se utilizan de lectura unica. 
        self.nodos_inicio_ciclo_idx    =[  
                                        self.nodos.Nombre_Equipo_idx,
                                        self.nodos.Cilclo_nro_torres_idx,
                                        self.nodos.Ciclo_nro_receta_idx,
                                        self.nodos.Ciclo_nombre_receta_idx,
                                        self.nodos.numero_Pasos_idx
                                    ]
        #Aca se almacena los datos de lectura unica.
        self.valores_inicio_ciclo       ={}

        self.nodos_datos_idx        =[  
                                        self.nodos.Estado_idx,
                                        self.nodos.Temp_equipo_idx,
                                        self.nodos.Temp_producto_idx,
                                        self.nodos.Temp_ingreso_idx,
                                        self.nodos.Temp_chiller_idx,
                                        self.nodos.Nivel_agua_idx,
                                        self.nodos.Vivo_Vapor_idx,
                                        self.nodos.Serpentina_Vapor_idx
                                        ]
        self.valores_datos={}
        self.arr_historico      = {}

        self.nodos_cierre_ciclo_idx     =[  
                                        self.nodos.Ciclo_pausas_totales,
                                        self.nodos.Ciclo_tiempo_tras,       #estimar 
                                        self.nodos.Ciclo_tipo_fin
                                    ]
        self.valores_cierre_ciclo={}
        self.datos              = {}
        
        self.con=conectrar_dB(USER_DB,PASS_DB,HOST_DB,DB,PORT)
        self.id_ciclo_DB=None
        
        self.ciclo_ACTIVATE=False
  

    def connect(self):
        try:
            self.client = Client(self.server_url)
            self.client.connect()
            Print_Console(f" OK conexión OPC: Equipo.PY")
            return True
        except Exception as e:
            Print_Console(f"Error en la conexión OPC: {str(e)},Equipo.PY")

    def disconnect(self):
        if self.client is not None:
            try:
                self.client.disconnect()
                Print_Console(f" OK Desconectado OPC: {str(e)},Equipo.PY")
            except Exception as e:
                Print_Console(f" Eror Desconectado OPC: {str(e)},Equipo.PY")

    def reconectar(self):
        Print_Console("Intentando reconectar")
        self.disconnect()
        self.connect()
    
    def reed_inicio(self):
        for i, nodo_idx in enumerate(self.nodos_inicio_ciclo_idx):
            nodo_tag = self.client.get_node(f"ns={self.NSpace};i={nodo_idx}")
            try:
                value = nodo_tag.get_value()
                self.valores_inicio_ciclo[i] = Dato_OPC(tiempo=datetime.now().strftime("%Y-%m-%d %H:%M:%S"), valor=value)
            except Exception as e:
                    error_msj = str(e)
                    if (EXP_NODE_NO_READ in error_msj):
                        self.valores_inicio_ciclo[i] = Dato_OPC(tiempo=datetime.now().strftime("%Y-%m-%d %H:%M:%S"), valor="NULL")
                    else:
                        Print_Console(f"Error Lectura inicio {e}, EQUIPO.py")
                        self.reconectar()
    def read_datos(self):
        for i, nodo_idx in enumerate(self.nodos_datos_idx):
            try:
                nodo_tag = self.client.get_node(f"ns={self.NSpace};i={nodo_idx}")
                value = nodo_tag.get_value()
                self.valores_datos[i] = Dato_OPC(tiempo=datetime.now().strftime("%Y-%m-%d %H:%M:%S"), valor=value)
            except:
                print(f"Nodo invalido, ns={self.NSpace};i={nodo_idx},datos")
                self.valores_datos[i] = Dato_OPC(tiempo=datetime.now().strftime("%Y-%m-%d %H:%M:%S"), valor="NULL")

    def read_cierre(self):
        for i, nodo_idx in enumerate(self.nodos_cierre_ciclo_idx):
            try:
                nodo_tag = self.client.get_node(f"ns={self.NSpace};i={nodo_idx}")
                value = nodo_tag.get_value()
                self.valores_cierre_ciclo[i] = Dato_OPC(tiempo=datetime.now().strftime("%Y-%m-%d %H:%M:%S"), valor=value)
            except:
                #print(f"Nodo invalido, ns={self.NSpace};i={nodo_idx},datos")
                self.valores_cierre_ciclo[i] = Dato_OPC(tiempo=datetime.now().strftime("%Y-%m-%d %H:%M:%S"), valor="NULL")

    def read_node_list_asoacite(self,index,save):
        for i, nodo_idx in enumerate(index):
            nodo_tag = self.client.get_node(f"ns={self.NSpace};i={nodo_idx}")
            try:
                value = nodo_tag.get_value()
                save[i] = Dato_OPC(tiempo=datetime.now().strftime("%Y-%m-%d %H:%M:%S"), valor=value)
            except Exception as e:
                    error_msj = str(e)
                    if (EXP_NODE_NO_READ in error_msj):
                        save[i] = Dato_OPC(tiempo=datetime.now().strftime("%Y-%m-%d %H:%M:%S"), valor="NULL")
                    Print_Console(f"Error Lectura")

    def cargar_en_historico(self):
        self.cargar_tiempo_transcurrido()
        try:
            for variable_nombre,value in self.valores_datos.items():
                #print(variable_nombre)
                if variable_nombre not in self.arr_historico:
                    self.arr_historico[variable_nombre] = []
                self.arr_historico[variable_nombre].append(value)
        except Exception as e:
            Print_Console(f"Error al cargar datos en historico: {str(e)}")

    def get_estado(self):
        return self.valores_datos[0].Get_Valor()

    def send_start_ciclo_db(self):
        if SEND_DATA_BASE==True:
            id_receta=self.valores_inicio_ciclo[2].Get_Valor()
            fecha_receta=self.valores_inicio_ciclo[2].Get_Tiempo()
            estado=self.get_estado()
            self.id_ciclo_DB=cargar_inicio_ciclo(self.id,id_receta,fecha_receta,estado,self.con)
            self.ciclo_ACTIVATE=True
            self.tiempoinicio=datetime.now()

    def send_data_DB(self):
        if SEND_DATA_BASE==True:
            for i in range(len(self.nodos_datos_idx)):
                nombre  = INDX_DATOS_LECTURA_OPC[i]
                cargar_componentes( nombre, self.arr_historico[i],self.id_ciclo_DB,self.con)
            Print_Console(f"Se cargo datos en a la db")

    def is_ciclo_E_activo(self):
        if self.get_estado() !=  (ESTADO_NO_ACTIVO) :
            return True
        return False
    
    def is_ciclo_end(self):
        if self.get_estado() == (ESTADO_FINALIZADO):
            return True
        return False
    
    def limpiar_historico(self):
        self.arr_historico.clear()

    def cargar_tiempo_transcurrido(self):
        ahora = datetime.now()
        self.tiempotranscurrido = str(ahora - self.tiempoinicio)

    def send_cierre_DB(self):
        self.ciclo_ACTIVATE=False
        cerrar_ciclo(self.id_ciclo_DB,self.get_estado(),self.tiempotranscurrido,0,self.con)

    

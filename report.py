from config import *

class Report:
    def __init__(self):
        pass

    def report_dato(self,equipo):
        try:
            equipo_data = {
                            INDX_INICIO_LECTURA_OPC[0]: equipo.nombre,                         
                            "componentes": {
                                                INDX_DATOS_LECTURA_OPC[0]: equipo.valores_datos[0].Get_Valor(),
                                                INDX_DATOS_LECTURA_OPC[3]: equipo.valores_datos[3].Get_Valor(),
                                                INDX_DATOS_LECTURA_OPC[2]: equipo.valores_datos[2].Get_Valor(),
                                                INDX_DATOS_LECTURA_OPC[1]: equipo.valores_datos[1].Get_Valor(),
                                                INDX_DATOS_LECTURA_OPC[4]: equipo.valores_datos[4].Get_Valor(),
                                                INDX_DATOS_LECTURA_OPC[5]: equipo.valores_datos[5].Get_Valor(),
                                                INDX_DATOS_LECTURA_OPC[6]: equipo.valores_datos[6].Get_Valor(),
                                                INDX_DATOS_LECTURA_OPC[7]: equipo.valores_datos[7].Get_Valor(),
                                            },
                                INDX_INICIO_LECTURA_OPC[3]: equipo.valores_inicio_ciclo[3].Get_Valor(),
                                INDX_INICIO_LECTURA_OPC[2]: equipo.valores_inicio_ciclo[2].Get_Valor(),
                                INDX_INICIO_LECTURA_OPC[4]: equipo.valores_inicio_ciclo[4].Get_Valor(),
                                INDEX_CIERRE_LECTURA_OPC[1]: str(equipo.tiempotranscurrido)
                            }

            return equipo_data
        except Exception as e:
            print(f"Error al obtener datos del equipo: {str(e)},En report")
            return None    
        
    def report_grafica(self,equipo,sensor):
        try:
            results = []
            
            max=0
            min=10000000
            # Verificar que el sensor existe en el historial del equipo
            if sensor in INDX_DATOS_LECTURA_OPC:
                # Iterar sobre los valores del sensor y agregarlos a la lista results
                posicion_sensor = INDX_DATOS_LECTURA_OPC.index(sensor)
                for value in equipo.arr_historico[posicion_sensor]:
                    
                    valor=value.Get_Valor()
                    results.append({
                        "value": valor,
                        "time": int(value.Get_Tiempo().timestamp())
                    })
                    if(valor>max):
                        max=valor
                    if(valor<min):
                        min=valor

                # Crear el diccionario de datos_sensor con la información recopilada
                datos_sensor = {
                    "sensor":   sensor,
                    "results":  results,
                    "ULTIMO":   equipo.valores_datos[posicion_sensor].Get_Valor(),
                    "MAX":      max,
                    "MIN":      min
                }
                return datos_sensor
        except Exception as e:
            print(f"Error al generar graficas: {str(e)}")
    
    def report_home(self,equipos):
        result=[]
        for equipo in equipos:
            dato={
                INDX_INICIO_LECTURA_OPC[1]  :   equipo.valores_inicio_ciclo[1].Get_Valor(),
                INDX_INICIO_LECTURA_OPC[0]  :   equipo.nombre,
                INDEX_CIERRE_LECTURA_OPC[1] :   str(equipo.tiempotranscurrido),
                INDX_INICIO_LECTURA_OPC[3]  :   equipo.valores_inicio_ciclo[3].Get_Valor(),
                "ID"                        :   equipo.id,
                INDX_DATOS_LECTURA_OPC[0]   :   equipo.valores_datos[0].Get_Valor(),
                
            }
            result.append(dato)
        return{"Equipos":result}
    
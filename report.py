from config import *

class Report:
    def __init__(self):
        pass

    def report_dato(self,equipo):
        try:
            equipo_data = {
                             INDX_INICIO_LECTURA_OPC[1]: equipo.valores_inicio_ciclo[1].Get_Valor(),
                            "componentes": {
                                                INDX_INICIO_LECTURA_OPC[0]: equipo.valores_inicio_ciclo[0].Get_Valor(),
                                                INDX_DATOS_LECTURA_OPC[2]: equipo.valores_datos[2].Get_Valor(),
                                                INDX_DATOS_LECTURA_OPC[1]: equipo.valores_datos[1].Get_Valor(),
                                                INDX_DATOS_LECTURA_OPC[0]: equipo.valores_datos[0].Get_Valor(),
                                                INDX_DATOS_LECTURA_OPC[3]: equipo.valores_datos[3].Get_Valor(),
                                                INDX_DATOS_LECTURA_OPC[4]: equipo.valores_datos[4].Get_Valor(),
                                                INDX_DATOS_LECTURA_OPC[5]: equipo.valores_datos[5].Get_Valor(),
                                                INDX_DATOS_LECTURA_OPC[6]: equipo.valores_datos[6].Get_Valor(),
                                            },
                                INDX_INICIO_LECTURA_OPC[4]: equipo.valores_inicio_ciclo[4].Get_Valor(),
                                INDX_INICIO_LECTURA_OPC[3]: equipo.valores_inicio_ciclo[3].Get_Valor(),
                                INDX_INICIO_LECTURA_OPC[5]: equipo.valores_inicio_ciclo[5].Get_Valor()
                            }

            return equipo_data
        except Exception as e:
            print(f"Error al obtener datos del equipo: {str(e)},En report")
            return None    
    
    def report_home(self,equipos):
        return 1
    
    def report_grafica(self,equipo,sensor):
        try:
            results = []
            # Verificar que el sensor existe en el historial del equipo
            if sensor in INDX_DATOS_LECTURA_OPC:
                # Iterar sobre los valores del sensor y agregarlos a la lista results
                posicion_sensor = INDX_DATOS_LECTURA_OPC.index(sensor)
                for value in equipo.arr_historico[posicion_sensor]:
                    results.append({
                        "value": value.Get_Valor(),
                        "fecha": value.Get_Tiempo()
                    })

                # Crear el diccionario de datos_sensor con la información recopilada
                datos_sensor = {
                    "sensor": sensor,
                    "results": results
                }
                return datos_sensor
        except Exception as e:
            print(f"Error al generar graficas: {str(e)}")

    def test(self,equipo):
        test_id={
            INDX_INICIO_LECTURA_OPC[0]: equipo.valores_inicio_ciclo[0].Get_Valor()
        }
        return test_id
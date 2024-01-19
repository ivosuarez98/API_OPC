class Report:
    def __init__(self):
        pass

    def report_dato(self,equipo):
        try:
            equipo_data = {
                "Nombre de Equipo": str(equipo.datos.get("Nombre_Equipo").Get_Valor()),
                "componentes": 
                    {
                    "Estado":                   {"value": str(equipo.datos.get("Estado").Get_Valor())},
                    "Temperatura_Ingreso":   {"value": str(equipo.datos.get("Temp_ingreso").Get_Valor())},
                    "Temperatura_Producto":  {"value": str(equipo.datos.get("Temp_producto").Get_Valor())},
                    "Temperatura_Equipo":    {"value": str(equipo.datos.get("Temp_equipo").Get_Valor())},
                    "Temperatura_Chiller":   {"value": str(equipo.datos.get("Temp_chiller").Get_Valor())},
                    "Nivel_agua":            {"value": str(equipo.datos.get("Nivel_agua").Get_Valor())},
                    "Vapor_serpentina":     {"value": str(equipo.datos.get("Serpentina_Vapor").Get_Valor())},
                    "Vapor_Vivo":               {"value": str(equipo.datos.get("Vivo_Vapor").Get_Valor())}
                    },
                "Nombre_Receta":     str(equipo.datos.get("Nombre_Receta").Get_Valor()),
                "Numero_Receta":     str(equipo.datos.get("Numero_Receta").Get_Valor()),
                "Cantida_pasos":     str(equipo.datos.get("numero_Pasos").Get_Valor()),
                "Cantidad_alarmas":  str(equipo.datos.get("numero_alarma").Get_Valor()),
                "ID_ultima_alarma":  str(equipo.datos.get("id_alarma").Get_Valor())
                }
            return equipo_data
        except Exception as e:
            print(f"Error al obtener datos del equipo: {str(e)}")
            return None    
    
    def report_home(self,equipos):
        return 1
    
    def report_grafica(self,equipo,sensor):
        try:
            results = []
            # Verificar que el sensor existe en el historial del equipo
            if sensor in equipo.arr_historico:
                # Iterar sobre los valores del sensor y agregarlos a la lista results
                for value in equipo.arr_historico[sensor]:
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
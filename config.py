
TIME_INTERVAL=3
IP="192.168.0.49"

URL="opc.tcp://192.168.0.140:8080"

INDX_EQUIPO1={
    "URL":                          URL, 
    "NameSpace":                    4,
    "NombreEquipo":                 7,
    "Estado":                       10,
    "Temperatura de Ingreso":       3,
    "Temperatura de Producto":      10,
    "Temperatura de Agua":          10,
    "Temperatura de Chiller":       10,
    "Nivel de Agua":                4,
    "Numero Receta":                11,
    "Nombre Receta":                8,
    "Numero de Pasos":              4,
    "Serpentina Vapor":             4,
    "Vivo Vapor":                   4,
    "Ciclo Nombre de Receta":       5,
    "Ciclo Numero de Receta":       5,
    "Ciclo Numero de torres":       9,
    "Ciclo Tipo de fin":            5,
    "Ciclo Tiempo Transcurrido":    12,
    "CicloPausas Totales":         5
}
INDX_EQUIPO2={
    "URL":                          URL, 
    "NameSpace":                    4,
    "NombreEquipo":                 10,
    "Estado":                       2,
    "Temperatura de Ingreso":       3,
    "Temperatura de Producto":      10,
    "Temperatura de Agua":          10,
    "Temperatura de Chiller":       10,
    "Nivel de Agua":                4,
    "Numero Receta":                4,
    "Nombre Receta":                4,
    "Numero de Pasos":              4,
    "Serpentina Vapor":             4,
    "Vivo Vapor":                   4,
    "Ciclo Nombre de Receta":       5,
    "Ciclo Numero de Receta":       5,
    "Ciclo Numero de torres":       5,
    "Ciclo Tipo de fin":            5,
    "Ciclo Tiempo Transcurrido":    5,
    "CicloPausas Totales":         5
}

INDX_ALARMA={
    "1":          2,
}
INDX_ALARMA_INV = {v: k for k, v in INDX_ALARMA.items()}



#estos indices los uso para convertir los indices fijos de las diferentes lecturas
INDX_INICIO_LECTURA_OPC=[
                         "NOMBRE_EQUIPO",       #0
                         "NRO_TORRES",          #1
                         "NRO_RECETA",          #2
                         "NOMBRE_RECETA",       #3
                         "NRO_PASOS"            #4
                         ]      

INDX_DATOS_LECTURA_OPC=[
                        "ESTADO",               #0
                        "TEM_AGUA",             #1
                        "TEMP_PRODUCTO",        #2
                        "TEMP_INGRESO",         #3
                        "TEMP_CHILLER",         #4
                        "NIVEL_AGUA",           #5
                        "VAPOR_VIVO",           #6
                        "VAPOR_SERPENTINA"      #7
                        
                        ]

INDEX_CIERRE_LECTURA_OPC=[
                        "PAUSA_TOTALES",        #0
                        "TIEMPO_TRANSCURRIDO",  #1
                        "TIPO DE FIN"
                        ]
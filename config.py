
TIME_INTERVAL=3
IP="192.168.0.85"

URL="opc.tcp://192.168.0.140:8080"

INDX_EQUIPO1={
    "URL":                          URL, 
    "NameSpace":                    4,
    "NombreEquipo":                 10,
    "Estado":                       4,
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




#estos indices los uso para convertir los indices fijos de las diferentes lecturas
INDX_INICIO_LECTURA_OPC=["ESTADO",              #0
                         "NOMBRE_EQUIPO",       #1
                         "NRO_TORRES",          #2
                         "NRO_RECETA",          #3
                         "NOMBRE_RECETA",       #4
                         "NRO_PASOS"            #5
                         ]      

INDX_DATOS_LECTURA_OPC=["TEM_AGUA",           #0
                        "TEMP_PRODUCTO",        #1
                        "TEMP_INGRESO",         #2
                        "TEMP_CHILLER",         #3
                        "NIVEL_AGUA",           #4
                        "VAPOR_VIVO",           #5
                        "VAPOR_SERPENTINA"      #6
                        
                        ]

INDEX_CIERRE_LECTURA_OPC=[
                        "PAUSA_TOTALES",        #0
                        "TIEMPO_TRANSCURRIDO",  #1
                        "TIPO DE FIN"
                        ]
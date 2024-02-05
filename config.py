
TIME_INTERVAL=3
IP="192.168.0.95"

URL="opc.tcp://192.168.0.140:8080"
#URL="opc.tcp://192.168.0.95:4840/freeopcua/server/"
INDX_EQUIPO1={
    "URL":                          URL, 
    "NameSpace":                    4,#4 numero de equipo 10
    "NombreEquipo":                 8,
    "Estado":                       3,
    "Temperatura de Ingreso":       5,
    "Temperatura de Producto":      6,
    "Temperatura de Agua":          4,
    "Temperatura de Chiller":       6,
    "Nivel de Agua":                7,
    "Numero Receta":                9,
    "Nombre Receta":                13,
    "Numero de Pasos":              15,#agragar
    "Serpentina Vapor":             11,
    "Vivo Vapor":                   12,#Repetido
    "Ciclo Nombre de Receta":       13,#Repetido
    "Ciclo Numero de Receta":       9,
    "Ciclo Numero de torres":       14,#numero 
    "Ciclo Tipo de fin":            5,
    "Ciclo Tiempo Transcurrido":    16,
    "CicloPausas Totales":          16
}
INDX_EQUIPO2={
    "URL":                          URL, 
    "NameSpace":                    4,
    "NombreEquipo":                 2,
    "Estado":                       3,
    "Temperatura de Ingreso":       4,
    "Temperatura de Producto":      4,
    "Temperatura de Agua":          4,
    "Temperatura de Chiller":       4,
    "Nivel de Agua":                4,
    "Numero Receta":                4,
    "Nombre Receta":                4,
    "Numero de Pasos":              4,
    "Serpentina Vapor":             4,
    "Vivo Vapor":                   4,
    "Ciclo Nombre de Receta":       4,
    "Ciclo Numero de Receta":       4,
    "Ciclo Numero de torres":       4,
    "Ciclo Tipo de fin":            4,
    "Ciclo Tiempo Transcurrido":    4,
    "CicloPausas Totales":          4
}

INDX_ALARMA={
    "1":          10,
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
                        "TEMP_AGUA",             #1
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
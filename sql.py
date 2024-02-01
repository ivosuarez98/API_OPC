import mysql.connector
from datetime import datetime
from DEFINE import *

def conectrar_dB(user,pasw,host,db,port):
    try:
        conexion = mysql.connector.connect(user=user, password=pasw, host=host, database=db, port=port)
        Print_Console("Conectado a la base de datos")
        return conexion
    except:
        Print_Console("Error al conectar a la db")

def cargar_inicio_ciclo(id_equipo,id_receta,fecha_inicico,estado,conexion):

    print(f"{id_equipo}:{type(id_equipo)},  {id_receta}:{type(id_receta)},{fecha_inicico}:{type(fecha_inicico)},{estado}:{type(estado)}")
    Print_Console("INICIO_BASE")

    cursor = conexion.cursor()
    consulta_insert = """
                        INSERT INTO ciclo (id_equipo, id_receta, fecha_inicio, estado)
                        VALUES (%s, %s, %s, %s)
                    """
    
    valores_insert = (id_equipo, id_receta, fecha_inicico, estado)
    print("quilmbo")
    cursor.execute(consulta_insert, valores_insert)
    last_id = cursor.lastrowid
    conexion.commit()
    cursor.close()
    return last_id

def cargar_componentes(nombre_SENS, datos, id_ciclo, conexion):
    cursor = conexion.cursor()
    print("entre")
    # Parte de la consulta SQL
    consulta_inicio = f"""
        INSERT INTO {nombre_SENS} (valor, fecha, id_ciclo)
        VALUES
    """

    # Valores para insertar
    valores_insert = []
    for dato in datos:
        valor = float(dato.Get_Valor())
        tiempo = "24/1/30 19:19"
        valores_insert.append(f"({valor}, '{tiempo}', {int(id_ciclo)})")

    # Unir las partes en una consulta final
    consulta_final = f"{consulta_inicio} {', '.join(valores_insert)}"
    print(consulta_final)
    cursor.execute(consulta_final)
    conexion.commit()
    cursor.close()



def desconectar_dB(conexion):
    conexion.close()




"""

con=conectrar_dB()

datos_a_insertar=[]

for i in range(7000) :
    datos_a_insertar.append(Dato_OPC("24/1/29 19:19", i))

nombre_SENS =   "TEMP_AGUA"
estado      =   "OPERATIVO" 

id_ciclo=cargar_inicio_ciclo(1,1,"24/1/30 19:19",con)

cargar_componentes(nombre_SENS,datos_a_insertar, id_ciclo, estado, con)

#print(leer_indice_ciclo("1",con))   

desconectar_dB(con)
"""
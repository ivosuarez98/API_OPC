import mysql.connector
from datetime import datetime
from DEFINE import *

"""
Conectar a la base de datos
"""
def conectrar_dB(user,pasw,host,db,port):
    try:
        conexion = mysql.connector.connect(user=user, password=pasw, host=host, database=db, port=port)
        Print_DB("Conectado a la base de datos")
        return conexion
    except:
        Print_DB("Error al conectar a la db")

def verificar_conexion(conexion):
    if conexion.is_connected():
        return True
    Print_DB("ERROR En la reconecxion de la base de datos ")
    return False



"""
Cargar el ciclo a la base de datos y devuelve el indice
"""
def cargar_inicio_ciclo(id_equipo,id_receta,fecha_inicico,estado):
    
    conexion=conectrar_dB(USER_DB,PASS_DB,HOST_DB,DB,PORT)
    if verificar_conexion(conexion)==False:
        print("Fallo en la conecion")
        pass    
    try:
        cursor = conexion.cursor()
        consulta_insert = """
                            INSERT INTO ciclo (id_equipo, id_receta, fecha_inicio, estado_inicio)
                            VALUES (%s, %s, %s, %s)
                        """
        valores_insert = (id_equipo, id_receta, fecha_inicico, estado)
        cursor.execute(consulta_insert, valores_insert)
        last_id = cursor.lastrowid
        conexion.commit()
        cursor.close()
        Print_DB("CARGAR inicio de ciclo")
        return last_id
    except  Exception as e :
        Print_DB(f"Fallo al cargar INICIO de ciclo: {str(e)}")
    finally: 
        desconectar_dB(conexion)

"""
Cargar los componentes 
"""
def cargar_componentes(nombre_SENS, datos, id_ciclo):
    conexion=conectrar_dB(USER_DB,PASS_DB,HOST_DB,DB,PORT)
    if verificar_conexion(conexion)==False:
        print("Fallo en la conecion")
        pass
    try:
        cursor = conexion.cursor()
        consulta_inicio = f"""
            INSERT INTO c_{nombre_SENS} (valor, fecha, id_ciclo)
            VALUES
        """
        valores_insert = []
        for dato in datos:
            valor = float(dato.Get_Valor())
            tiempo = str(dato.Get_Tiempo())
            valores_insert.append(f"({valor}, '{tiempo}', {int(id_ciclo)})")
        consulta_final = f"{consulta_inicio} {', '.join(valores_insert)}"
        cursor.execute(consulta_final)
        conexion.commit()
        cursor.close()
        Print_DB("CARGAR Componentes OK")
    except Exception as e:
        Print_DB("fallo al cargar Componentes")
        print(f"error en cargar lso componentes a la db: {str(e)} ")
    finally: 
        desconectar_dB(conexion)

def cerrar_ciclo(id_ciclo,estado,tiempo,cant_pausas):
    conexion=conectrar_dB(USER_DB,PASS_DB,HOST_DB,DB,PORT)
    if verificar_conexion(conexion)==False:
        print("Fallo en la conecion")
        pass  
    try:
        cursor=conexion.cursor()
        cierre = """
                    INSERT INTO cierre (id_ciclo, estado_fin,tiempo,cant_p)
                    VALUES (%s,%s,%s,%s)                    
                """
        Valores=(id_ciclo,estado,tiempo,cant_pausas)
        cursor.execute(cierre,Valores)
        conexion.commit()
        cursor.close()
        Print_DB("Se genero el cierre de un ciclo")
    except Exception as e :
        Print_DB(f"Error en el cierre de ciclo{str(e)}")
    finally: 
        desconectar_dB(conexion)

def desconectar_dB(conexion):
    conexion.close()



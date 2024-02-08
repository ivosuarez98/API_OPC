import mysql.connector
import pandas as pd

from flask import send_file
import io
USER_DB = 'root'
PASS_DB = ''
HOST_DB = 'localhost'
DB = 'dato'
PORT = '1010'
IP="192.168.0.95"

CONSOLE_DB_ACTIVE = True


def Print_DB(str):
    print(str) if CONSOLE_DB_ACTIVE else None


def conectar_DB(user, pasw, host, db, port):
    try:
        conexion = mysql.connector.connect(user=user, password=pasw, host=host, database=db, port=port)
        Print_DB("Conectado a la base de datos")
        return conexion
    except:
        Print_DB("Error al conectar a la db")


def consultar_id_ciclo(fecha_inicial, fecha_final, equipo, con):
    conn = con
    cursor = conn.cursor()

    try:
        # Consulta SQL
        consulta = """
            SELECT id_ciclo, estado_inicio, id_receta
            FROM ciclo
            WHERE id_equipo = %s
              AND (estado_inicio = 1 OR estado_inicio = 2)
              AND Fecha_inicio BETWEEN %s AND %s
            GROUP BY id_ciclo, estado_inicio, id_receta;
        """

        # Ejecución de la consulta
        cursor.execute(consulta, (equipo, fecha_inicial, fecha_final))

        # Obtención de los resultados
        resultados = cursor.fetchall()
        return resultados
    except Exception as e:
        print(f"Error:{str(e)}")
    finally:
        # Cierre de la conexión
        cursor.close()

def consultar_id_ciclo_cierre(id_ciclo, con):
    conn = con
    cursor = conn.cursor()

    try:
        # Consulta SQL
        consulta_combinada = f"""
        SELECT id_ciclo, estado_Fin, cant_t,cant_p,tiempo
        FROM cierre
        WHERE id_ciclo IN ({', '.join(map(str, id_ciclo))})
        GROUP BY id_ciclo, cant_t, estado_Fin;
        """

        cursor.execute(consulta_combinada)
        resultados_combinados = cursor.fetchall()
        return resultados_combinados

    except Exception as e:
        print(f"Error:{str(e)}")
    finally:
        # Cierre de la conexión
        cursor.close()
    
def consultar_pesos(con):
    conn = con
    cursor = conn.cursor()

    try:
        # SQL
        consulta_combinada = f"""
        SELECT id_receta,peso_t
        FROM recetas
        """

        cursor.execute(consulta_combinada)
        resultados_combinados = cursor.fetchall()
        return resultados_combinados

    except Exception as e:
        print(f"Error:{str(e)}")
    finally:
        # Cierre de la conexión
        cursor.close()
def ver_ciclos(fecha_inicial, fecha_final, equipo,con):
   pass

def procesar_datos(ciclos,cierre_ciclos,peso):
    JORNADA=8
    tiempo_uso=0
    ESTADO_OPERATIVO=2
    FINALIZADO_OK=6
    cantidad_inicio_op=0
    cantidad_inicio_op_fin_ok=0
    cantidad_ciclos=len(ciclos)

    id_operativos=[]
    id_operativos_fin_ok=[]
    cantidad_ciclos_por_receta=[0]*31
    cantidad_torres_receta=[0]*31
    for  ciclo in ciclos:
        for cierre_ciclo in cierre_ciclos:
            if ciclo[0]==cierre_ciclo[0]:
                tiempo_uso+=int(cierre_ciclo[4].seconds)
                if ciclo[1]==ESTADO_OPERATIVO :
                    cantidad_inicio_op+=1
                    id_operativos.append(ciclo[0])

                    if cierre_ciclo[1]==FINALIZADO_OK:
                        cantidad_inicio_op_fin_ok+=1
                        id_operativos_fin_ok.append(ciclo[0])
                        cantidad_ciclos_por_receta[ciclo[2]]+=cierre_ciclo[2]
                        cantidad_torres_receta[ciclo[2]]+=1

    tiempo_uso=tiempo_uso/3600


    print(f"% Ciclos Realizados correctamente: {cantidad_inicio_op_fin_ok}/{cantidad_inicio_op}  {(cantidad_inicio_op_fin_ok/cantidad_inicio_op)*100}%")
    print(f"% uso de equipo{tiempo_uso}/{JORNADA}  {(tiempo_uso/JORNADA)*100}%")
    for i, receta  in enumerate(cantidad_ciclos_por_receta):
        print(f"La receta {i} se ciclo {receta}/{cantidad_inicio_op_fin_ok}  {(receta/cantidad_inicio_op_fin_ok)*100} ")

    pesototal=0
    for  i, torres  in enumerate(cantidad_torres_receta): 
        pesototal+=torres*peso[i][1]

    print(pesototal)
    return cantidad_inicio_op,cantidad_inicio_op_fin_ok,tiempo_uso,cantidad_ciclos_por_receta,pesototal

def get_data(equipo, fecha_inicial, fecha_final, sens, con):
    conn = con
    cursor = conn.cursor()

    try:
        # SQL para obtener id_ciclo
        consulta_id_ciclo = """
            SELECT id_ciclo
            FROM ciclo
            WHERE id_equipo = %s
              AND (estado_inicio = 1 OR estado_inicio = 2)
              AND Fecha_inicio BETWEEN %s AND %s
        """
        cursor.execute(consulta_id_ciclo, (equipo, fecha_inicial, fecha_final))

        id_ciclo_resultado = cursor.fetchall()

        # Convertir la lista de tuplas a una lista de valores
        id_ciclo = list(zip(*id_ciclo_resultado))[0]

        print(id_ciclo)

        # Verificar si hay algún id_ciclo antes de continuar
        if not id_ciclo:
            print("No se encontraron ciclos para los parámetros dados.")
            return None, None

        # SQL para obtener datos de la tabla especificada
        # Utiliza la función 'IN' con la cantidad correcta de marcadores de posición
        marcadores = ', '.join(['%s'] * len(id_ciclo))
        consulta_datos = f"""
            SELECT *
            FROM {sens}
            WHERE id_ciclo IN ({marcadores})
        """
        cursor.execute(consulta_datos, tuple(id_ciclo))

        columnas = [desc[0] for desc in cursor.description]
        data = cursor.fetchall()

        return columnas, data

    except Exception as e:
        print(f"Error: {str(e)}")
        return None, None
    finally:
        # Cierre de la conexión
        cursor.close()
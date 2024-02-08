import mysql.connector

USER_DB = 'root'
PASS_DB = ''
HOST_DB = 'localhost'
DB = 'dato'
PORT = '1010'

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
        """

        # Ejecución de la consulta
        cursor.execute(consulta, (equipo, fecha_inicial, fecha_final))

        # Obtención de los resultados
        resultados = cursor.fetchall()

        # Separar los resultados en dos vectores
        todos_id_ciclo = [[resultado[0],resultado[2]] for resultado in resultados]
        id_ciclo_estado_2 = [resultado[0] for resultado in resultados if resultado[1] == 2]

        return todos_id_ciclo, id_ciclo_estado_2
    except Exception as e:
        print(f"Error:{str(e)}")
    finally:
        # Cierre de la conexión
        cursor.close()
    
    


def tomar_id_ciclo_operativo_finalizado(ciclos_op,con):
    conn=con
    cursor = conn.cursor()
    if ciclos_op:
        try:
            id_ciclos_lista = ciclos_op
            consulta_finalizados_correctamente = """
                SELECT id_ciclo, estado_Fin
                FROM cierre
                WHERE id_ciclo IN ({})
            """

            # Crear la cadena de placeholders para IN en la consulta (evitar SQL injection)
            placeholders = ', '.join(['%s'] * len(id_ciclos_lista))
            consulta_finalizados_correctamente = consulta_finalizados_correctamente.format(placeholders)

            # Ejecución de la consulta para obtener los resultados
            cursor.execute(consulta_finalizados_correctamente, tuple(id_ciclos_lista))
            resultados_finalizados_correctamente = cursor.fetchall()
            resultado = [resultado[0] for resultado in resultados_finalizados_correctamente if resultado[1] == 6]
            return resultado
        except Exception as e:
            Print_DB(f"Error al tomar los id_operativos: {str(e)}")

        finally:
            # Cierre de la conexión
            cursor.close()
    else:
        return None
    
def obtener_cantidad_por_receta(arreglo_id_ciclo, con):
    # Conectar a la base de datos
    conn = con
    cursor = conn.cursor()

    # Asegurarse de que arreglo_id_ciclo sea una lista
    if not isinstance(arreglo_id_ciclo, list):
        arreglo_id_ciclo = [arreglo_id_ciclo]

    placeholders = ', '.join(['%s'] * len(ciclos_op_fin))
    consulta = f"""
    SELECT id_receta , COUNT(*) as cantidad_ciclos
    FROM ciclo
    WHERE id_ciclo IN ({placeholders})
    GROUP BY id_receta
    """

    # Reemplazar los marcadores de posición con los valores de la lista
    consulta_final = consulta % tuple(ciclos_op_fin)
    cursor.execute(consulta_final)
    resultados = cursor.fetchall()

    # Imprimir los resultados

    return resultados



def obtener_horas_uso(id_ciclo,con):
    conn=con
    cursor = conn.cursor()
    placeholders = ', '.join(['%s'] * len(id_ciclo))
    consulta = f"""
        SELECT SUM(tiempo) as tiempo_total
        FROM cierre
        WHERE id_ciclo IN ({placeholders})
    """

    consulta_final = consulta % tuple(id_ciclo)
    cursor.execute(consulta_final)
    resultado = cursor.fetchall()
    return int(resultado[0][0])/3600
    
def obtener_cantidad_torres(id_ciclo,con):
    conn=con
    cursor = conn.cursor()
    placeholders = ', '.join(['%s'] * len(id_ciclo))
    consulta = f"""
        SELECT id_ciclo,cant_t
        FROM cierre
        WHERE id_ciclo IN ({placeholders})
    """

    consulta_final = consulta % tuple(id_ciclo)
    cursor.execute(consulta_final)
    resultados = cursor.fetchall()
    print(resultados)
    return resultados
def obtener_produccion_total(id_ciclo,con):
    conn=con
    cursor = conn.cursor()
    consulta_combinada = f"""
    SELECT id_ciclo, estado_Fin, cant_t
    FROM cierre
    WHERE id_ciclo IN ({', '.join(map(str, id_ciclo))})
    GROUP BY id_ciclo, cant_t, estado_Fin;
    """

    cursor.execute(consulta_combinada)
    resultados_combinados = cursor.fetchall()
    return resultados_combinados
    
    
    
    pass


def interpretar(datos):

    id_ciclos_op_fin_ok=[]
    cant_torres_fin_ok=[]
    for ciclo in datos:
        print(ciclo)
        if ciclo[1]==6:            
            id_ciclos_op_fin_ok.append(ciclo[0])
            cant_torres_fin_ok.append((ciclo[0],ciclo[2]))

    return id_ciclos_op_fin_ok,cant_torres_fin_ok

def obtener_peso_torres(id_receta,con):
    pass




conn = conectar_DB(USER_DB, PASS_DB, HOST_DB, DB, PORT)


# Definición de las fechas y otros criterios
fecha_inicial = '2024-01-01'
fecha_final = '2024-02-08'
equipo = 1
estado = 2

ciclos_recetas, ciclos_op = consultar_id_ciclo(fecha_inicial, fecha_final, equipo, conn)

ciclos = [fila[0] for fila in ciclos_recetas]

print("Todos los id_ciclos op y pre-op:", ciclos)
print("los id_ciclos inicados op:", ciclos_op)

ciclos_op_fin=tomar_id_ciclo_operativo_finalizado(ciclos_op,conn)
resultados=obtener_cantidad_por_receta(ciclos_op_fin,conn)

hs=obtener_horas_uso(ciclos,conn)

print(f"CAntida de ciclos: op finalizados / op iniciados  {len(ciclos_op_fin)/len(ciclos_op)}")

for resultado in resultados:
    id_receta, cantidad_ciclos_RECETA = resultado
    print(f"DE LA Receta:{id_receta}   {cantidad_ciclos_RECETA}/{len(ciclos_op_fin)} ")

print(hs)
cant_t=obtener_cantidad_torres(ciclos_op_fin,conn)
valor=obtener_produccion_total(ciclos_op,conn)

id_ciclos_OK_OP,torres_y_id_ciclo=interpretar(valor)

print(f"La cantidad de ciclos que terminaron ok es {len(id_ciclos_OK_OP)} y son :{id_ciclos_OK_OP}")

print(torres_y_id_ciclo)



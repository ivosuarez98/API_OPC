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
            SELECT id_ciclo, estado
            FROM ciclo
            WHERE id_equipo = %s
              AND (estado = 1 OR estado = 2)
              AND Fecha_inicio BETWEEN %s AND %s
        """

        # Ejecución de la consulta
        cursor.execute(consulta, (equipo, fecha_inicial, fecha_final))

        # Obtención de los resultados
        resultados = cursor.fetchall()

        # Separar los resultados en dos vectores
        todos_id_ciclo = [resultado[0] for resultado in resultados]
        id_ciclo_estado_2 = [resultado[0] for resultado in resultados if resultado[1] == "2"]

        return todos_id_ciclo, id_ciclo_estado_2

    finally:
        # Cierre de la conexión
        cursor.close()
      



conn = conectar_DB(USER_DB, PASS_DB, HOST_DB, DB, PORT)
cursor = conn.cursor()

# Definición de las fechas y otros criterios
fecha_inicial = '2024-01-01'
fecha_final = '2024-02-06'
equipo = 1
estado = 2

ciclos, ciclos_op = consultar_id_ciclo(fecha_inicial, fecha_final, equipo, conn)

print("Todos los id_ciclo:", ciclos)
print("Id_ciclo con estado 2:", ciclos_op)

cursor = conn.cursor()
if ciclos_op:
    try:
        # Crear una lista de id_ciclo para la consulta de finalizados_correctamente
        id_ciclos_lista = ciclos_op
        print("hola")
        # Consulta SQL para obtener los ciclos que finalizaron correctamente
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

        print(len(resultados_finalizados_correctamente))
        print(len(ciclos_op))

        # Imprimir los resultados
        for resultado in resultados_finalizados_correctamente:
            id_ciclo = resultado[0]
            estado_fin = resultado[1]
            print(f'El ciclo con id_ciclo {id_ciclo} finalizó con estado {estado_fin}.')

    finally:
        # Cierre de la conexión
        cursor.close()
        conn.close()
else:
    print("No hay ciclos que cumplan con los criterios especificados.")











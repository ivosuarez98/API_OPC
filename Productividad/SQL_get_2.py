
import pandas as pd
from flask import Flask, jsonify
from flask_cors import CORS,cross_origin

from sql_consultas import *

app = Flask(__name__)
CORS(app)   

USER_DB = 'root'
PASS_DB = ''
HOST_DB = 'localhost'
DB = 'dato'
PORT = '1010'
IP="192.168.0.95"

CONSOLE_DB_ACTIVE = True

@cross_origin
@app.route('/productividad/<equipo>/<fecha_inicial>/<fecha_final>', methods=['GET'])
def consultar_productividad(fecha_inicial, fecha_final, equipo):
    try:
        json_data={}
        conn = conectar_DB(USER_DB, PASS_DB, HOST_DB, DB, PORT)
        ciclos = consultar_id_ciclo(fecha_inicial, fecha_final, equipo, conn)
        id_ciclos= list(zip(*ciclos))[0]
        cierre_ciclos=consultar_id_ciclo_cierre(id_ciclos,conn) 
        
        peso=consultar_pesos(conn)
        cantidad_inicio_op,cantidad_inicio_op_fin_ok,tiempo_uso,cantidad_ciclos_por_receta,pesototal=procesar_datos(ciclos,cierre_ciclos,peso)
        json_data={ 
                "ciclos_correctos": cantidad_inicio_op_fin_ok,
                "ciclos_totales": cantidad_inicio_op,
                "uso_equipo":tiempo_uso,
                "pesototal":pesototal,
                "recetas": cantidad_ciclos_por_receta
                }

        print(json_data)
        conn.close()

        return json_data

    except Exception as e:
        return ({"error": f"Error al consultar datos: {str(e)}"})
    
@cross_origin
@app.route('/data/<equipo>/<fecha_inicial>/<fecha_final>/<sens>', methods=['GET'])
def consultar_datos(fecha_inicial, fecha_final, equipo, tag):
    try:
        conn = conectar_DB(USER_DB, PASS_DB, HOST_DB, DB, PORT)
        columnas, data = get_data(equipo, fecha_inicial, fecha_final, tag, conn)
        conn.close()

        if columnas is None or data is None:
            return "No se encontraron datos para los parámetros dados."

        df = pd.DataFrame(data, columns=columnas)

        # Guardar el DataFrame como un archivo Excel en memoria
        excel_data = io.BytesIO()
        df.to_excel(excel_data, index=False)
        excel_data.seek(0)

        # Devolver el archivo como una respuesta para descargar
        return send_file(
            excel_data,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=f'resultado_{tag}.xlsx'
        )

    except Exception as e:
        print(f"Error al consultar datos: {str(e)}")
        return f"Error al consultar datos: {str(e)}"

if __name__ == '__main__':
    
    app.run(host=IP, debug=True, use_reloader=False, port=5001)
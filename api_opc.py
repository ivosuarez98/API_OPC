import threading
import time
from datetime import datetime
from Equipo import *
from report import *
from flask import Flask, jsonify
from config import *
import time
from alarmas import *
from flask_cors import CORS,cross_origin

flag_READ_OPC=False
HILO_TIMER=True

app = Flask(__name__)
CORS(app)                               #cors es una problema que se presento al leer los datos desde otra api 

Equipos={"Cocina1": 1, "Enfriador1": 2,}#NS

Equipo1=Equipo("Cocina",
              url=INDX_EQUIPO1["URL"],
              ns=INDX_EQUIPO1["NameSpace"],
              id=1,
              index=INDX_EQUIPO1
              )
Equipo1.connect()
   
def timer():
    while True:
        try:
            Equipo1.reed_inicio()
            Equipo1.read_datos()
            Equipo1.cargar_en_historico()
            Equipo1.read_cierre()

        except Exception as e:
            print(f"Error al interactuar con Equipo1: {e}")
            print("Equipo no disponible")
        time.sleep(TIME_INTERVAL)

t = threading.Thread(target=timer)
t.start()

#a=Alarmas(URL)
#a.connect()
#a.cargar_nodos(INDX_ALARMA,4)
#a.suscribirce()

r=Report()
"""
Reporte toma un equipo y reporta el estado actual del equipo. 
"""
# Ruta para consultar los últimos valores
@cross_origin
@app.route('/Reporte/<equipo>', methods=['GET'])
def consultar_datos(equipo):
    try:
        json_data = {}
        print(equipo)

        if equipo in Equipos:
            json_data = r.report_dato(Equipo1)  
            print(json_data)

        return (json_data)

    except Exception as e:
        return jsonify({"error": f"Error al consultar datos: {str(e)}"}), 500
"""
Historico toma un sensor y devuelve el historico del ciclo actual.
"""
@cross_origin
@app.route('/Historico/<equipo>/<tag>', methods=['GET'])
def consultar_historicos(equipo,tag):
    try:
        json_data = {}
        print(equipo)

        if equipo in Equipos:
            json_data = r.report_grafica(Equipo1,tag)  
            print(json_data)

        return json_data

    except Exception as e:
        return jsonify({"error": f"Error al consultar datos: {str(e)}"}), 500
"""
Home es por definicion la pagina de inici de la web lo que se realizan es el empquetado 
de todos los equipos en un array y el motodo retira los atributo.
"""
@cross_origin
@app.route('/Home', methods=['GET'])
def consultar_home():
    try:
        #a.Print()
        equipos=[Equipo1,Equipo1]
        json_data = {}
        json_data = r.report_home(equipos)  
        print(json_data)

        return json_data

    except Exception as e:
        return jsonify({"error": f"Error al consultar datos: {str(e)}"}), 500



if __name__ == '__main__':
    app.run(host=IP,debug=True)


#from flask import Flask, jsonify
import threading
import time
from datetime import datetime
import json
from collections import deque
from dato_opc import *
from metodos_GET import *
from report import *
from flask import Flask, jsonify
from config import *
import time

flag_READ_OPC=False
HILO_TIMER=True

app = Flask(__name__)

Equipos={"Cocina1": 1, "Enfriador1": 2,}#NS

Equipo1=Equipo("Cocina",
              url=INDX_EQUIPO1["URL"],
              ns=INDX_EQUIPO1["NameSpace"],
              id=1,
              index=INDX_EQUIPO1
              )
Equipo1.connect()
   
i = 0

def timer():
    global i
    print(i)
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

# Suponiendo que TIME_INTERVAL está definido en algún lugar antes de este código

# Crear el hilo y comenzar el temporizador
t = threading.Thread(target=timer)
t.start()

r=Report()

# Ruta para consultar los últimos valores
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

@app.route('/Home', methods=['GET'])
def consultar_home():
    try:
        equipos=[Equipo1,Equipo1]
        json_data = {}
        json_data = r.report_home(equipos)  
        print(json_data)

        return json_data

    except Exception as e:
        return jsonify({"error": f"Error al consultar datos: {str(e)}"}), 500



if __name__ == '__main__':
    app.run(host=IP,debug=True)


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
HILO_TIMER=False#true

app = Flask(__name__)

Equipos={"Cocina1": 1, "Enfriador1": 2,}#NS

Equipo1=Equipo("Cocina",
              url=INDX_EQUIPO1["URL"],
              ns=INDX_EQUIPO1["NameSpace"],
              id=1,
              index=INDX_EQUIPO1
              )
Equipo1.connect()
   

def timer():
    while HILO_TIMER:
        global flag_READ_OPC
        Equipo1.read_data()
        Equipo1.completar_historicos()
        print("hola")
        time.sleep(TIME_INTERVAL)  
t = threading.Thread(target=timer)
t.start()

Equipo1.reed_inicio()
Equipo1.read_datos()
Equipo1.print_inicio()
#Equipo1.print_data()



r=Report()
print("holas")
print(r.report_dato(Equipo1))


i=0

# Ruta para consultar los últimos valores
@app.route('/Reporte/<equipo>', methods=['GET'])
def consultar_datos(equipo):
    try:
        json_data = {}
        print(equipo)

        if equipo in Equipos:
            json_data = r.report_dato(Equipo1)  
            print(json_data)

        return json_data

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

if __name__ == '__main__':
    app.run(host=IP,debug=True)


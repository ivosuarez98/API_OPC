from  config import *


def consultar_datos(datos_OPC):
    try:
        json_data = {}
        for dato in datos_OPC:
            json_data[dato.nombre]=  {
                "Tiempo":dato.tiempo.strftime("%Y-%m-%d %H:%M:%S"),
                "Valor":dato.valor}
        return json_data

    except Exception as e:
        return ({"error": f"Error al consultar datos: {str(e)}"})
    
##Definir la cantidad de cocinas y enfriadores exitentes 
EQUIPOS={   "Cocina": 1,
            "Enfriador": 1}
    
def Validar_Equipo(equipo,id):
    if equipo in EQUIPOS:
        if id<=EQUIPOS[equipo]:
            return True
    return False
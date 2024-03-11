from Equipo import *
from DEFINE import *
from config import *



def mng(equipo):
    equipo.reed_inicio()
    equipo.read_datos()
    equipo.read_cierre()
    try:
        if equipo.is_ciclo_E_activo():
            if not equipo.ciclo_ACTIVATE and not equipo.is_ciclo_end() :
                equipo.send_start_ciclo_db()
            if not equipo.is_ciclo_end():
                equipo.cargar_en_historico() 
            if equipo.is_ciclo_end() and equipo.ciclo_ACTIVATE:
                print("Datos DB")
                equipo.cargar_en_historico()
                equipo.send_data_DB()
                equipo.send_cierre_DB()
                equipo.limpiar_historico()#limpar el json 
                equipo.tiempotranscurrido=0
        elif equipo.ciclo_ACTIVATE:
            equipo.cargar_en_historico()
            equipo.send_data_DB()
            equipo.send_cierre_DB()
            equipo.limpiar_historico()
            equipo.tiempotranscurrido=0
    except Exception as e:
        Print_Console(f"Error al cargar datos en historico: {str(e)}")

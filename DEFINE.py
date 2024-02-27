
EXP_NODE_NO_READ ="The node id refers to a node that does not exist in the server address space."

CONSOLE_ACTIVE      =       True
CONSOLE_DB_ACTIVE   =       True

SEND_DATA_BASE      =       True

ESTADO_NO_ACTIVO        =       4           #inactivo
ESTADO_ACTIVO           =       2           #OPERATIVO
ESTADO_PRE              =       1           #PRE-OPERATIVO
ESTADO_PAUSA            =       3           #PAUSA
ESTADO_FINALIZADO       =       6           #FINALIZDO
ESTADO_CANCELADO        =       5           #CANCELADO



USER_DB =   'root'
PASS_DB =   '1234'
HOST_DB =   'localhost'
DB      =   'pf_cremona'
PORT    =   '3306'



def Print_Console(srt):
    print(srt) if CONSOLE_ACTIVE else None

def Print_DB(str):
    print(str) if CONSOLE_DB_ACTIVE else None
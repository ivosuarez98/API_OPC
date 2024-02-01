
EXP_NODE_NO_READ ="The node id refers to a node that does not exist in the server address space."

CONSOLE_ACTIVE      =       True

ESTADO_NO_ACTIVO        =       0
ESTADO_ACTIVO           =       1
ESTADO_PRE              =       2
ESTADO_PAUSA            =       3
ESTADO_FINALIZADO       =       4



USER_DB =   'root'
PASS_DB =   ''
HOST_DB =   'localhost'
DB      =   'dato'
PORT    =   '1010'



def Print_Console(srt):
    print(srt) if CONSOLE_ACTIVE else None
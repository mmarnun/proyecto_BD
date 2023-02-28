from funciones import *

db = Conectar_BD("localhost","alex","alex","camiones")
opcion=Menu()
while opcion!=7:
    if opcion==1:
        opcion1(db)
    elif opcion==2:
        opcion2(db)
    elif opcion==3:
        opcion3(db)
    elif opcion==4:
        opcion4(db)
    elif opcion==5:
        opcion5(db)
    elif opcion==6:
        opcion6(db)
    else:
        print("Opción incorrecta.")
    opcion=Menu()
Desconectar_BD(db)
from funciones import *

db = Conectar_BD("localhost","alex","alex","camiones")
opcion=Menu()
while opcion!=0:
    if opcion==1:
        opcion1(db)
    elif opcion==2:
        opcion2(db)
    else:
        print("Opción incorrecta.")
    opcion=Menu()
Desconectar_BD(db)
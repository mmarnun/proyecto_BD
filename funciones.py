import sys
import mysql.connector

def Conectar_BD(host, user, password, database):
    try:
        db = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
    except mysql.connector.Error as e:
        print("No se pudo conectar a la base de datos:", e)
        sys.exit(1)

    print("Conexión correcta.")
    return db

def Desconectar_BD(db):
    db.close()

def Menu():
    menu='''
    Introduce la opción deseada
    1. Listar información de los remolques.
    2. Introduce dos valores de peso y muestra información de los remolques.
    '''
    print(menu)
    while True:
        try:
            opcion=int(input("Opción:"))
            return opcion
        except:
            print("Opción incorrecta, debe ser un número")

def opcion1(db):
    sql="SELECT r.modelo, MAX(r.matricula) AS matricula, MAX(r.peso) AS peso, COUNT(*) AS numero_de_remolques FROM Remolque r GROUP BY r.modelo;"
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        registros = cursor.fetchall()
        for registro in registros:
            print("Modelo:", registro[0], "Matricula:", registro[1], "Peso máximo:", registro[2], "Numero de remolques:", registro[3])
    except:
        print("Error en la consulta")

def opcion2(db):
    min_peso = int(input("Introduce un peso mínima: "))
    max_peso = int(input("Introduce un peso máxima: "))
    if min_peso > max_peso:
        print("Error: el peso mínimo debe ser menor o igual que el máximo.")
        return
    sql="SELECT * FROM Remolque WHERE peso BETWEEN {} AND {}".format(min_peso, max_peso)
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        registros = cursor.fetchall()
        for registro in registros:
            print("Matricula:", registro[0], "Modelo:", registro[1], "Peso:", registro[2], "Codigo del parque:", registro[3])
    except:
        print("Error en la consulta")

def opcion3(db):
    modelo = input("Introduce el modelo del remolque: ")
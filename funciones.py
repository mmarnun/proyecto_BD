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
    3. Introduce el modelo de un remolque y muestra información relacionada.
    4. Insertar nuevo remolque.
    5. Eliminar remolque.
    6. Actualizar capacidad de remolque.
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
    sql="SELECT * FROM Remolque WHERE peso BETWEEN %d AND %d" % (min_peso, max_peso)

    cursor = db.cursor()
    try:
        cursor.execute(sql)
        registros = cursor.fetchall()
        for registro in registros:
            print("Matricula:", registro[0], "Modelo:", registro[1], "Peso:", registro[2], "Codigo del parque:", registro[3])
    except:
        print("Error en la consulta")

def opcion3(db):
    modelo = input("Introduce el modelo de remolque: ")
    sql = "SELECT r.matricula, r.modelo, r.peso, r.codigo_parque, c.tipo_mercancia, f.rango_temperatura FROM Remolque r LEFT JOIN Remolque_Cisterna c ON r.matricula = c.matricula_remolque LEFT JOIN Remolque_Frigorifico f ON r.matricula = f.matricula_remolque WHERE UPPER(r.modelo) = UPPER('%s')" % modelo
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        registros = cursor.fetchall()
        if registros:
            for registro in registros:
                matricula = registro[0]
                modelo = registro[1]
                peso = registro[2]
                codigo_parque = registro[3]
                tipo_mercancia = registro[4]
                rango_temperatura = registro[5]

                if tipo_mercancia:
                    print("Matricula:", matricula, "Modelo:", modelo, "Peso:", peso, "Codigo del parque:", codigo_parque, "Tipo de mercancía:", tipo_mercancia)
                elif rango_temperatura:
                    print("Matricula:", matricula, "Modelo:", modelo, "Peso:", peso, "Codigo del parque:", codigo_parque, "Rango de temperatura:", rango_temperatura)
                else:
                    print("Matricula:", matricula, "Modelo:", modelo, "Peso:", peso, "Codigo del parque:", codigo_parque)

        else:
            print("No se existen remolques con el modelo introducido.")

    except:
        print("Error en la consulta")


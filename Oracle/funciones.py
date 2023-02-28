import sys
import cx_Oracle

def Conectar_BD(host, user, password, database):
    try:
        db = cx_Oracle.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
    except cx_Oracle.Error as e:
        print("No se pudo conectar a la base de datos:", e)
        sys.exit(1)

    print("Conexión correcta a Oracle.")
    return db

def Desconectar_BD(db):
    db.close()

def Menu():
    menu='''
    Introduce la opción deseada
    1. Listar información de los remolques y mostrar el que tiene el mayor peso.
    2. Introduce dos valores de peso y muestra información de los remolques.
    3. Introduce el modelo de un remolque y muestra información relacionada.
    4. Insertar nuevo remolque.
    5. Eliminar remolque.
    6. Actualizar peso de remolque.
    7. Salir
    '''
    print(menu)
    while True:
        try:
            opcion=int(input("Opción:"))
            return opcion
        except:
            print("Opción incorrecta, debe ser un número")

def opcion1(db):
    if db is None:
        print("No se pudo conectar a la base de datos.")
        return

    sql = "SELECT r.modelo, MAX(r.matricula) AS matricula, MAX(r.peso) AS peso, COUNT(*) AS numero_de_remolques FROM Remolque r GROUP BY r.modelo;"
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        registros = cursor.fetchall()
        for registro in registros:
            print("Modelo:", registro[0], "Matrícula:", registro[1], "Peso máximo:", registro[2], "Número de remolques:", registro[3])
    except:
        print("Error en la consulta.")

def opcion2(db):
    min_peso = int(input("Introduce un peso mínimo: "))
    max_peso = int(input("Introduce un peso máximo: "))
    if min_peso > max_peso:
        print("Error: el peso mínimo debe ser menor o igual que el máximo.")
        return
    sql="SELECT * FROM Remolque WHERE peso BETWEEN %d AND %d" % (min_peso, max_peso)

    cursor = db.cursor()
    try:
        cursor.execute(sql)
        registros = cursor.fetchall()
        for registro in registros:
            print("Matrícula:", registro[0], "Modelo:", registro[1], "Peso:", registro[2], "Código del parque:", registro[3])
    except:
        print("Error en la consulta.")

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

def opcion4(db):
    cursor = db.cursor()
    matricula = input("Introduce la matricula del remolque (por ejemplo: 0000AAA): ")
    modelo = input("Introduce el modelo del remolque (debe ser en mayúscula): ")
    peso = input("Introduce el peso del remolque (deber ser mayor que 10000): ")
    codigo_parque = input("Introduce el código del parque: ")
    tipo_remolque = input("¿Qué tipo de remolque es? (CISTERNA, FRIGORIFICO o NORMAL?): ")

    if tipo_remolque == "CISTERNA":
        capacidad = input("Introduce la capacidad de la cisterna (debe ser entre 2000 y 20000): ")
        tipo_mercancia = input("Introduce el tipo de mercancía (PELIGROSO o NO PELIGROSO): ")
        sql = "INSERT INTO Remolque_Cisterna (matricula_remolque, capacidad, tipo_mercancia) VALUES ('%s', '%s', UPPER('%s'))" % (matricula, capacidad, tipo_mercancia)
    elif tipo_remolque == "FRIGORIFICO":
        capacidad = input("Introduce la capacidad del frigorífico (deber ser entre 2000 y 20000): ")
        rango_temperatura = input("Introduce el rango de temperatura (debe ser entre -30 y 10): ")
        sql = "INSERT INTO Remolque_Frigorifico (matricula_remolque, capacidad, rango_temperatura) VALUES ('%s', '%s', '%s')" % (matricula, capacidad, rango_temperatura)
    else:
        capacidad = input("Introduce la capacidad del remolque (debe ser entre 2000 y 20000): ")
        sql = "INSERT INTO Remolque_Normal (matricula_remolque, capacidad) VALUES ('%s', '%s')" % (matricula, capacidad)

    sql2 = "INSERT INTO Remolque (matricula, modelo, peso, codigo_parque) VALUES ('%s', UPPER('%s'), '%s', UPPER('%s'))" % (matricula, modelo, peso, codigo_parque)

    try:
        cursor.execute(sql2)
        cursor.execute(sql)
        db.commit()
        print("Remolque insertado correctamente.")
    except:
        db.rollback()
        print("Error al insertar el remolque.")


def opcion5(db):
    matricula = input("Introduce la matricula del remolque que deseas eliminar: ")
    cursor = db.cursor()
    try:
        sql = "DELETE FROM Remolque_Cisterna WHERE matricula_remolque = '%s'" % matricula
        cursor.execute(sql)
        if cursor.rowcount > 0:
            print("Se ha eliminado la información del remolque en la tabla Remolque Cisterna.")

        sql = "DELETE FROM Remolque_Frigorifico WHERE matricula_remolque = '%s'" % matricula
        cursor.execute(sql)
        if cursor.rowcount > 0:
            print("Se ha eliminado la información del remolque en la tabla Remolque Frigorifico.")

        sql = "DELETE FROM Remolque_Normal WHERE matricula_remolque = '%s'" % matricula
        cursor.execute(sql)
        if cursor.rowcount > 0:
            print("Se ha eliminado la información del remolque en la tabla Remolque Normal.")

        sql = "DELETE FROM Remolque WHERE matricula = '%s'" % matricula
        cursor.execute(sql)
        if cursor.rowcount == 0:
            print("No existe ningún remolque con la matrícula introducida.")
        else:
            print("Se ha eliminado el remolque de la tabla Remolque.")

        db.commit()
        print("Se han eliminado todos los datos relacionados con la matrícula introducida.")

    except:
        db.rollback()
        print("Ha ocurrido un error al intentar eliminar los datos del remolque.")

def opcion6(db):
    matricula = input("Introduce la matrícula del remolque que deseas actualizar: ")
    peso = int(input("Introduce el nuevo peso del remolque: "))
    cursor = db.cursor()
    try:
        sql = "UPDATE Remolque SET peso = %d WHERE matricula = '%s'" % (peso, matricula)
        cursor.execute(sql)
        if cursor.rowcount == 0:
            print("No existe ningún remolque con la matrícula introducida.")
        else:
            print("Se ha actualizado el peso del remolque en la tabla Remolque.")
        db.commit()
    except:
        db.rollback()
        print("Error al intentar actualizar el peso del remolque.")

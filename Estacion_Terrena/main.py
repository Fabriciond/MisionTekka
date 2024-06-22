from almacenamiento import Almacenamiento
from obtencion_de_informacion import obtener_info_del_puerto_serial

import input_info
import serial
import mysql.connector



def main():
    # datos_lanzamiento = input_info.obtener_datos_sobre_lanzamiento()
    # lugar = datos_lanzamiento[0]
    # descripcion = datos_lanzamiento[1]
    # hora = datos_lanzamiento[2]

    nombre_puerto_serial = input_info.obtener_puerto_serial()

    # info_database = input_info.obtener_info_database()
    # usuario = info_database[0]
    # contrasena = info_database[1]

    # db = Almacenamiento(usuario=usuario, contrasena=contrasena)
    # db.guardar_datos_lanzamientos(lugar=lugar, descripcion=descripcion, hora=hora)
    # lanzamiento = db.cursor.lastrowid

    mydb = mysql.connector.connect(
        host="localhost",
        user="",
        password="",
        database="Teeka"
    )
    mycursor = mydb.cursor()

    puerto_serial = serial.Serial(port=nombre_puerto_serial, baudrate=9600)

    while True:
        try:            
            if puerto_serial.in_waiting > 0:
                datos_obtenidos = puerto_serial.readline().decode('utf-8', errors='ignore').rstrip()

                datos = datos_obtenidos.split(',')

                temperatura = None
                presion = None
                altitud = None
                aceleracion_x = None
                aceleracion_y = None
                aceleracion_z = None

                for dato in datos:
                    if dato[0] == 't':
                        temperatura = float(dato.replace('t', ''))
                    if dato[0] == 'p':
                        presion = float(dato.replace('p', ''))
                    if dato[0] == 'a':
                        altitud = float(dato.replace('a', ''))
                    if dato[0] == 'x':
                        aceleracion_x = float(dato.replace('x', ''))
                    if dato[0] == 'y':
                        aceleracion_y = float(dato.replace('y', ''))
                    if dato[0] == 'z':
                        aceleracion_z = float(dato.replace('z', ''))

                datos_separados = [temperatura, presion, altitud, aceleracion_x, aceleracion_y, aceleracion_z]

                print(datos_separados)

                mycursor.execute('insert into suawaka (temperatura, presion, altitud, aceleracion_x, aceleracion_y, aceleracion_z) values (%s, %s, %s, %s, %s, %s)', (temperatura, presion, altitud, aceleracion_x, aceleracion_y, aceleracion_z))
                mydb.commit()

        except Exception as error:
            print(error)


if __name__ == "__main__":
    main()

import getpass
import serial.tools.list_ports as serial_ports

from datetime import datetime


def obtener_info_database():
    print('Accediendo a la base de datos...')
    usuario = input('Ingresa tu usuario: ')
    contrasena = getpass.getpass(prompt='Ingresa tu contrasana: ')

    return (usuario, contrasena)


def obtener_puerto_serial():
    puertos_seriales = serial_ports.comports()

    for indice, puerto in enumerate(puertos_seriales, 1):
        print(f'{indice}: {puerto.device} {puerto.interface}')

    puerto_seleccionado = int(
        input('Ingresa el numero del puerto serial que quieres utilizar: '))

    return puertos_seriales[puerto_seleccionado - 1].device


def obtener_datos_sobre_lanzamiento():
    lugar = input('Ingresa el lugar del lanzamiento: ')
    descripcion = input('Ingresa la descripcion del lanzamiento: ')
    hora = datetime.now()

    return (lugar, descripcion, hora)

import serial


def obtener_info_del_puerto_serial(puerto_serial: serial.Serial):
    try:
        if puerto_serial.in_waiting > 0:
            datos_obtenidos = puerto_serial.readline().decode('utf-8', errors='ignore').rstrip()
            return datos_obtenidos
    except:
        pass

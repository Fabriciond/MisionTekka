import random
import serial
import serial.tools.list_ports as serial_ports


class Communication:
    baudrate = ''
    portName = ''
    dummyPlug = False
    ports = serial_ports.comports()
    ser = serial.Serial()

    def __init__(self):
        self.baudrate = 230400
        for indice, puerto in enumerate(self.ports, 1):
            print(f'{indice}: {puerto.device} {puerto.interface}')
        
        print("the available ports are (if none appear, press any letter): ")
        for port in sorted(self.ports):
            # obtener la lista de puetos: https://stackoverflow.com/a/52809180
            print(("{}".format(port)))
        self.portName = input("write serial port name (ex: /dev/ttyUSB0): ")
        try:
            # puerto_seleccionado = int(
            #     input('Ingresa el numero del puerto serial que quieres utilizar: '))
            # self.portName = self.ports[puerto_seleccionado-1].name
            self.ser = serial.Serial(self.portName, self.baudrate)
        except:
            print("Can't open : ", self.portName)
            self.dummyPlug = True
            print("Dummy mode activated")

    def close(self):
        if (self.ser.isOpen()):
            self.ser.close()
        else:
            print(self.portName, " it's already closed")

    def getData(self):
        value_chain = self.obtener_datos_separados()

        return value_chain

    def isOpen(self):
        return self.ser.isOpen()

    def dummyMode(self):
        return self.dummyPlug

    def activar_servo(self):
        self.ser.write(b'p')
        return 0
        
    def activar_toma_fotografias(self):
        self.ser.write(b't')
        return 0

    def obtener_datos_separados(self):
        try:
            if self.ser.in_waiting > 0:
                datos_obtenidos = self.ser.readline().decode('utf-8', errors='ignore').rstrip()
                print(datos_obtenidos)

                if datos_obtenidos[0] == '1':
                    datos = datos_obtenidos.split(',')
                    mision = None
                    medicion = None
                    tiempo = None
                    temperatura = None
                    presion = None
                    altitud = None
                    aceleracion_x = None
                    aceleracion_y = None
                    aceleracion_z = None
                    aceleracion_angular_x = None
                    aceleracion_angular_y = None
                    aceleracion_angular_z = None
                    latitud = None
                    longitud = None
                    servo_activado = None

                    for dato in datos:
                        try:
                            if dato[0] == '1':
                                mision = '1'
                            elif dato[0] == 'm':
                                medicion = float(dato.replace('m', ''))
                            elif dato[0] == 'j':
                                tiempo = float(dato.replace('j', ''))
                            elif dato[0] == 't':
                                temperatura = float(dato.replace('t', ''))
                            elif dato[0] == 'p':
                                presion = float(dato.replace('p', ''))
                            elif dato[0] == 'a':
                                altitud = float(dato.replace('a', ''))
                            elif dato[0] == 'x':
                                aceleracion_x = float(dato.replace('x', ''))
                            elif dato[0] == 'y':
                                aceleracion_y = float(dato.replace('y', ''))
                            elif dato[0] == 'z':
                                aceleracion_z = float(dato.replace('z', ''))
                            elif dato[0] == 'b':
                                aceleracion_angular_x = float(dato.replace('b', ''))
                            elif dato[0] == 'c':
                                aceleracion_angular_y = float(dato.replace('c', ''))
                            elif dato[0] == 'd':
                                aceleracion_angular_z = float(dato.replace('d', ''))
                            elif dato[0] == 'l':
                                latitud = float(dato.replace('l', ''))
                            elif dato[0] == 'g':
                                longitud = float(dato.replace('g', ''))
                            elif dato[0] == 's':
                                servo_activado = dato.replace('s', '')
                        except:
                            pass

                        datos_separados = [mision, medicion, tiempo, temperatura, presion, altitud,
                                   aceleracion_x, aceleracion_y, aceleracion_z, aceleracion_angular_x, aceleracion_angular_y, aceleracion_angular_z, latitud, longitud, servo_activado]

                elif datos_obtenidos[0] == '2':
                    datos = datos_obtenidos.split(',')
                    mision = None
                    medicion = None
                    tiempo = None
                    altitud = None
                    ppm = None
                    presion = None
                    indice_uv = None
                    temperatura = None
                    humedad = None
                    luz = None
                    toma_fotos = None

                    for dato in datos:
                        try:
                            if dato[0] == '2':
                                mision = '2'
                            elif dato[0] == 'i':
                                medicion = float(dato.replace('i', ''))
                            elif dato[0] == 'j':
                                tiempo = float(dato.replace('j', ''))
                            elif dato[0] == 'u':
                                indice_uv = float(dato.replace('u', ''))
                            elif dato[0] == 't':
                                temperatura= float(dato.replace('t', ''))
                            elif dato[0] == 'h':
                                humedad = float(dato.replace('h', ''))
                            elif dato[0] == 'm':
                                ppm = float(dato.replace('m', ''))
                            elif dato[0] == 'p':
                                presion = float(dato.replace('p', ''))
                            elif dato[0] == 'a':
                                altitud = float(dato.replace('a', ''))
                            elif dato[0] == 'l':
                                luz = float(dato.replace('l', ''))
                            elif dato[0] == 'c':
                                toma_fotos == dato.replace('c', '')
                        except:
                            pass

                        datos_separados = [
                            mision, medicion, tiempo, indice_uv, temperatura, humedad, ppm, presion, altitud, luz, toma_fotos
                        ]
                else:
                    pass

                return datos_separados
        except Exception as e:
            print(f"fallo recepcion de datos {e}")

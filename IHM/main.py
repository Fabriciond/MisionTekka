import sys
from pyqtgraph.Qt import QtGui, QtCore, QtWidgets
import pyqtgraph as pg
from communication import Communication
from PyQt5.QtWidgets import QPushButton
from graphs.graph_acceleration import graph_acceleration
from graphs.graph_altitude import graph_altitude
from graphs.graph_battery import graph_battery
from graphs.graph_gyro import graph_gyro
from graphs.graph_pressure import graph_pressure
from graphs.graph_temperature import graph_temperature
from graphs.graph_uv import graph_uv
from graphs.graph_CO2 import graph_co2
from graphs.graph_humidity import graph_humidity
from graphs.graph_light import graph_light
import pyperclip
# Function to create a window
from map import QGoogleMap

def create_window(title, width, height, isMap=False):
    pg.setConfigOption('background', (33, 33, 33))
    pg.setConfigOption('foreground', (197, 198, 199))
    app = QtWidgets.QApplication(sys.argv)
    if isMap:
        win = QGoogleMap(api_key='AIzaSyDNESuwm02SRod1FSahttV5aw4gWl5lcYc')
    else:
        win = pg.GraphicsLayoutWidget()

    win.setWindowTitle(title)
    win.resize(width, height)
    return app, win

map, w = create_window('Map', 1200, 700, isMap=True)
w.waitUntilReady()
w.setZoom(14)
lat, lng = w.centerAtAddress("Guaymas Mexico")
w.addMarker("MyHome", lat, lng)
if lat is None and lng is None:
    lat, lng = 27.908160, -110.925030
    w.centerAt(lat, lng)
    w.addMarker("MyDragableMark", lat, lng, **dict(
        icon="http://maps.gstatic.com/mapfiles/ridefinder-images/mm_20_red.png",
        draggable=True,
        title="Move me!"
    ))

w.mapMoved.connect(print)
w.mapClicked.connect(print)
w.mapRightClicked.connect(print)
w.mapDoubleClicked.connect(print)

map2, w2 = create_window('Map', 1200, 700, isMap=True)
w2.waitUntilReady()
w2.setZoom(14)
lat, lng = w2.centerAtAddress("Mazatlán Mexico")
w2.addMarker("MyHome", lat, lng)
if lat is None and lng is None:
    lat, lng = 27.908160, -110.925030
    w2.centerAt(lat, lng)
    w2.addMarker("MyDragableMark", lat, lng, **dict(
        icon="http://maps.gstatic.com/mapfiles/ridefinder-images/mm_20_red.png",
        draggable=True,
        title="Move me!"
    ))

w2.mapMoved.connect(print)
w2.mapClicked.connect(print)
w2.mapRightClicked.connect(print)
w2.mapDoubleClicked.connect(print)

app1, win1 = create_window('Flight monitoring 1', 1200, 700)

serial = Communication()
font = QtGui.QFont()
font.setPixelSize(90)

# Declare graphs

# Graficas de suawaka
altitude = graph_altitude()
acceleration = graph_acceleration()
gyro = graph_gyro()
temperature = graph_temperature()

# Graficas de ili
co2_ili = graph_co2()
altitude_ili = graph_altitude()
temperature_ili = graph_temperature()
uv_ili = graph_uv()
humidity_ili = graph_humidity()
graph_light = graph_light()

# Create layouts for the first window
# Create first window

l1 = win1.addLayout(colspan=20, rowspan=2)
l11 = l1.addLayout(colspan=2, rowspan=1, border=(83, 83, 83))

# Altitude, speed
l11.addItem(altitude)
l11.nextCol()
l11.addItem(temperature)
# l11.addItem(speed)
l1.nextRow()

# Acceleration, gyro, pressure, temperature
l12 = l1.addLayout(rowspan=1, border=(83, 83, 83))
l12.addItem(acceleration)
l12.addItem(gyro)
# l12.addItem(pressure)

l1.nextRow()




# -------------buttons---------------
# buttons style
def copiar(lat, lng):
    pyperclip.copy(f"http://www.google.com/maps/place/lat,lng")
style = "background-color:rgb(29, 185, 84);color:rgb(0,0,0);font-size:14px;height:100px"
styleE = "background-color:rgb(255, 0, 0);color:rgb(255,255,255);font-size:14px; height: 100px;"
# Button 1
proxy = QtWidgets.QGraphicsProxyWidget()
save_button = QtWidgets.QPushButton('Ubicacion del VL')
save_button.setStyleSheet(style)
proxy.setWidget(save_button)


# Button 2
proxy2 = QtWidgets.QGraphicsProxyWidget()
end_save_button = QtWidgets.QPushButton('Servo no ha sido activado. Activar')
end_save_button.setStyleSheet(styleE)
#end_save_button.clicked.connect(data_base.stop)
proxy2.setWidget(end_save_button)

# Button Emergency
proxy3 = QtWidgets.QGraphicsProxyWidget()
emergency_buttom = QtWidgets.QPushButton('Toma de fotografias sin activar. Activar')
emergency_buttom.setStyleSheet(styleE)
emergency_buttom.clicked.connect(serial.activar_servo)
proxy3.setWidget(emergency_buttom)


btns, btns_win = create_window("Buttons", 120, 120)


layoutB = btns_win.addLayout(row=1, col=3)
layoutB.addItem(proxy3)
#layoutB.nextCol()
layoutB.addItem(proxy2)
#layoutB.nextCol()
layoutB.addItem(proxy)
#layoutB.addItem(proxy_liberado)
#layoutB.addItem(proxy_toma_fotografias)

# ili
ili, ili_win = create_window('ILI', 1200, 700)

layout_ili = ili_win.addLayout(row=2, col=0)
layout_ili.addItem(co2_ili, colspan=20)
layout_ili.addItem(temperature_ili, colspan=20)
layout_ili.nextRow()
layout_ili.addItem(altitude_ili, colspan=20)
layout_ili.addItem(uv_ili, colspan=20)
layout_ili.nextRow()
layout_ili.addItem(humidity_ili, colspan=20)
layout_ili.addItem(graph_light, colspan=20)


def update():
    try:
        #value_chain = [1, None, 202, 93, 1023, 32, 543, 1,1,2]  # ser.getData()
        value_chain = serial.obtener_datos_separados()
        print(value_chain)

        if value_chain[0] == '1':
            temperature.update(value_chain[1])
            altitude.update(value_chain[3])
            acceleration.update(value_chain[4], value_chain[5], value_chain[6])
            gyro.update(value_chain[7], value_chain[8], value_chain[9])

            if value_chain[13] == '1':
                end_save_button.setText('Servo motor activado')

            save_button.clicked.connect(copiar(value_chain[11], value_chain[12]))

        elif value_chain[0] == '2':
            uv_ili.update(value_chain[3])
            temperature_ili.update(value_chain[4])
            humidity_ili.update(value_chain[5])        
            co2_ili.update(value_chain[6])
            altitude_ili.update(value_chain[8])
            graph_light.update(value_chain[9])

            if value_chain[10] == '1':
                end_save_button.setText('Empezo la toma de fotos')

        archivo = open('flight_data.csv', 'a')
        archivo.write(f"{value_chain}\n")
        archivo.close()

    except IndexError:
        print('starting, please wait a moment')


if (serial.isOpen()) or (serial.dummyMode()):
    timer = pg.QtCore.QTimer()
    timer.timeout.connect(update)
    # Esto lo relentiza
    timer.start(100)
else:
    print("something is wrong with the update call")


# Mostrar las ventanas
win1.show()
ili_win.show()
btns_win.show()
w.show()
w2.show()

# Start Qt event loop unless running in interactive mode.
if __name__ == '__main__':
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        app1.exec_()
        map.exec_()
        map2.exec_()
        ili.exec_()

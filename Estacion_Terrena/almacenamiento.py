import mysql.connector


class Almacenamiento:
    conector_database = None
    cursor = None

    def __init__(this, usuario, contrasena):
        host = 'localhost'
        database = 'Teeka'

        this.conector_database = mysql.connector.connect(
            host=host,
            user=usuario,
            password=contrasena,
            database=database
        )

        this.cursor = this.conector_database.cursor()

    def guardar_datos_lanzamientos(this, lugar, descripcion, hora):
        query = f"INSERT INTO lanzamientos (lugar, descripcion, hora) VALUES ('{lugar}', '{descripcion}', '{hora}')"
        this.cursor.execute(query)
        this.conector_database.commit()

        return this.cursor.lastrowid

    def guardar_datos_sensores_ili(this, tiempo, humedad, temperatura_dht, temperatura_bmp, co2, presion, altitud, indice_uv, id_lanzamiento):
        query = f"INSERT INTO ili (tiempo, humedad, temperatura_dht, temperatura_bmp, co2, presion, altitud, indice_uv, id_lanzamiento) VALUES ('{tiempo}', {float(humedad)}, {float(temperatura_dht)}, {float(temperatura_bmp)}, {float(co2)}, {float(presion)}, {float(altitud)}, {int(indice_uv)}, {int(id_lanzamiento)})"
        this.cursor.execute(query)
        this.conector_database.commit()

    
    def guardar_datos_sensores_suawaka(this, tiempo, temperatura, presion, altitud, aceleracion_x, aceleracion_y, aceleracion_z, id_lanzamiento):
        query = f"INSERT INTO suawaka (tiempo, temperatura, presion, altitud, aceleracion_x, aceleracion_y, aceleracion_z, id_lanzamiento) VALUES ('{tiempo}', {float(temperatura)}, {float(presion)}, {float(altitud)}, {float(aceleracion_x)}, {float(aceleracion_y)}, {float(aceleracion_z)}, {int(id_lanzamiento)})"
        this.cursor.execute(query)
        this.conector_database.commit()


def obtener_datos_separados(cadena_de_datos: str):
    datos = cadena_de_datos.split(',')
    
    for index, dato in enumerate(datos):
        if dato[index] == 't':
            valor = dato[index].replace('t', '')
            temperatura = valor


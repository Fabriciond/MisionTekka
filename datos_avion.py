import csv

archivo_entrada = 'ili_datos_avion copy.csv'
archivo_salida = 'ili_datos_sin_corchetes'

with open(archivo_entrada, 'r') as f_entrada, open(archivo_salida, 'w', newline='') as f_salida:
    lector_csv = csv.reader(f_entrada)
    escritor_csv = csv.writer(f_salida)
    
    for fila in lector_csv:
        fila_sin_corchetes = [elemento.strip('[]') for elemento in fila]
        
        escritor_csv.writerow(fila_sin_corchetes)

print("Corchetes eliminados con éxito.")

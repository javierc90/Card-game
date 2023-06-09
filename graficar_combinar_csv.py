import os
import glob
import matplotlib.pyplot as plt
import pandas as pd
import time
import numpy as np
from datetime import datetime, timedelta

def generate_report(datos_combinados, mur, rango, tiempo):
    reporte = "Informe\n"
    reporte += "========\n\n"
    reporte += f"Fecha y hora de inicio: {datetime.fromtimestamp(tiempo)}\n"
    reporte += f"Tiempo total transcurrido: {str(timedelta(seconds=time.time() - tiempo))}\n"
    reporte += f"Probabilidad de ganar el juego: {mur} ± {rango}\n"
    reporte += "\nTabla de datos:\n"

    # Obtener las columnas en orden numérico
    columnas_ordenadas = sorted(datos_combinados.columns[1:], key=lambda x: int(x.split('_')[1]))

    # Crear un nuevo DataFrame con las columnas ordenadas
    df_ordenado = datos_combinados[['intentos'] + columnas_ordenadas]

    # Convertir el DataFrame a una tabla de texto
    tabla = df_ordenado.to_string(index=False, justify='left')

    # Agregar la tabla al informe
    reporte += tabla

    # Guardar el informe en un archivo de texto
    with open("informe.txt", "w") as archivo_reporte:
        archivo_reporte.write(reporte)

    print("Informe generado exitosamente.")

def graficar_datos_csv(mur, rango, tiempo):
    # Obtener la lista de archivos CSV en el directorio actual
    archivos_csv = glob.glob("resultados_*.csv")

    # Leer y combinar los datos de los archivos CSV en un DataFrame
    datos_combinados = pd.DataFrame(columns=['intentos', 'probabilidad'])

    for archivo in archivos_csv:
        df = pd.read_csv(archivo)
        columna_nombre = os.path.splitext(archivo)[0]

        # Renombrar la columna de probabilidad con el nombre del archivo
        df = df.rename(columns={'probabilidad': columna_nombre})

        # Combinar los datos del archivo con el DataFrame
        if datos_combinados.empty:
            datos_combinados = df
        else:
            datos_combinados = datos_combinados.merge(df, on='intentos', how='outer')

    # Rellenar los valores faltantes hacia adelante
    datos_combinados.fillna(method='ffill', inplace=True)

    # Generar el informe
    generate_report(datos_combinados, mur, rango, tiempo)

    # Graficar los datos
    plt.figure(figsize=(10, 6))
    plt.xlabel('Intentos')
    plt.ylabel('Probabilidad')
    plt.title('Probabilidad en función de los intentos')
    plt.xscale('log')

    for archivo in archivos_csv:
        df = pd.read_csv(archivo)
        plt.plot(df['intentos'], df['probabilidad'], label=os.path.splitext(os.path.basename(archivo))[0])

    # Agregar la línea recta con el valor de "mur"
    plt.axhline(y=mur, color='r', linestyle='--', label='resultado')
    plt.text(1, mur, f'mur: {mur}', color='r', ha='left', va='bottom')

    # Crear un arreglo de x para el fill_between con el mismo largo que mur
    x_fill = np.linspace(min(df['intentos']), max(df['intentos']), len(df['intentos']))

    # Agregar la región de tolerancia
    plt.fill_between(x_fill, mur - rango, mur + rango, color='r', alpha=0.2, label=f'tolerancia ± {rango}')
    plt.text(1, mur + rango, f'(+/- {rango})', color='r', ha='left', va='bottom')

    # Agregar el valor de mur y su rango en la escala del eje y
    plt.yticks(list(plt.yticks()[0]) + [mur])

    plt.legend()
    plt.grid(True)
    ruta_imagen = os.path.join("Img", "prob.png")
    plt.savefig(ruta_imagen)
    plt.show(block=True)

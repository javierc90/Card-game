from juego import anillo
import csv
import os
from dotenv import load_dotenv
from graficar_combinar_csv import graficar_datos_csv
import time
from datetime import datetime, timedelta
import threading

load_dotenv()

def run_test(test_number):
    fo = open(f"resultados_{test_number}.csv", "w", encoding="utf-8", newline="")
    header = ['intentos', 'probabilidad']
    writer = csv.DictWriter(fo, fieldnames=header)
    writer.writeheader()
    intentos = []
    probabilidades = []
    j = int(os.getenv("j"))
    match = 0
    last_iteration = 0
    while True:
        j += 1
        for i in range(last_iteration, b ** j):
            if anillo():
                match += 1
            if not 10 * i % (b ** j):
                print(f"thread {test_number} : {int(100 * (i % (b ** j) / (b ** j)))}%")
        probabilidades.append(round((match / (b ** j) * 100), 2))
        intentos.append(b ** j)
        print("thread:",test_number, "-", match, "/", b ** j)
        writer.writerow({"intentos": intentos[-1], "probabilidad": probabilidades[-1]})
        if len(probabilidades) > 3:
            if 1 - intervalo < probabilidades[-1] / probabilidades[-2] < 1 + intervalo:
                mu.append(probabilidades[-1])
                fo.close()
                break
        last_iteration = b ** j

def run_tests_in_threads():
    cantidad_intentos = int(os.getenv("intentos"))
    threads = []
    for k in range(cantidad_intentos):
        t = threading.Thread(target=run_test, args=(k+1,))
        threads.append(t)
        t.start()
    
    # Espero que finalicen los test
    for t in threads:
        t.join()

if __name__ == '__main__':
    intervalo = float(os.getenv("intervalo"))
    mu = []
    b = int(os.getenv("b"))

    tiempo_inicio = time.time()
    
    run_tests_in_threads()
    
    mur = round(sum(mu) / len(mu),2)
    rango = round(mur - (mur * (1 - intervalo)),4)
    print("probabilidad de ganar el juego es", mur, "±", rango)
    print("tiempo total: ", str(timedelta(seconds=time.time() - tiempo_inicio)))
    graficar_datos_csv(mur,rango,tiempo_inicio)
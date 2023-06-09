import mazo

def anillo():
    cartas = mazo.Mazo()
    match = [False] * 13
    posicion = [[] for _ in range(13)]
    
    while len(cartas.mazo):
        try:
            for i in range(len(posicion)):
                if match[i] == False:
                    if __name__ == '__main__': print("Cantidad de cartas restantes:", len(cartas.mazo))
                    carta = cartas.sacar_carta()
                    posicion[i].append(carta)
                    if carta[1] == i+1:
                        match[i] = True
                        for a in range(len(posicion[i])-1):
                            cartas.colocar_carta(posicion[i][a])
                        posicion[i].clear()
                        posicion[i].append(carta)
            if(all(match)):
                if __name__ == '__main__': print("Has ganado!")
                return True                             
        except:
            if __name__ == '__main__': print("No hay mas cartas! Juego terminado.")
            return False 

if __name__ == '__main__':
    anillo()
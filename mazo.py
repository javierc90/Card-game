import random

class Mazo:
    def __init__(self):
        self.mazo = self.crear_mazo()
        self.mezclar()

    def __repr__(self):
        return str(self.mazo)

    def crear_mazo(self):
        mazo = []
        palos = ["♠", "♣", "♥", "♦"]
        valores = list(range(1, 14))
        
        for palo in palos:
            for valor in valores:
                mazo.append([palo, valor])
        
        return mazo

    def mezclar(self):
        random.shuffle(self.mazo)

    def sacar_carta(self):
        return self.mazo.pop(0)
    
    def colocar_carta(self, carta):
        self.mazo.append(carta)
        
    def reiniciar(self):
        self.mazo = self.crear_mazo()
        self.mezclar()
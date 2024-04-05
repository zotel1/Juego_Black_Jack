import random
from cartas import CartaPoker


class GeneradorCartas:
    """
    Clase GeneradorCartas encargada de generar cartas de póker basadas en ciertos criterios.
    
    Esta clase actúa como un generador, pero se implementa como un objeto iterable que produce cartas
    de póker basadas en los criterios especificados durante la inicialización.
    
    La clase ha sido diseñada para no ser heredable.
    
    Atributos:
        cantidad (int): Cantidad de cartas a generar.
        tapada (bool): Si las cartas deben estar tapadas. Por defecto es False.
        color (str): Color de las cartas ("rojo" o "negro"). Si es None, no se filtra por color.
        rango_numeros (tuple): Rango de números para las cartas, por ejemplo (1, 10) para cartas entre As y 10.
        producidas (int): Cantidad de cartas que ya se han producido.
    """
    
    def __init__(self, cantidad, tapada=False, color=None, rango_numeros=None):
        """
        Inicializa una instancia de GeneradorCartas.
        
        Args:
            cantidad (int): Cantidad de cartas a generar.
            tapada (bool): Si las cartas deben estar tapadas. Por defecto es False.
            color (str): Color de las cartas ("rojo" o "negro"). Si es None, no se filtra por color.
            rango_numeros (tuple): Rango de números para las cartas, por ejemplo (1, 10) para cartas entre As y 10.
        """
        self.__cantidad = cantidad
        self.__tapada = tapada
        self.__color = color
        self.__rango_numeros = rango_numeros
        self.__producidas = 0

    def __iter__(self):
        """Devuelve el objeto generador para ser iterado."""
        return self

    def __next__(self):
        """Produce la siguiente carta válida, o lanza StopIteration si se alcanza la cantidad deseada."""
        if self.__producidas < self.__cantidad:
            while True:
                num = random.randint(1, 13)
                palo = random.randint(1, 4)
                
                carta_valida = True
                
                # Verificar si la carta cumple con el color especificado
                if self.__color:
                    if self.__color == "rojo" and palo not in (1, 2):  # 1: Corazón, 2: Diamante
                        carta_valida = False
                    elif self.__color == "negro" and palo not in (3, 4):  # 3: Trébol, 4: Pica
                        carta_valida = False
                
                # Verificar si la carta cumple con el rango de números especificado
                if self.__rango_numeros and (num < self.__rango_numeros[0] or num > self.__rango_numeros[1]):
                    carta_valida = False
                
                # Si la carta es válida según los criterios, la producimos y aumentamos el contador
                if carta_valida:
                    self.__producidas += 1
                    return CartaPoker(num, palo, self.__tapada)

        else:
            raise StopIteration

    def __init_subclass__(cls, **kwargs):
        """
        Método mágico que se invoca automáticamente al intentar heredar de esta clase.
        
        Es decir, si intentas heredar de GeneradorCartas, Python invocará automáticamente 
        el método __init_subclass__ de la clase GeneradorCartas. 
        En nuestro caso, ese método simplemente lanza un TypeError para evitar que se 
        herede de la clase.

        Raises:
            TypeError: Si se intenta heredar de GeneradorCartas.
        """
        raise TypeError("La clase GeneradorCartas no puede ser heredada")


# Testeamos el generador
def test_generador_cartas():
    print("Se esta ejecutando el test de la clase GeneradorCartas")
    cartas_generadas = list(GeneradorCartas(5, color="rojo", rango_numeros=(1, 2)))
    print(cartas_generadas)
    for carta in GeneradorCartas(25):
        print(carta,end='')    
    print(list(GeneradorCartas(10)))

if __name__ == '__main__':
    test_generador_cartas()

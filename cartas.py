"""
cartas.py - Módulo para representar y manipular cartas de póker.

Este módulo provee una representación de cartas de póker y 
funcionalidades asociadas para manipularlas. Las cartas pueden
estar tapadas o destapadas, y se pueden comparar entre sí.

Clases:
    - Carta:
    - CartaPoker: Representa una carta de póker con un número y un palo.

Uso típico:

    carta1 = CartaPoker(10, 4)  # 10 de picas
    carta2 = CartaPoker(1, 1)  # As de corazones
    print(carta1)  # [10♠]
    print(carta2.isroja())  # True

Véase la documentación de `CartaPoker` para más detalles.
"""

from txtcolores import strclr
import random
from abc import ABC, abstractmethod

class Carta(ABC):
    def __init__(self, numero: int, palo: int, tapada: bool = False) -> None:
        """
        Inicializa una carta con un número, palo y si está tapada.

        Args:
            numero (int): Número de la carta.
            palo (int): Palo de la carta.
            tapada (bool, optional): Si la carta está tapada. Por defecto es False.

        Raises:
            ValueError: Si el número o palo no es válido.
        """

        if not 1 <= numero <= 13 or not 1 <= palo <= 4:
            raise ValueError("Número o palo no válido")

        self.__numero: int = numero
        self.__palo: int = palo
        self.__tapada: bool = tapada

    def __str__(self) -> str:
        """
        Retorna la representación en cadena de la carta.

        Returns:
            str: Representación en cadena de la carta.
        """
        marco_derecho = strclr("]",148)
        marco_izquierdo = strclr("[",148)

        return f"{marco_izquierdo}{self.el_dibujo_del_numero()}{self.el_dibujo_del_palo()}{marco_derecho}"

    @property
    def numero(self) -> int:
        """Retorna el número de la carta."""
        return self.__numero

    @property
    def palo(self) -> int:
        """Retorna el palo de la carta."""
        return self.__palo

    @property
    def istapada(self) -> bool:
        """Retorna si la carta está tapada."""
        return self.__tapada

    def tapar(self) -> None:
        """Tapa la carta."""
        self.__tapada = True

    def destapar(self) -> None:
        """Destapa la carta."""
        self.__tapada = False

    def darvuelta(self) -> None:
        """Invierte el estado de tapada de la carta."""
        self.__tapada = not self.__tapada

    def __eq__(self, other: object) -> bool:
        """
        Compara si dos cartas son iguales.

        Args:
            other (object): Otro objeto para comparar.

        Returns:
            bool: True si las cartas son iguales, False en caso contrario.
        """
        if other is None or not isinstance(other, Carta):
            return False
        return self.numero == other.numero and self.palo == other.palo

    def __ne__(self, other: object) -> bool:
        """
        Compara si dos cartas son diferentes.

        Args:
            other (object): Otro objeto para comparar.

        Returns:
            bool: True si las cartas son diferentes, False en caso contrario.
        """
        return not self.__eq__(other)
    
    def __repr__(self) -> str:
        return str(self)

    @abstractmethod
    def el_dibujo_del_numero(self)->str:
        pass

    @abstractmethod
    def el_dibujo_del_palo(self)-> str:
        pass


class CartaPoker(Carta):

    # Constantes de clase
    CORAZON = "♥"
    DIAMANTE = "♦"
    TREBOL = "♣"
    PICA = "♠" 
    FONDO = "#"  
    ROJAS = (CORAZON,DIAMANTE) 
    NEGRAS = (PICA,TREBOL)
    PALOS = (FONDO,CORAZON,DIAMANTE,TREBOL,PICA)
    NUMEROS = (FONDO, "A", "2", "3", "4", "5", "6",
               "7", "8", "9", "10", "J", "Q", "K")
    
    def isroja(self) -> bool:
        """Retorna True si la carta es roja."""
        return self.palo in (1,2)

    def isnegra(self) -> bool:
        """Retorna True si la carta es negra."""
        return self.palo in (3,4)

    def isas(self) -> bool:
        """Retorna True si la carta es un as."""
        return self.numero == 1

    def ispica(self) -> bool:
        """Retorna True si el palo de la carta es pica."""
        return self.palo == CartaPoker.PICA

    def iscorazon(self) -> bool:
        """Retorna True si el palo de la carta es corazón."""
        return self.palo == CartaPoker.CORAZON

    def istrebol(self) -> bool:
        """Retorna True si el palo de la carta es trébol."""
        return self.palo == CartaPoker.TREBOL 

    def isdiamante(self) -> bool:
        """Retorna True si el palo de la carta es diamante."""
        return self.palo == CartaPoker.DIAMANTE

    def el_dibujo_del_numero(self) -> str:
        if self.istapada:
            txt_numero = strclr(CartaPoker.FONDO,'dark_orange')
        else:
            txt_numero = strclr(CartaPoker.NUMEROS[self.numero],7)
        return txt_numero
    

    def el_dibujo_del_palo(self) -> str:
        if self.istapada:
            txt_palo= strclr(CartaPoker.FONDO,'dark_orange')
        elif self.isroja():                
            txt_palo = strclr(CartaPoker.PALOS[self.palo],'red_1')
        else:
            txt_palo = strclr(CartaPoker.PALOS[self.palo],'white')
        return txt_palo
 
class CartaEspaniola(Carta):
    def __init__(self, numero: int, palo: int, tapada: bool = False) -> None:
        super().__init__(numero, palo, tapada)

def test_cartas():
    print("Se esta ejecutando el test de la clase CartaPoker")
    carta1 = CartaPoker(10, 4)  # 10 de picas
    carta2 = CartaPoker(1, 1)  # As de corazones
    print(carta2)  # [A♥]
    print(carta1)  # [10♠]
    
    
if __name__ == '__main__':
    test_cartas()


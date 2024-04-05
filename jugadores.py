from os import system
from txtcolores import strclr
import utilidades2 as util
from abc import ABC, abstractmethod
from cartas import Carta, CartaPoker, CartaEspaniola
from mazos import MazoBlackJack, Mazo
import random


class JugadorCartas(ABC):
    """Representa un jugador genérico en un juego de cartas.

    Atributos:
        __nombre (str): El nombre del jugador.
        __mano (Mazo): El mazo de cartas que tiene en la mano el jugador.
    """
    def __init__(self, nombre: str, mazo: Mazo) -> None:
        """Inicializa un nuevo jugador con un nombre y un mazo de cartas.

        Args:
            nombre (str): El nombre del jugador.
            mazo (Mazo): El mazo de cartas del jugador.
        """
        self.__nombre: str = nombre
        self.__mano: Mazo = mazo

    @property
    def nombre(self) -> str:
        """Obtiene el nombre del jugador.

        Returns:
            str: El nombre del jugador.
        """
        return self.__nombre

    @property
    def mano(self) -> Mazo:
        """Obtiene el mazo de cartas que tiene en la mano el jugador.

        Returns:
            Mazo: El mazo de cartas del jugador.
        """
        return self.__mano

    def __str__(self) -> str:
        """Representación en cadena de caracteres del jugador y su mano.

        Returns:
            str: Una cadena que representa al jugador y las cartas que tiene.
        """
        return f"{self.nombre} {self.mano}"


class Plantable (ABC):
    """Define una interfaz para entidades que pueden decidir plantarse en un juego de cartas."""

    def __init__(self) -> None:
        """Inicializa una entidad que puede plantarse."""
        super().__init__()

    @abstractmethod
    def me_planto(self) -> bool:
        """Determina si la entidad decide plantarse.

        Returns:
            bool: True si la entidad se planta, False en caso contrario.
        """
        pass


class JugadorBlackJack(JugadorCartas, Plantable):
    """Representa un jugador de BlackJack.

    Esta clase hereda de JugadorCartas y Plantable para implementar las funcionalidades
    específicas de un jugador en el juego de BlackJack.
    """
    def __init__(self, nombre: str) -> None:
        """Inicializa un nuevo jugador de BlackJack con un nombre y un mazo de BlackJack.

        Args:
            nombre (str): El nombre del jugador.
        """
        super().__init__(nombre, MazoBlackJack())

    def poner_carta(self, carta: CartaPoker, index: int = None) -> None:
        """Agrega una carta a la mano del jugador.

        Args:
            carta (CartaPoker): La carta a agregar.
            index (int, optional): La posición en la que se debe agregar la carta. Defaults to None.
        """
        self.mano.poner_carta(carta, index)

    def sacar_carta(self, index: int = None) -> CartaPoker:
        """Retira una carta de la mano del jugador.

        Args:
            index (int, optional): La posición de la carta a retirar. Defaults to None.

        Returns:
            CartaPoker: La carta retirada de la mano.
        """
        return self.mano.sacar_carta(index)

    def sumar_cartas(self) -> int:
        """Calcula la suma total de las cartas en la mano del jugador según las reglas de BlackJack.

        En BlackJack, los ases pueden valer 1 u 11 puntos, y esta función calcula el valor óptimo.

        Returns:
            int: La suma total de las cartas en la mano del jugador.
        """
        cantidad_unos = 0
        suma_numeros = 0
        for carta in self.mano:
            if carta.numero == 1:
                cantidad_unos += 1
            elif carta.numero >= 10:
                suma_numeros += 10
            else:
                suma_numeros += carta.numero
        suma = 0
        if cantidad_unos == 0:
            suma = suma_numeros
        elif cantidad_unos == 1:
            if 11 + suma_numeros > 21:
                suma = 1 + suma_numeros
            else:
                suma = 11 + suma_numeros
        else:
            if suma_numeros + 11 + cantidad_unos - 1 > 21:
                suma = suma_numeros + cantidad_unos
            else:
                suma = suma_numeros + 11 + cantidad_unos - 1
        return suma


class Croupier(JugadorBlackJack):
    """Representa al croupier en un juego de BlackJack.

    El croupier tiene reglas específicas para plantarse que están implementadas en el método me_planto.
    """
    def __init__(self) -> None:
        """Inicializa al croupier con el nombre 'Sr. Croupier'."""
        super().__init__("Sr. Croupier")

    def me_planto(self) -> bool:
        """Decide si el croupier se planta según las reglas de BlackJack.

        El croupier se planta si la suma de sus cartas es mayor o igual a 17 y no se ha pasado de 21.

        Returns:
            bool: True si el croupier se planta, False si decide tomar otra carta.
        """
        respuesta = True
        suma = self.sumar_cartas()
        print(f"{str(self)} ({suma})")
        if suma > 21:
            print(strclr("Se paso", 'red'))
            system('pause')
        elif suma >= 17:
            print("¿Se planta? [S/N]: S")
            system('pause')
        else:
            respuesta = False
        return respuesta


class Apostable(ABC):
    """Define una interfaz para entidades que pueden realizar apuestas."""

    def __init__(self) -> None:
        """Inicializa una entidad que puede realizar apuestas."""
        super().__init__()

    @abstractmethod
    def apuesto(self) -> int:
        """Calcula la cantidad de la apuesta que realizará la entidad.

        Returns:
            int: La cantidad de la apuesta.
        """
        pass


class Cliente(JugadorBlackJack, Apostable):
    """Representa a un cliente jugando BlackJack.

    Esta clase hereda de JugadorBlackJack y Apostable, permitiendo al cliente apostar y jugar BlackJack.

    Atributos:
        __fichas (int): La cantidad de fichas que el cliente posee para apostar.
    """

    def __init__(self, nombre: str, fichas: int) -> None:
        """Inicializa un nuevo cliente con un nombre y una cantidad inicial de fichas.

        Args:
            nombre (str): El nombre del cliente.
            fichas (int): La cantidad inicial de fichas del cliente.
        """
        super().__init__(nombre)
        self.__fichas:int = fichas

    @property
    def fichas(self) -> int:
        """Obtiene la cantidad actual de fichas del cliente.

        Returns:
            int: La cantidad de fichas que el cliente tiene.
        """
        return self.__fichas
    
    def ganar_fichas(self, cantidad: int) -> None:
        """Incrementa la cantidad de fichas del cliente.

        Args:
            cantidad (int): La cantidad de fichas a añadir al total del cliente.
        """
        self.__fichas += cantidad

    def perder_fichas(self, cantidad: int) -> None:
        """Decrementa la cantidad de fichas del cliente.

        Args:
            cantidad (int): La cantidad de fichas a restar del total del cliente.
        """
        self.__fichas -= cantidad


    def __str__(self) -> str:
        """Representación en cadena de caracteres del cliente, sus fichas y la suma de sus cartas.

        Returns:
            str: Una cadena que representa al cliente, sus fichas y la suma de sus cartas.
        """
        return f"{super().__str__()} ${self.fichas} ({self.sumar_cartas()})"


class Humano(Cliente):
    """Representa a un jugador humano en un juego de BlackJack.

    Esta clase hereda de Cliente y añade interacciones específicas que un humano podría tener en el juego.
    """

    def __init__(self, nombre: str, fichas: int) -> None:
        """Inicializa un nuevo jugador humano con un nombre y una cantidad inicial de fichas.

        Args:
            nombre (str): El nombre del jugador humano.
            fichas (int): La cantidad inicial de fichas del jugador.
        """
        super().__init__(nombre, fichas)

    def apuesto(self) -> int:
        """Permite al jugador humano realizar una apuesta.

        Devuelve un entero que representa la cantidad de fichas apostadas, dentro del rango permitido.

        Returns:
            int: La cantidad de fichas apostadas por el jugador.
        """
        print(self)
        return util.leer_entero("Cantidad fichas: ", 1, self.fichas)

    def me_planto(self) -> bool:
        """Permite al jugador humano decidir si se planta o toma otra carta.

        El jugador se planta si tiene más de 21 puntos, exactamente 21 puntos, o elige hacerlo.

        Returns:
            bool: True si el jugador decide plantarse, False si decide tomar otra carta.
        """

        respuesta = True
        print(self)
        suma = self.sumar_cartas()
        if suma > 21:
            print(strclr("Se paso", 'red'))
            system('pause')

        elif suma == 21:
            print("¿Se planta? [S/N]: S")
            system('pause')

        else:
            respuesta = util.continua("¿Se planta?")
        return respuesta


class Compu(Cliente):
    """Representa a un jugador computarizado en un juego de BlackJack.

    El jugador computarizado tiene una 'personalidad' que influye en su toma de decisiones de apuestas y juego.

    Atributos:
        TRAN (int): El valor mínimo de la personalidad, representando un jugador conservador.
        LOCO (int): El valor máximo de la personalidad, representando un jugador agresivo.
    """

    TRAN: int = 1
    LOCO: int = 100

    def __init__(self, nombre: str, fichas: int) -> None:
        """Inicializa un nuevo jugador computarizado con un nombre y una cantidad inicial de fichas.

        Args:
            nombre (str): El nombre del jugador computarizado.
            fichas (int): La cantidad inicial de fichas del jugador.
        """
        super().__init__(nombre, fichas)
        self.__personalidad: int = self.__obtener_personalidad()

    @property
    def personalidad(self) -> int:
        """Obtiene la personalidad del jugador computarizado.

        Returns:
            int: La personalidad del jugador computarizado.
        """
        return self.__personalidad

    def apuesto(self) -> int:
        """Realiza una apuesta basada en la personalidad del jugador computarizado.

        Returns:
            int: La cantidad de fichas apostadas por el jugador computarizado.
        """
        print(self)

        pensamiento = self.__pensar()
        if pensamiento < self.__personalidad:
            desde = self.fichas // 2
            hasta = self.fichas
        else:
            desde = 1
            hasta = self.fichas // 2
        cantidad = random.randint(desde, hasta)
        print(f"Cantidad fichas: {cantidad}")
        system('pause')
        return cantidad

    def me_planto(self) -> bool:
        """Decide si el jugador computarizado se planta o toma otra carta.

        Returns:
            bool: True si el jugador computarizado decide plantarse, False si decide tomar otra carta.
        """
        respuesta = True
        print(self)
        suma = self.sumar_cartas()
        if suma > 21:
            print(strclr("Se paso", 'red'))
            system('pause')
            return True
        elif suma == 21:
            letra = 'S'
            print("¿Se planta? [S/N]: S")
        else:  # DONDE SE PIENSA
            pensamiento = self.__pensar()
            if suma >= 15:
                if pensamiento < self.personalidad:
                    respuesta = False
                    letra = 'N'
                else:
                    respuesta = True
                    letra = 'S'
            else:
                respuesta = False
                letra = 'N'
        print(f"¿Se planta? [S/N]: {letra}")
        system('pause')
        return respuesta

    def __pensar(self) -> int:
        """Genera un número aleatorio que representa el 'pensamiento' del jugador computarizado.

        Returns:
            int: Un número aleatorio entre TRAN y LOCO.
        """
        return random.randint(Compu.TRAN, Compu.LOCO)

    def __obtener_personalidad(self) -> int:
        """Obtiene un valor aleatorio que representa la personalidad del jugador computarizado.

        Returns:
            int: Un número aleatorio entre TRAN y LOCO que define la personalidad del jugador.
        """
        return random.randint(Compu.TRAN, Compu.LOCO)


if __name__ == "__main__":
    m = MazoBlackJack()
    m.llenar()
    m.barajar()
    print(len(m))
    cr = Croupier()
    c = m.sacar_carta()
    c.tapar()
    cr.poner_carta(c)
    cr.poner_carta(m.sacar_carta())
    print(cr)

    h = Humano("Cris", 200)
    h.poner_carta(m.sacar_carta())
    h.poner_carta(m.sacar_carta())
    print(h)
    c = h.sacar_carta()
    c.tapar()
    h.poner_carta(c, 0)
    print(h)
    print(len(m))

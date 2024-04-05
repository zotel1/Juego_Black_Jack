import utilidades2 as util
from cartas import CartaPoker
from mazos import MazoBlackJack
from jugadores import Humano, Compu, Croupier, Cliente
from txtcolores import strclr


class BlackJack:
    """Representa un juego de BlackJack.

    Atributos:
        __croupier (Croupier): El croupier del juego.
        __jugadores (list[Cliente]): Lista de jugadores en el juego.
        __mazo (MazoBlackJack): El mazo de cartas utilizado en el juego.
        __apuestas (list[int]): Las apuestas realizadas por los jugadores.
    """
    def __init__(self) -> None:
        """Inicializa una nueva instancia de BlackJack."""
        self.__croupier: Croupier = Croupier()
        self.__jugadores: list[Cliente] = []
        self.__mazo: MazoBlackJack = MazoBlackJack()
        self.__apuestas: list[int] = []

    @property
    def croupier(self) -> Croupier:
        """Obtiene el croupier del juego.

        Returns:
            Croupier: El croupier del juego.
        """
        return self.__croupier
    
    @property
    def jugadores(self) -> list[Cliente]:
        """Obtiene la lista de jugadores del juego.

        Returns:
            list[Cliente]: Lista de jugadores en el juego.
        """
        return self.__jugadores

    @property
    def mazo(self) -> MazoBlackJack:
        """Obtiene el mazo de cartas del juego.

        Returns:
            MazoBlackJack: El mazo de cartas utilizado en el juego.
        """
        return self.__mazo

    @property
    def apuestas(self) -> list[int]:
        """Obtiene las apuestas realizadas por los jugadores.

        Returns:
            list[int]: Las apuestas realizadas por los jugadores.
        """
        return self.__apuestas

    def agregar_jugador(self, jugador: Cliente) -> None:
        """Agrega un nuevo jugador al juego.

        Args:
            jugador (Cliente): El jugador a agregar al juego.

        Raises:
            ValueError: Si el objeto no es una instancia de Cliente.
        """
        if not isinstance(jugador, Cliente):
            raise ValueError("Solo pueden jugar clientes")
        self.jugadores.append(jugador)

    def __hay_jugadores(self) -> bool:
        """Determina si hay jugadores en el juego.

        Returns:
            bool: True si hay jugadores, False en caso contrario.
        """
        return len(self.jugadores) > 0

    def __jugadores_apuestan(self) -> None:
        """Proceso donde los jugadores realizan sus apuestas."""
        util.system("cls")
        print(util.titulo('Los jugadores apuestan'))
        print(self.croupier)
        for jugador in self.jugadores:
            self.apuestas.append(jugador.apuesto())

    def __croupier_reparte_dos_cartas(self) -> None:
        """El croupier reparte dos cartas a cada jugador y a sí mismo."""
        print(util.titulo('El croupier reparte dos cartas'))
        for jugador in self.jugadores:
            jugador.poner_carta(self.mazo.sacar_carta())
            jugador.poner_carta(self.mazo.sacar_carta())
        c = self.mazo.sacar_carta()
        c.tapar()
        self.croupier.poner_carta(c)
        self.croupier.poner_carta(self.mazo.sacar_carta())

    def __jugadores_juegan(self) -> None:
        """Proceso donde cada jugador decide si pide más cartas o se planta."""
        print(util.titulo("los jugadores juegan"))
        print(self.croupier)
        for jugador in self.jugadores:
            while not jugador.me_planto():
                jugador.poner_carta(self.mazo.sacar_carta())

    def __croupier_juega(self) -> None:
        """Proceso donde el croupier juega su mano después de los jugadores."""
        print(util.titulo("El croupier juega"))
        c = self.croupier.sacar_carta()
        c.destapar()
        self.croupier.poner_carta(c, 0)
        while not self.croupier.me_planto():
            self.croupier.poner_carta(self.mazo.sacar_carta())

    def __croupier_reparte_premios(self) -> None:
        """El croupier reparte los premios a los jugadores según las reglas del juego."""
        util.system("cls")
        print(util.titulo('el croupier reparte los premios'))
        suma_croupier = self.croupier.sumar_cartas()
        print(f"{str(self.croupier)} ({suma_croupier})", end="")
        suma_jugador = 0
        if suma_croupier > 21:  # Se paso el croupier
            print(strclr(" SE PASO", 'red'))
            for jugador in self.jugadores:
                apuesta = self.apuestas[self.jugadores.index(jugador)]
                suma_jugador = jugador.sumar_cartas()
                if suma_jugador > 21:  # PIERDE EL JUGADOR; SE PASO
                    jugador.perder_fichas(apuesta)
                    print(f"¡{jugador} PIERDE {apuesta} FICHAS SE PASO!")
                else:  # GANA EL JUGADOR
                    jugador.ganar_fichas(apuesta)
                    print(f"¡{jugador} GANA {apuesta} FICHAS EL CROUPIER SE PASO!")
        else:  # EL CROUPIUER NO SE PASA
            print()
            for jugador in self.jugadores:
                apuesta = self.apuestas[self.jugadores.index(jugador)]
                suma_jugador = jugador.sumar_cartas()
                if suma_jugador > 21:  # PIERDE EL JUGADOR SE PASO
                    jugador.perder_fichas(apuesta)
                    print(f"¡{jugador} PIERDE {apuesta} FICHAS, EL JUGADOR SE PASO!")
                elif suma_jugador < suma_croupier:  # PIERDE EL JUGADOR, LE GANA EL CROUPIER
                    jugador.perder_fichas(apuesta)
                    print(f"¡{jugador} PIERDE {apuesta} FICHAS, EL CROUPIER LE GANO!")
                elif suma_jugador > suma_croupier:  # GANA EL JUGADOR
                    jugador.ganar_fichas(apuesta)
                    print(f"¡{jugador} GANA {apuesta} FICHAS, EL CROUPIER PIERDE!")
                else:  # EMPATE
                    print(f"¡{jugador} EMPATE!")
        util.system('pause')

    def __jugadores_se_descartan(self) -> None:
        """Los jugadores se descartan de sus cartas al final de la ronda."""
        #print(util.titulo("los jugadores se descartan"))
        for jugador in self.jugadores:
            while not jugador.mano.isvacio():
                self.mazo.poner_carta(jugador.sacar_carta())

    def __croupier_se_descarta(self) -> None:
        """El croupier se descarta de sus cartas al final de la ronda."""
        # print(util.titulo("el croupier se descarta"))
        while not self.croupier.mano.isvacio():
            self.mazo.poner_carta(self.croupier.sacar_carta())

    def __jugadores_se_retiran(self) -> None:
        """Retira a los jugadores que ya no tienen fichas para apostar."""
        util.system("cls")
        print(util.titulo("los jugadores se retiran"))
        bandera = False
        index = 0
        while index < len(self.jugadores):
            if self.jugadores[index].fichas <= 0:
                print(f"{self.jugadores[index].nombre} Se retira del juego")
                self.jugadores.pop(index)
                bandera = True
            else:
                index += 1
        if bandera:
            util.system("pause")

    def jugar(self) -> None:
        """Inicia y controla el flujo del juego de BlackJack."""
        self.mazo.llenar()
        while self.__hay_jugadores():
            self.apuestas.clear()
            self.mazo.barajar()
            self.__croupier_reparte_dos_cartas()
            self.__jugadores_apuestan()
            self.__jugadores_juegan()
            self.__croupier_juega()
            self.__croupier_reparte_premios()
            self.__jugadores_se_descartan()
            self.__croupier_se_descarta()
            self.__jugadores_se_retiran()


def main():

    juego = BlackJack()
    juego.agregar_jugador(Humano("Cris", 100))
    juego.agregar_jugador(Compu("Batman", 100))
    juego.agregar_jugador(Humano("Zotel", 100))
    juego.agregar_jugador(Compu("Spider-man", 100))
    juego.jugar()


main()

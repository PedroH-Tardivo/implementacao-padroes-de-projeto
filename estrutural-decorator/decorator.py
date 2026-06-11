from abc import ABC, abstractmethod


class Personagem(ABC):
    @abstractmethod
    def descricao(self) -> str:
        pass

    @abstractmethod
    def vida(self) -> int:
        pass

    @abstractmethod
    def ataque(self) -> int:
        pass


class Guerreiro(Personagem):
    def descricao(self) -> str:
        return "Guerreiro"

    def vida(self) -> int:
        return 100

    def ataque(self) -> int:
        return 10


class DecoradorEquipamento(Personagem):
    def __init__(self, personagem: Personagem):
        self._personagem = personagem

    def descricao(self) -> str:
        return self._personagem.descricao()

    def vida(self) -> int:
        return self._personagem.vida()

    def ataque(self) -> int:
        return self._personagem.ataque()


class Espada(DecoradorEquipamento):
    def descricao(self) -> str:
        return self._personagem.descricao() + " com espada"

    def ataque(self) -> int:
        return self._personagem.ataque() + 25


class Armadura(DecoradorEquipamento):
    def descricao(self) -> str:
        return self._personagem.descricao() + " com armadura"

    def vida(self) -> int:
        return self._personagem.vida() + 50


class Amuleto(DecoradorEquipamento):
    def descricao(self) -> str:
        return self._personagem.descricao() + " com amuleto"

    def vida(self) -> int:
        return self._personagem.vida() + 30

    def ataque(self) -> int:
        return self._personagem.ataque() + 10


def exibir(personagem: Personagem):
    print(f"{personagem.descricao()}")
    print(f"  Vida: {personagem.vida()} | Ataque: {personagem.ataque()}")


if __name__ == "__main__":
    personagem = Guerreiro()
    exibir(personagem)

    personagem = Espada(personagem)
    exibir(personagem)

    personagem = Armadura(personagem)
    exibir(personagem)

    personagem = Amuleto(personagem)
    exibir(personagem)

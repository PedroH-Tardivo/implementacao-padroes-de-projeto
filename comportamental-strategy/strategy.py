from abc import ABC, abstractmethod


class EstrategiaOrdenacao(ABC):
    @abstractmethod
    def ordenar(self, produtos: list) -> list:
        pass


class OrdenarPorPreco(EstrategiaOrdenacao):
    def ordenar(self, produtos: list) -> list:
        return sorted(produtos, key=lambda p: p["preco"])


class OrdenarPorNome(EstrategiaOrdenacao):
    def ordenar(self, produtos: list) -> list:
        return sorted(produtos, key=lambda p: p["nome"])


class OrdenarPorAvaliacao(EstrategiaOrdenacao):
    def ordenar(self, produtos: list) -> list:
        return sorted(produtos, key=lambda p: p["avaliacao"], reverse=True)


class ListaProdutos:
    def __init__(self, estrategia: EstrategiaOrdenacao):
        self._estrategia = estrategia

    def alterar_estrategia(self, estrategia: EstrategiaOrdenacao):
        self._estrategia = estrategia

    def exibir(self, produtos: list):
        resultado = self._estrategia.ordenar(produtos)
        for p in resultado:
            print(f"{p['nome']} | R${p['preco']:.2f} | Avaliação: {p['avaliacao']}")


if __name__ == "__main__":
    produtos = [
        {"nome": "Teclado", "preco": 150.00, "avaliacao": 4.2},
        {"nome": "Monitor", "preco": 900.00, "avaliacao": 4.8},
        {"nome": "Mouse",   "preco": 80.00,  "avaliacao": 3.9},
        {"nome": "Headset", "preco": 250.00, "avaliacao": 4.5},
    ]

    lista = ListaProdutos(OrdenarPorPreco())
    print("Por preço:")
    lista.exibir(produtos)

    lista.alterar_estrategia(OrdenarPorNome())
    print("\nPor nome:")
    lista.exibir(produtos)

    lista.alterar_estrategia(OrdenarPorAvaliacao())
    print("\nPor avaliação:")
    lista.exibir(produtos)

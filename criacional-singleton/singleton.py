class GerenciadorSenhas:
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia._senha_atual = 0
            cls._instancia._atendimentos = []
        return cls._instancia

    def gerar_senha(self):
        self._senha_atual += 1
        return self._senha_atual

    def registrar_atendimento(self, senha):
        self._atendimentos.append(senha)
        print(f"Senha {senha:03d} chamada para atendimento.")

    def senhas_pendentes(self):
        return self._senha_atual - len(self._atendimentos)

    def status(self):
        print(f"Última senha: {self._senha_atual:03d} | Atendidas: {len(self._atendimentos)} | Pendentes: {self.senhas_pendentes()}")


if __name__ == "__main__":
    totem_entrada = GerenciadorSenhas()
    painel_recepcao = GerenciadorSenhas()

    print("São a mesma instância?", totem_entrada is painel_recepcao)
    print()

    s1 = totem_entrada.gerar_senha()
    s2 = totem_entrada.gerar_senha()
    s3 = painel_recepcao.gerar_senha()

    print(f"Senhas geradas: {s1:03d}, {s2:03d}, {s3:03d}")
    print()

    painel_recepcao.registrar_atendimento(s1)
    painel_recepcao.registrar_atendimento(s2)

    print()
    totem_entrada.status()

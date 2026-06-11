# Implementação de Padrões de Projeto

Repositório criado para documentar e implementar padrões de projeto,
um por categoria: criacional, estrutural e comportamental.
Todas implementações foram feitas em Python 3.

Referência: https://refactoring.guru/pt-br/design-patterns, de autoria de Alexander Shvets. As implementações e exemplos contextualizados são originais.

---

## O que são padrões de projeto?

Durante anos de desenvolvimento de software, programadores perceberam que
certos problemas de design aparecem repetidamente em sistemas diferentes.
Padrões de projeto são soluções documentadas para esses problemas recorrentes.

Eles não são trechos de código prontos para copiar, são descrições de como
estruturar classes e objetos para resolver um tipo específico de problema.
Além de resolver o problema em si, eles criam um vocabulário comum entre
desenvolvedores: quando alguém diz "usei um Observer aqui", qualquer outro
programador que conhece o padrão já entende a estrutura sem precisar ler o código.

Os padrões são divididos em três categorias. Os criacionais controlam
como os objetos são criados, os estruturais organizam como classes e
objetos se conectam, e os comportamentais definem como os objetos se
comunicam e dividem responsabilidades entre si.

---

## Padrões implementados

Singleton (Criacional): `criacional-singleton/singleton.py`

Decorator (Estrutural): `estrutural-decorator/decorator.py`

---

## Singleton — Criacional

> Referência: https://refactoring.guru/pt-br/design-patterns/singleton

### Contexto

Em sistemas onde um único recurso precisa ser compartilhado por várias partes
do programa, criar múltiplos objetos independentes pode causar inconsistências.
O Singleton garante que apenas uma instância de uma classe exista durante
toda a execução, e que qualquer parte do sistema que precisar dessa instância
receba sempre a mesma.

### Problema

Considere um sistema de atendimento com senha eletrônica, como os usados em
bancos e cartórios. O totem na entrada gera senhas para os clientes, e o painel
da recepção registra os atendimentos. Se cada um desses pontos criasse seu
próprio objeto de controle de senhas de forma independente, o totem poderia
estar na senha 010 enquanto o painel ainda acredita que a última gerada foi 005,
porque cada um teria seu próprio contador separado. Clientes receberiam senhas
duplicadas e o controle de fila quebraria completamente.

### Solução

O Singleton garante que não importa quantas vezes o programa tente criar um
objeto GerenciadorSenhas, ele sempre receberá o mesmo objeto. O totem e o
painel compartilham o mesmo contador, o mesmo histórico e o mesmo estado.

### Como o código funciona

O controle começa na variável `_instancia`, definida diretamente na classe.
Ela é lida apenas uma vez, quando o Python carrega o arquivo, e começa como
`None` indicando que nenhum objeto ainda foi criado.

```python
class GerenciadorSenhas:
    _instancia = None
```

O método `__new__` é chamado pelo Python toda vez que alguém tenta criar um
objeto da classe. Aqui ele é sobrescrito para interceptar essa criação. Se
`_instancia` ainda for `None`, o objeto é criado, seus dados são inicializados
e ele é armazenado na classe. Caso contrário, o bloco é ignorado e o objeto
já existente é retornado diretamente. O resultado é que não importa quantas
vezes a classe seja chamada, sempre se recebe o mesmo objeto.

```python
    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia._senha_atual = 0
            cls._instancia._atendimentos = []
        return cls._instancia
```

`gerar_senha` incrementa o contador interno e retorna o novo número. Como
existe apenas uma instância, o contador nunca reinicia entre chamadas de
partes diferentes do sistema.

```python
    def gerar_senha(self):
        self._senha_atual += 1
        return self._senha_atual
```

`registrar_atendimento` recebe o número de uma senha e a adiciona à lista
de atendidas, registrando que aquele cliente já foi chamado.

```python
    def registrar_atendimento(self, senha):
        self._atendimentos.append(senha)
        print(f"Senha {senha:03d} chamada para atendimento.")
```

`senhas_pendentes` calcula a diferença entre o total de senhas geradas e
as que já foram atendidas, retornando quantos clientes ainda estão esperando.

```python
    def senhas_pendentes(self):
        return self._senha_atual - len(self._atendimentos)
```

`status` exibe um resumo do estado atual do gerenciador, mostrando a última
senha gerada, quantas foram atendidas e quantas ainda estão na fila.

```python
    def status(self):
        print(f"Última senha: {self._senha_atual:03d} | Atendidas: {len(self._atendimentos)} | Pendentes: {self.senhas_pendentes()}")
```

No código cliente, mesmo tentando criar dois objetos separados, os dois
recebem a mesma instância. O painel continua o contador de onde o totem parou
porque compartilham o mesmo estado.

```python
totem_entrada = GerenciadorSenhas()
painel_recepcao = GerenciadorSenhas()

print("São a mesma instância?", totem_entrada is painel_recepcao)

s1 = totem_entrada.gerar_senha()
s2 = totem_entrada.gerar_senha()
s3 = painel_recepcao.gerar_senha()

painel_recepcao.registrar_atendimento(s1)
painel_recepcao.registrar_atendimento(s2)

totem_entrada.status()
```

### Como executar

```bash
python3 criacional-singleton/singleton.py
```

### Saída esperada

```
São a mesma instância? True

Senhas geradas: 001, 002, 003

Senha 001 chamada para atendimento.
Senha 002 chamada para atendimento.

Última senha: 003 | Atendidas: 2 | Pendentes: 1
```

---

## Decorator — Estrutural

> Referência: https://refactoring.guru/pt-br/design-patterns/decorator

### Contexto

Em sistemas onde objetos precisam ganhar comportamentos extras de forma
flexível e combinável, usar herança para cada variação gera uma quantidade
impraticável de subclasses. O Decorator resolve isso envolvendo o objeto
original em camadas, onde cada camada acrescenta algo sem modificar o que
está dentro.

### Problema

Em um jogo, um personagem começa com atributos base e pode equipar itens
ao longo da partida. Se cada combinação de equipamentos fosse uma subclasse,
seriam necessárias classes como GuerreiroComEspada, GuerreiroComArmadura,
GuerreiroComEspadaEArmadura, GuerreiroComEspadaArmaduraEAmuleto e assim
por diante. Com apenas 3 itens isso já se torna inviável, e cada novo item
adicionado ao jogo multiplicaria o problema.

### Solução

Cada equipamento é um Decorator que envolve o personagem e acrescenta seus
atributos aos que já existem. Os itens são empilhados em tempo de execução
na ordem que o jogador equipar, sem precisar criar nenhuma subclasse nova
para cada combinação possível.

### Como o código funciona

`Personagem` é a interface base que define o contrato: todo personagem deve
ter uma descrição, um valor de vida e um valor de ataque.

```python
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
```

`Guerreiro` é o personagem base concreto, sem nenhum equipamento.

```python
class Guerreiro(Personagem):
    def descricao(self) -> str:
        return "Guerreiro"

    def vida(self) -> int:
        return 100

    def ataque(self) -> int:
        return 10
```

`DecoradorEquipamento` é a classe base de todos os decorators. Ela recebe
qualquer objeto do tipo `Personagem`, guarda a referência e repassa todas
as chamadas para ele. Sozinha não adiciona nada, mas serve de estrutura
para os equipamentos concretos.

```python
class DecoradorEquipamento(Personagem):
    def __init__(self, personagem: Personagem):
        self._personagem = personagem

    def descricao(self) -> str:
        return self._personagem.descricao()

    def vida(self) -> int:
        return self._personagem.vida()

    def ataque(self) -> int:
        return self._personagem.ataque()
```

Cada equipamento concreto sobrescreve apenas os atributos que modifica,
chamando o objeto interno e somando sua contribuição.

```python
class Espada(DecoradorEquipamento):
    def descricao(self) -> str:
        return self._personagem.descricao() + " com espada"

    def ataque(self) -> int:
        return self._personagem.ataque() + 25
```

No código cliente, os equipamentos são empilhados um sobre o outro. Cada
chamada percorre todas as camadas de fora para dentro, acumulando os atributos.

```python
personagem = Guerreiro()
personagem = Espada(personagem)
personagem = Armadura(personagem)
personagem = Amuleto(personagem)
```

### Como executar

```bash
python3 estrutural-decorator/decorator.py
```

### Saída esperada

```
Guerreiro
  Vida: 100 | Ataque: 10
Guerreiro com espada
  Vida: 100 | Ataque: 35
Guerreiro com armadura
  Vida: 150 | Ataque: 35
Guerreiro com amuleto
  Vida: 180 | Ataque: 45
```

![Jogo da Cobrinha em Python - Lógica de Programação e Biblioteca Curses](https://github.com/ryanvmorais/python-jogo-da-cobrinha/blob/main/assets/jogo-da-cobrinha-python.png?raw=true)

# 🐍 Jogo da Cobrinha em Python | Exercício de Lógica de Programação

![Python](https://img.shields.io/badge/Python-3.12+-3776AB?logo=python&logoColor=white)
![deps](https://img.shields.io/badge/deps-uv-DE5FE9)
[![CI](https://github.com/ryanvmorais/python-jogo-da-cobrinha/actions/workflows/ci.yml/badge.svg)](https://github.com/ryanvmorais/python-jogo-da-cobrinha/actions/workflows/ci.yml)
![Lint](https://img.shields.io/badge/lint-ruff-261230)
![Format](https://img.shields.io/badge/style-black-000000)
![Types](https://img.shields.io/badge/types-mypy%20strict-2A6DB2)
![License](https://img.shields.io/badge/license-MIT-green)

Este repositório contém o clássico **Jogo da Cobrinha (Snake Game)** desenvolvido em Python, projetado especificamente como um material de estudo para desenvolvedores iniciantes. O foco principal é a aplicação de **lógica de movimento**, manipulação de listas dinâmicas e o uso da biblioteca `curses` para interfaces de terminal.

### 🎯 Objetivo do Projeto:
Demonstrar a aplicação de **estruturas de dados (listas)**, **controle de eventos em tempo real** e **modularização de funções**. É um projeto prático ideal para estudantes que desejam entender como jogos baseados em coordenadas e ciclos de atualização (*game loops*) funcionam.

---

### 📚 O que você vai aprender com este projeto?
Este exercício foi estruturado para consolidar conceitos essenciais de algoritmos:

*   **Manipulação de Listas:** Uso de `insert` e `pop` para simular o movimento e o crescimento do corpo da cobra.
*   **Controle de Fluxo e Tempo:** Gerenciamento da velocidade do jogo e captura de teclas sem interromper a execução (`timeout`).
*   **Lógica de Coordenadas:** Como gerenciar posições `[y, x]` dentro de um plano cartesiano delimitado por bordas.
*   **Biblioteca Curses:** Manipulação avançada do terminal para criar janelas, bordas e desenhar caracteres em posições específicas.
*   **Modularização:** Organização do código em funções com responsabilidades únicas (S.O.L.I.D. para iniciantes).

---
### 🧠 Guia de Implementação (A Lógica por trás do Código):
Para quem está começando, o maior desafio não é a sintaxe, mas a **montagem do raciocínio**. Confira o passo a passo da construção deste jogo:
1. **Modelagem Dinâmica do Corpo:** A cobra não é um objeto único, mas uma **lista de coordenadas** `[[y, x], [y, x]]`. A "cabeça" é sempre o primeiro item (índice `0`), e o restante da lista forma o rastro que chamamos de corpo.
2. **A Matemática do Movimento:** Em vez de "empurrar" cada gomo da cobra, usamos um truque lógico: em cada turno, calculamos e inserimos uma **nova cabeça** na direção escolhida. Se a cobra não comer nada, removemos o último item da lista (a cauda). Essa troca constante cria a ilusão de movimento.
3. **Detecção de Colisões:** O sistema monitora a coordenada da cabeça em tempo real. Se ela for igual aos limites da borda (`y <= 0` ou `x >= largura`) ou se coincidir com qualquer coordenada que já exista na lista do corpo, o jogo identifica o impacto e encerra a partida.
4. **Ecossistema e Alimentação:** Utilizamos a biblioteca `random` para sortear posições para a fruta. Quando a cabeça ocupa a mesma posição da fruta, o sistema incrementa a pontuação e **não remove a cauda** naquele turno, resultando no crescimento natural da cobra.
5. **Prevenção de Movimento Oposto:** Para evitar o "suicídio lógico", implementamos uma trava que impede a cobra de virar 180° instantaneamente (ex: tentar ir para cima quando já está indo para baixo). O comando só é aceito se for uma curva lateral.
6. **O Coração do Jogo (Game Loop):** Um loop `while True` coordena o tempo do jogo. Ele limpa a tela, desenha os atores (caracteres `ASCII`), processa a entrada do teclado e aguarda alguns milissegundos antes de repetir tudo, garantindo que o jogo não rode rápido demais para o olho humano.
7. **Abstração com Funções:** O código é dividido em funções especialistas (como `mover_cobra` e `verificar_colisao`), facilitando a manutenção e permitindo que você entenda o papel de cada peça no funcionamento global do sistema.

---

### 🛠️ Tecnologias e Ferramentas:
Para garantir a melhor experiência de aprendizado e a execução correta de todos os recursos (como a limpeza de tela automática), o projeto utiliza as seguintes tecnologias:


| Ferramenta | Descrição | Badge |
| :--- | :--- | :--- |
| **Python 3** | Linguagem principal utilizada no desenvolvimento do algoritmo. | ![Linguagem Python](https://img.shields.io/badge/-Python-3776AB%3Fstyle%3Dflat%26logo%3Dpython?logo=python&logoColor=3776AB&logoSize=flat&color=F0F0F0) |
| **uv** | Gerenciador de ambiente e dependências (substitui `pip` + `venv`); resolve o `windows-curses` automaticamente no Windows. | ![uv](https://img.shields.io/badge/uv-DE5FE9?style=flat&logo=uv&logoColor=white) |
| **pytest** | Framework de testes automatizados usado em `tests/test_main.py`. | ![pytest](https://img.shields.io/badge/pytest-0A9EDC?style=flat&logo=pytest&logoColor=white) |
| **Ruff / Black / Mypy** | Lint, formatação e checagem de tipos (portão de qualidade do projeto). | ![Ruff](https://img.shields.io/badge/Ruff-D7FF64?style=flat&logo=ruff&logoColor=black) |
| **Terminal** | Interface onde o jogo é executado e processa a entrada do usuário. | ![Terminal](https://img.shields.io/badge/Terminal-241F31?style=flat&logo=gnometerminal&logoColor=241F31&color=F0F0F0) |
| **VS Code / PyCharm** | IDEs recomendadas para edição, depuração e refatoração do arquivo `main.py`. | ![PyCharm](https://img.shields.io/badge/PyCharm-pycharm?style=flat&logo=pycharm&logoColor=000000&color=F0F0F0) |

---

### ✅ Requisitos Mínimos:

Para garantir que o jogo funcione corretamente, certifique-se de ter os seguintes itens instalados:

- **Python 3.12 ou superior:** O código utiliza recursos modernos da linguagem.
- **[uv](https://docs.astral.sh/uv/) (recomendado):** Gerencia o ambiente e instala o `windows-curses` automaticamente no Windows. Sem ele, o jogo ainda roda com `python main.py`, mas quem estiver no Windows precisa instalar o `windows-curses` manualmente (`pip install windows-curses`) — em Linux/macOS o `curses` já vem na biblioteca padrão.
- **VS Code / PyCharm (Opcional):** Recomendado para abrir e editar o arquivo `main.py` com suporte total a refatoração e depuração.

> **Dica:** Para uma melhor experiência visual, execute o jogo diretamente no terminal do seu sistema (`Prompt de Comando` ou `PowerShell`).

---

### ⚙️ Como Executar o Projeto:
1. **Clone o repositório:**
   ```bash
   git clone https://github.com/ryanvmorais/python-jogo-da-cobrinha.git
   ``` 
2. **Execute o script:**
- Navegue até a **pasta do projeto** e utilize o comando abaixo no seu terminal (CMD, PowerShell ou Terminal do VS Code/PyCharm):
   ```bash
   uv run main.py
   ```
   Sem o `uv` instalado, `python main.py` funciona igual — no Windows,
   instale antes o `windows-curses` com `pip install windows-curses`.
> **Nota:** O jogo utiliza a biblioteca `curses` para gerenciar a interface do terminal de forma nativa e eficiente.
---
### ▶️ Execução Simplificada (Atalhos):
Para facilitar o acesso de quem está começando, adicionei scripts de inicialização automática. Basta baixar o projeto e:
   * **No Windows:** Dê dois cliques no arquivo `iniciar_jogo.bat`.
   * **No Linux/macOS:** Execute o arquivo `iniciar_jogo.sh` no terminal.

*Esses scripts detectam automaticamente se você tem `uv` (preferido) ou `python`/`python3` instalado antes de iniciar a partida.*

---

### 🧪 Testes e qualidade:

O projeto tem uma suíte de testes automatizados (`pytest`) e um portão de
qualidade que roda no CI a cada push/PR:

```bash
uv sync              # instala o grupo de desenvolvimento (ruff, black, mypy, pytest)
uv run pytest        # roda a suíte de testes
uv run ruff check .  # lint
uv run black --check .  # formatação
uv run mypy          # checagem de tipos
```

> Para quem quer entender o raciocínio por trás de cada ferramenta da
> stack, veja [`docs/stack.md`](docs/stack.md). Para o detalhamento
> completo do comportamento do jogo (requisitos, design, decisões), veja
> [`specs/001-jogo-da-cobrinha/`](specs/001-jogo-da-cobrinha/requirements.md).
> Para orientações de desenvolvimento voltadas a um agente de IA
> trabalhando neste repositório, veja [`CLAUDE.md`](CLAUDE.md).

---
### 📋 Atividade para praticar:

Para exercitar o que aprendeu, tente modificar o código e implementar estas novas funcionalidades:

1. **🏆 Sistema de Recorde (Persistência de Dados):**

Atualmente, a pontuação é reiniciada toda vez que o programa fecha. O desafio é criar uma "memória permanente" para o jogo:
   * **O Conceito:** Utilize as funções de manipulação de arquivos do Python (`open`, `read`, `write`).
   * **A Lógica:** Ao iniciar o jogo, o programa lê um arquivo chamado `recorde.txt`. Se a pontuação atual ultrapassar o valor lido, o jogo deve sobrescrever o arquivo com o novo recorde antes de encerrar.
   * **O Aprendizado:** Você aprenderá a salvar dados fisicamente no computador (`HD/SSD`), garantindo que o recorde persista mesmo após desligar a máquina.
2. **🍎 Frutas Especiais:** Crie uma fruta "dourada" que aparece raramente e dá 5 pontos de uma vez.
3. **🔳 Atravesar Paredes:** Altere a lógica de colisão para que, ao bater na borda direita, a cobra reapareça na borda esquerda.

---

### 🎮 Continue praticando

Este projeto faz parte de uma série de exercícios de lógica de programação em Python. Depois deste, experimente:

* **[Jogo da Velha em Python](https://github.com/ryanvmorais/python-jogo-da-velha):** Matrizes e Programação Orientada a Objetos.
* **[Calculadora Simples em Python](https://github.com/ryanvmorais/python-calculadora-simples):** Dicionários e tratamento de erros.
* **[Pedra, Papel e Tesoura em Python](https://github.com/ryanvmorais/python-pedra-papel-tesoura):** Dicionários e POO.

Veja todos os projetos e vídeos do canal em [aprenda-com-ryan-morais](https://github.com/ryanvmorais/aprenda-com-ryan-morais).

---

### 💡 Ficou com alguma dúvida ou tem sugestões?

Aprender algo novo tem seus desafios, mas estou aqui para caminharmos juntos! Se você encontrou algum erro, teve dificuldade em rodar o jogo ou pensou em uma funcionalidade incrível para adicionar:

*   **Abra uma [Issue](https://github.com/ryanvmorais/python-jogo-da-cobrinha/issues):** Clique no link e descreva sua dúvida ou sugestão. É a melhor forma de trocarmos conhecimento e ajudarmos outras pessoas que tenham a mesma dúvida!
*   **Me mande um E-mail:** Se preferir algo mais privado, pode me escrever em [**contato@ryanmorais.com.br**](mailto:contato@ryanmorais.com.br).

Ficarei muito feliz em ver seu progresso e receber seu feedback para melhorar cada vez mais nossos materiais de estudo! 🤝

---

### ⚖️ Licença

Este projeto está sob a **Licença MIT**. Isso significa que você pode usar, copiar e modificar o código à vontade, inclusive para seus próprios projetos. Para mais detalhes, consulte o arquivo [LICENSE](LICENSE).

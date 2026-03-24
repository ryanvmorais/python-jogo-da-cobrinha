![Jogo da Cobrinha em Python - Lógica de Programação e Matrizes](https://github.com/ryanvmorais/python-jogo-da-cobrinha/blob/main/assets/jogo-da-cobrinha-python.png?raw=true)

# 🐍 Jogo da Cobrinha em Python | Exercício de Lógica de Programação

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
### 🧠 Guia de Implementação: A Lógica por trás do Código
Para quem está começando, o maior desafio não é a sintaxe, mas a **montagem do raciocínio**. Confira o passo a passo da construção deste jogo:
1. **Modelagem do Corpo:** A cobra é uma lista de listas `[[y, x], [y, x]]`. A "cabeça" é sempre o primeiro item (índice 0).
2. **O Truque do Movimento:** Em cada turno, criamos uma "nova cabeça" na direção escolhida. Se a cobra não comer a fruta, removemos o último item da lista (a cauda). Isso cria a ilusão de movimento.
3. **Detecção de Colisão:** O sistema verifica constantemente se a coordenada da cabeça é igual a uma borda ou se a cabeça "encostou" em qualquer outra coordenada que já pertence ao corpo.
4. **Gerenciamento de Frutas:** Usamos a biblioteca `random` para gerar coordenadas aleatórias. Se a cabeça ocupar a mesma posição da fruta, a cobra "come", ganha ponto e a cauda não é removida, fazendo-a crescer.
5. **Prevenção de Movimento Oposto:** Implementamos uma lógica para impedir que a cobra vire 180° (ex: ir para cima quando está indo para baixo), o que causaria um "suicídio" imediato.
6. **O Game Loop:** Um loop `while True` limpa a tela, desenha os atores, processa a entrada do usuário e atualiza a posição da cobra em milissegundos.

---

### 🛠️ Tecnologias e Ferramentas:
Para garantir a melhor experiência de aprendizado e a execução correta de todos os recursos (como a limpeza de tela automática), o projeto utiliza as seguintes tecnologias:


| Ferramenta | Descrição | Selo |
| :--- | :--- | :--- |
| **Python 3** | Linguagem principal utilizada no desenvolvimento do algoritmo. | ![Linguagem Python](https://img.shields.io/badge/-Python-3776AB%3Fstyle%3Dflat%26logo%3Dpython?logo=python&logoColor=3776AB&logoSize=flat&color=F0F0F0) |
| **Terminal** | Interface onde o jogo é executado e processa a entrada do usuário. | ![Terminal](https://img.shields.io/badge/Terminal-241F31?style=flat&logo=gnometerminal&logoColor=241F31&color=F0F0F0) |
| **VS Code / PyCharm** | IDEs recomendadas para edição, depuração e refatoração do arquivo `main.py`. | ![PyCharm](https://img.shields.io/badge/PyCharm-pycharm?style=flat&logo=pycharm&logoColor=000000&color=F0F0F0) |

---

### ✅ Requisitos Mínimos:

Para garantir que o jogo funcione corretamente, certifique-se de ter os seguintes itens instalados:

- **Python 3.10 ou superior:** O código utiliza recursos modernos da linguagem.
- **Suporte a Curses:** No Windows, é necessário instalar o pacote windows-curses (incluído no `requirements.txt`).
- **VS Code / PyCharm (Opcional):** Recomendado para abrir e editar o arquivo `main.py` com suporte total a refatoração e depuração.

> **Dica:** Para uma melhor experiência visual, execute o jogo diretamente no terminal do seu sistema (`Prompt de Comando` ou `PowerShell`).

---

### ⚙️ Como Executar o Projeto:
1. **Clone o repositório:**
   ```bash
   git clone https://github.com/ryanvmorais/python-jogo-da-cobrinha.git
   ``` 
2. **Instale as dependências:**
- Navegue até a **pasta do projeto** e utilize o comando abaixo no seu terminal (CMD, PowerShell ou Terminal do VS Code/PyCharm):
   ```bash
   pip install -r requirements.txt
   ```
3. **Execute o script:**
- Navegue até a **pasta do projeto** e utilize o comando abaixo no seu terminal (CMD, PowerShell ou Terminal do VS Code/PyCharm):
   ```bash
   python main.py
   ```
> **Nota:** O jogo utiliza a biblioteca `curses` para gerenciar a interface do terminal de forma nativa e eficiente.
---

### 📋 Atividade para praticar:

Para exercitar o que aprendeu, tente modificar o código e implementar estas novas funcionalidades:

1. **🏆 Sistema de Recorde:** Salve a maior pontuação em um arquivo `.txt` para que ela persista mesmo após fechar o jogo.
2. **🍎 Frutas Especiais:** Crie uma fruta "dourada" que aparece raramente e dá 5 pontos de uma vez.
3. **🔳 Atravesar Paredes:** Altere a lógica de colisão para que, ao bater na borda direita, a cobra reapareça na borda esquerda.

---

### 💡 Ficou com alguma dúvida ou tem sugestões?

Aprender algo novo tem seus desafios, mas estou aqui para caminharmos juntos! Se você encontrou algum erro, teve dificuldade em rodar o jogo ou pensou em uma funcionalidade incrível para adicionar:

*   **Abra uma [Issue](https://github.com/ryanvmorais/python-jogo-da-cobrinha/issues):** Clique no link e descreva sua dúvida ou sugestão. É a melhor forma de trocarmos conhecimento e ajudarmos outras pessoas que tenham a mesma dúvida!
*   **Me mande um E-mail:** Se preferir algo mais privado, pode me escrever em [**contato@ryanmorais.com.br**](mailto:contato@ryanmorais.com.br).

Ficarei muito feliz em ver seu progresso e receber seu feedback para melhorar cada vez mais nossos materiais de estudo! 🤝

---

### ⚖️ Licença

Este projeto está sob a **Licença MIT**. Isso significa que você pode usar, copiar e modificar o código à vontade, inclusive para seus próprios projetos, desde que mantenha os créditos originais. Para mais detalhes, consulte o arquivo [LICENSE](LICENSE).

# 🤝 Como Contribuir no Jogo da Cobrinha

Este repositório é um espaço dedicado ao aprendizado de Python, Manipulação de Coordenadas e o uso da biblioteca **Curses** para interfaces de terminal. Sua colaboração é fundamental para fortalecer este material didático para a comunidade de desenvolvedores!

## 🚀 O que você pode fazer?

1.  **Refinamento de Lógica:** Sugira melhorias no sistema de colisão ou na lógica de crescimento da cobra (listas e coordenadas).
2.  **Novas Funcionalidades:** 
    *   Implemente um sistema de **Recorde Máximo** (High Score) que persista em um arquivo `.txt`.
    *   Adicione "frutas especiais" que dão mais pontos ou alteram a velocidade temporariamente.
3.  **Interface e UX:** 
    *   Melhore as bordas do campo utilizando caracteres diferentes da biblioteca Curses.
    *   Adicione uma tela de "Pause" ou um menu inicial mais elaborado.
4.  **Documentação:** Enriqueça as Docstrings das funções ou melhore as explicações sobre como o sistema de coordenadas `(y, x)` do Curses difere do padrão matemático tradicional no README.

## 🛠️ Como enviar sua sugestão

1.  Faça o **Fork** do projeto para sua conta pessoal.
2.  Crie uma branch específica para sua modificação: `git checkout -b feature/nome-da-melhoria`.
3.  Realize seus commits seguindo o padrão **Conventional Commits** (ex: `feat:`, `fix:`, `docs:`).
4.  Envie suas alterações para o seu fork: `git push origin feature/nome-da-melhoria`.
5.  Abra um **Pull Request** detalhando tecnicamente o que foi alterado e o impacto pedagógico da mudança.

## 📜 Diretrizes do Projeto
- O código deve seguir o padrão de **Funções Modulares** e nomes autoexplicativos já estabelecido.
- Mantenha a **coerência na nomenclatura** das variáveis (sempre em português e seguindo o padrão snake_case).
- O objetivo principal é a **didática**: o uso da biblioteca `curses` pode ser desafiador para iniciantes, então mantenha os comentários claros e simples.


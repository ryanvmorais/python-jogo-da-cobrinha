"""Jogo da Cobrinha (Snake Game) em Python com curses — projeto educacional.

Material de estudo para prática de lógica de programação, manipulação de
listas dinâmicas e uso da biblioteca `curses` para interfaces de terminal.

ESTRUTURA DO CÓDIGO:
1. CONFIGURAÇÃO E INTERFACE: Funções que preparam a tela e desenham os elementos.
2. LÓGICA DE MOVIMENTAÇÃO: Regras de direção e como a cobra se desloca.
3. REGRAS DE NEGÓCIO (COLISÕES): Verificações de vitória, derrota e pontuação.
4. LOOP PRINCIPAL (CORE): Onde todas as funções se unem para rodar o jogo.
"""

from __future__ import annotations

import curses
import random
import sys
import time

# No Windows, stdout sem console UTF-8 (saída redirecionada/pipe, alguns
# executores de CI) cai para cp1252 e quebra o emoji de aviso abaixo com
# UnicodeEncodeError; reconfigurar para UTF-8 evita o crash em qualquer
# ambiente. Afeta só a seleção de dificuldade — roda antes do curses.wrapper
# assumir o terminal.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# Velocidade do jogo por nível de dificuldade, em milissegundos de espera
# entre quadros (timeout do curses) — quanto menor, mais rápida a cobra.
NIVEIS_DIFICULDADE = {
    "1": 1000,
    "2": 500,
    "3": 150,
    "4": 90,
    "5": 35,
}

# Teclas de seta aceitas como direção; qualquer outra tecla é ignorada.
DIRECOES_VALIDAS = [curses.KEY_UP, curses.KEY_LEFT, curses.KEY_DOWN, curses.KEY_RIGHT]

# Mapeia cada direção para a oposta a ela — usado para travar o "suicídio"
# de virar 180° instantaneamente. Constante de módulo: recriar o dict a
# cada quadro (chamado dezenas de vezes por segundo nas dificuldades mais
# altas) seria trabalho redundante.
DIRECOES_OPOSTAS = {
    curses.KEY_UP: curses.KEY_DOWN,
    curses.KEY_DOWN: curses.KEY_UP,
    curses.KEY_LEFT: curses.KEY_RIGHT,
    curses.KEY_RIGHT: curses.KEY_LEFT,
}


# ---------------------------------------------------------------------------
# Configuração e interface
# ---------------------------------------------------------------------------


def selecionar_nivel_dificuldade() -> int:
    """Define a velocidade do jogo (tempo de espera em milissegundos).

    Returns:
        int: Tempo de espera entre quadros, em milissegundos, de acordo com
            o nível escolhido (``NIVEIS_DIFICULDADE``).
    """
    while True:
        resposta = input("Escolha a dificuldade de 1 a 5 (1=Fácil, 5=Difícil): \n")
        velocidade = NIVEIS_DIFICULDADE.get(resposta)
        if velocidade:
            return velocidade
        print("⚠️ Por favor, escolha um número entre 1 e 5.")


def desenhar_tela(janela: curses.window) -> None:
    """Limpa a tela e desenha as bordas do campo de jogo.

    Args:
        janela (curses.window): Janela curses a redesenhar.
    """
    janela.clear()
    janela.border()


def desenhar_ator(ator: list[int], janela: curses.window, caractere: str) -> None:
    """Desenha um objeto (cobra ou fruta) em uma coordenada específica da tela.

    Args:
        ator (list[int]): Coordenada ``[y, x]`` onde desenhar.
        janela (curses.window): Janela curses onde o caractere é escrito.
        caractere (str): Caractere ASCII a desenhar na posição.
    """
    janela.addch(ator[0], ator[1], caractere)


def desenhar_cobra(cobra: list[list[int]], janela: curses.window) -> None:
    """Diferencia visualmente a cabeça (``@``) do restante do corpo (``#``).

    Args:
        cobra (list[list[int]]): Coordenadas ``[y, x]`` da cobra; o primeiro
            item é a cabeça, os demais formam o corpo.
        janela (curses.window): Janela curses onde a cobra é desenhada.
    """
    # Desenha a cabeça (primeiro item da lista)
    desenhar_ator(ator=cobra[0], janela=janela, caractere="@")
    # Desenha cada gomo do corpo (do segundo item em diante)
    for parte in cobra[1:]:
        desenhar_ator(ator=parte, janela=janela, caractere="#")


# ---------------------------------------------------------------------------
# Lógica de movimentação
# ---------------------------------------------------------------------------


def gerar_nova_fruta(janela: curses.window) -> list[int]:
    """Sorteia uma posição aleatória para a fruta dentro das bordas.

    Args:
        janela (curses.window): Janela curses; usada para descobrir os
            limites (``getmaxyx``) dentro dos quais a fruta pode aparecer.

    Returns:
        list[int]: Coordenada ``[y, x]`` sorteada, sempre longe das bordas.
    """
    altura, largura = janela.getmaxyx()
    return [random.randint(1, altura - 2), random.randint(1, largura - 2)]


def obter_nova_direcao(janela: curses.window, tempo_espera: int) -> int | None:
    """Captura a tecla pressionada pelo usuário dentro do tempo limite.

    Args:
        janela (curses.window): Janela curses de onde a tecla é lida.
        tempo_espera (int): Tempo máximo de espera, em milissegundos, antes
            de ``getch`` retornar sem tecla.

    Returns:
        int | None: O código da tecla de direção pressionada, ou ``None`` se
            nenhuma tecla de direção válida foi capturada a tempo.
    """
    janela.timeout(tempo_espera)
    tecla = janela.getch()
    return tecla if tecla in DIRECOES_VALIDAS else None


def direcao_e_oposta(direcao: int, direcao_atual: int) -> bool:
    """Impede que a cobra 'atropele' o próprio pescoço ao tentar voltar.

    Args:
        direcao (int): Nova direção pretendida (tecla ``curses.KEY_*``).
        direcao_atual (int): Direção em que a cobra já está se movendo.

    Returns:
        bool: ``True`` se ``direcao`` for exatamente o oposto de
            ``direcao_atual``.
    """
    return DIRECOES_OPOSTAS.get(direcao) == direcao_atual


def mover_cobra(cobra: list[list[int]], direcao: int, cobra_comeu_fruta: bool) -> None:
    """Cria uma nova cabeça na direção escolhida e remove a cauda se não comeu.

    Args:
        cobra (list[list[int]]): Coordenadas da cobra, modificada in-place
            (nova cabeça inserida no início).
        direcao (int): Direção do movimento (tecla ``curses.KEY_*``).
        cobra_comeu_fruta (bool): Se ``True``, a cauda não é removida — a
            cobra cresce um segmento.
    """
    nova_cabeca = cobra[0].copy()

    # Atualiza a posição baseada na tecla
    if direcao == curses.KEY_UP:
        nova_cabeca[0] -= 1
    if direcao == curses.KEY_DOWN:
        nova_cabeca[0] += 1
    if direcao == curses.KEY_LEFT:
        nova_cabeca[1] -= 1
    if direcao == curses.KEY_RIGHT:
        nova_cabeca[1] += 1

    cobra.insert(0, nova_cabeca)  # Adiciona nova posição na frente
    if not cobra_comeu_fruta:
        cobra.pop()  # Remove a cauda para manter o tamanho


# ---------------------------------------------------------------------------
# Verificações de fim de jogo
# ---------------------------------------------------------------------------


def verificar_colisoes(cobra: list[list[int]], janela: curses.window) -> bool:
    """Centraliza os testes de colisão (borda e corpo).

    Args:
        cobra (list[list[int]]): Coordenadas da cobra; o primeiro item é a
            cabeça.
        janela (curses.window): Janela curses; usada para descobrir os
            limites (``getmaxyx``) que definem a borda.

    Returns:
        bool: ``True`` se a cabeça bateu na borda ou em qualquer gomo do
            próprio corpo.
    """
    altura, largura = janela.getmaxyx()
    cabeca = cobra[0]

    # Bateu na borda?
    bateu_borda_vertical = cabeca[0] <= 0 or cabeca[0] >= altura - 1
    bateu_borda_horizontal = cabeca[1] <= 0 or cabeca[1] >= largura - 1
    if bateu_borda_vertical or bateu_borda_horizontal:
        return True
    # Bateu em si mesma?
    if cabeca in cobra[1:]:
        return True
    return False


def finalizar_jogo(pontuacao: int, janela: curses.window) -> None:
    """Exibe a mensagem final centralizada antes de fechar.

    Args:
        pontuacao (int): Número de frutas coletadas na partida.
        janela (curses.window): Janela curses onde a mensagem é desenhada.
    """
    altura, largura = janela.getmaxyx()
    texto = f" Fim de Jogo! Frutas coletadas: {pontuacao} "
    janela.addstr(altura // 2, (largura - len(texto)) // 2, texto, curses.A_REVERSE)
    janela.refresh()
    time.sleep(3)


# ---------------------------------------------------------------------------
# Loop principal
# ---------------------------------------------------------------------------


def ciclo_do_jogo(janela: curses.window, velocidade_jogo: int) -> None:
    """Roda uma partida completa, do estado inicial até a colisão fatal.

    Chamada por ``curses.wrapper``, que garante que o terminal volte ao
    normal mesmo se o código lançar uma exceção.

    Args:
        janela (curses.window): Janela curses fornecida pelo
            ``curses.wrapper``.
        velocidade_jogo (int): Tempo de espera entre quadros, em
            milissegundos (controla a dificuldade).
    """
    # Configurações iniciais do ambiente curses
    curses.curs_set(0)  # Esconde o cursor piscante

    # Estado inicial do jogo
    cobra = [[10, 15], [9, 15], [8, 15]]  # Começa com 3 segmentos
    fruta = gerar_nova_fruta(janela)
    direcao_atual = curses.KEY_DOWN
    pontuacao = 0

    while True:
        desenhar_tela(janela)
        desenhar_cobra(cobra, janela)
        desenhar_ator(fruta, janela, "*")

        # Gerenciamento de direção
        proxima = obter_nova_direcao(janela, velocidade_jogo)
        if proxima and not direcao_e_oposta(proxima, direcao_atual):
            direcao_atual = proxima

        # Lógica de alimentação
        comeu = cobra[0] == fruta
        if comeu:
            pontuacao += 1
            fruta = gerar_nova_fruta(janela)

        mover_cobra(cobra, direcao_atual, comeu)

        # Verificação de derrota
        if verificar_colisoes(cobra, janela):
            break

    finalizar_jogo(pontuacao, janela)


if __name__ == "__main__":
    # O wrapper do curses garante que o terminal volte ao normal se o código der erro
    vel = selecionar_nivel_dificuldade()
    curses.wrapper(ciclo_do_jogo, velocidade_jogo=vel)

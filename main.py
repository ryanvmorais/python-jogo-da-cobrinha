"""
🐍 PROJETO: JOGO DA COBRINHA (SNAKE GAME)
🎯 Objetivo: Educacional - Prática de Lógica com Python e Biblioteca Curses.

ESTRUTURA DO CÓDIGO:
1. CONFIGURAÇÃO E INTERFACE: Funções que preparam a tela e desenham os elementos.
2. LÓGICA DE MOVIMENTAÇÃO: Regras de direção e como a cobra se desloca.
3. REGRAS DE NEGÓCIO (COLISÕES): Verificações de vitória, derrota e pontuação.
4. LOOP PRINCIPAL (CORE): Onde todas as funções se unem para rodar o jogo.
"""

import curses
import random
import time

# --- Funções de Configuração e Interface ---

def selecionar_nivel_dificuldade():
    """ Define a velocidade do jogo (tempo de espera em milissegundos). """
    niveis_dificuldade = {
        '1': 1000, '2': 500, '3': 150, '4': 90, '5': 35,
    }
    while True:
        resposta = input('Escolha a dificuldade de 1 a 5 (1=Fácil, 5=Difícil): \n')
        velocidade = niveis_dificuldade.get(resposta)
        if velocidade:
            return velocidade
        print('⚠️ Por favor, escolha um número entre 1 e 5.')

def desenhar_tela(janela):
    """ Limpa a tela e desenha as bordas do campo de jogo. """
    janela.clear()
    janela.border()

def desenhar_ator(ator, janela, caractere):
    """ Desenha um objeto (cobra ou fruta) em uma coordenada específica da tela. """
    janela.addch(ator[0], ator[1], caractere)

def desenhar_cobra(cobra, janela):
    """ Diferencia visualmente a cabeça (@) do restante do corpo (#). """
    # Desenha a cabeça (primeiro item da lista)
    desenhar_ator(ator=cobra[0], janela=janela, caractere='@')
    # Desenha cada gomo do corpo (do segundo item em diante)
    for parte in cobra[1:]:
        desenhar_ator(ator=parte, janela=janela, caractere='#')

# --- Funções de Lógica e Movimentação ---

def gerar_nova_fruta(janela):
    """ Sorteia uma posição aleatória para a fruta dentro das bordas. """
    altura, largura = janela.getmaxyx()
    return [random.randint(1, altura-2), random.randint(1, largura-2)]

def obter_nova_direcao(janela, tempo_espera):
    """ Captura a tecla pressionada pelo usuário dentro do tempo limite. """
    janela.timeout(tempo_espera)
    tecla = janela.getch()
    direcoes_validas = [curses.KEY_UP, curses.KEY_LEFT, curses.KEY_DOWN, curses.KEY_RIGHT]
    return tecla if tecla in direcoes_validas else None

def direcao_e_oposta(direcao, direcao_atual):
    """ Impede que a cobra 'atropele' o próprio pescoço ao tentar voltar. """
    opostos = {
        curses.KEY_UP: curses.KEY_DOWN,
        curses.KEY_DOWN: curses.KEY_UP,
        curses.KEY_LEFT: curses.KEY_RIGHT,
        curses.KEY_RIGHT: curses.KEY_LEFT
    }
    return opostos.get(direcao) == direcao_atual

def mover_cobra(cobra, direcao, cobra_comeu_fruta):
    """ Cria uma nova cabeça na direção escolhida e remove a cauda se não comeu. """
    nova_cabeca = cobra[0].copy()
    
    # Atualiza a posição baseada na tecla
    if direcao == curses.KEY_UP:    nova_cabeca[0] -= 1
    if direcao == curses.KEY_DOWN:  nova_cabeca[0] += 1
    if direcao == curses.KEY_LEFT:  nova_cabeca[1] -= 1
    if direcao == curses.KEY_RIGHT: nova_cabeca[1] += 1
    
    cobra.insert(0, nova_cabeca) # Adiciona nova posição na frente
    if not cobra_comeu_fruta:
        cobra.pop() # Remove a cauda para manter o tamanho

# --- Verificações de Fim de Jogo ---

def verificar_colisoes(cobra, janela):
    """ Centraliza os testes de colisão (borda e corpo). """
    altura, largura = janela.getmaxyx()
    cabeca = cobra[0]
    
    # Bateu na borda?
    if cabeca[0] <= 0 or cabeca[0] >= altura-1 or cabeca[1] <= 0 or cabeca[1] >= largura-1:
        return True
    # Bateu em si mesma?
    if cabeca in cobra[1:]:
        return True
    return False

def finalizar_jogo(pontuacao, janela):
    """ Exibe a mensagem final centralizada antes de fechar. """
    altura, largura = janela.getmaxyx()
    texto = f' Fim de Jogo! Frutas coletadas: {pontuacao} '
    janela.addstr(altura // 2, (largura - len(texto)) // 2, texto, curses.A_REVERSE)
    janela.refresh()
    time.sleep(3)

# --- Loop Principal ---

def ciclo_do_jogo(janela, velocidade_jogo):
    # Configurações iniciais do ambiente curses
    curses.curs_set(0) # Esconde o cursor piscante
    
    # Estado inicial do jogo
    cobra = [[10, 15], [9, 15], [8, 15]] # Começa com 3 segmentos
    fruta = gerar_nova_fruta(janela)
    direcao_atual = curses.KEY_DOWN
    pontuacao = 0

    while True:
        desenhar_tela(janela)
        desenhar_cobra(cobra, janela)
        desenhar_ator(fruta, janela, '*')
        
        # Gerenciamento de direção
        proxima = obter_nova_direcao(janela, velocidade_jogo)
        if proxima and not direcao_e_oposta(proxima, direcao_atual):
            direcao_atual = proxima
            
        # Lógica de alimentação
        comeu = (cobra[0] == fruta)
        if comeu:
            pontuacao += 1
            fruta = gerar_nova_fruta(janela)
            
        mover_cobra(cobra, direcao_atual, comeu)
        
        # Verificação de derrota
        if verificar_colisoes(cobra, janela):
            break
            
    finalizar_jogo(pontuacao, janela)

if __name__ == '__main__':
    # O wrapper do curses garante que o terminal volte ao normal se o código der erro
    vel = selecionar_nivel_dificuldade()
    curses.wrapper(ciclo_do_jogo, velocidade_jogo=vel)

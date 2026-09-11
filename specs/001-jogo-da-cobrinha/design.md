---
feature: Jogo da Cobrinha (Snake) via terminal com curses
status: concluído
data: 2026-09-11
relacionado:
  - 001-jogo-da-cobrinha/requirements.md
origem: engenharia reversa
---

# 001 — Jogo da Cobrinha — design

## Visão geral da abordagem

Um único módulo (`main.py`), sem classe — o estado do jogo (cobra, fruta,
direção, pontuação) vive em variáveis locais de `ciclo_do_jogo`, e cada
responsabilidade (desenhar, mover, verificar colisão) é uma função pura ou
quase pura que recebe a `curses.window` como parâmetro em vez de guardar
estado global. `curses.wrapper` chama `ciclo_do_jogo`, garantindo que o
terminal volte ao normal mesmo se o código lançar uma exceção.

Não há camadas (persistência, rede, UI gráfica) — é intencional: o
projeto é didático e o objetivo é que o game loop caiba na cabeça em uma
leitura.

## Layout de módulos

```
main.py            # todas as funções do jogo + ciclo_do_jogo (ponto de entrada)
tests/test_main.py # suíte pytest, com uma curses.window falsa (_FakeJanela)
```

## Modelo de dados

- `cobra: list[list[int]]` — lista de coordenadas `[y, x]`; o primeiro
  item é a cabeça, os demais formam o corpo, na ordem em que foram
  ocupados.
- `fruta: list[int]` — coordenada `[y, x]` da fruta atual.
- `direcao_atual: int` — uma constante `curses.KEY_*`.
- `pontuacao: int` — frutas coletadas na partida.

Constantes de módulo:

- `NIVEIS_DIFICULDADE: dict[str, int]` — mapeia a resposta digitada
  (`"1"`-`"5"`) para o tempo de espera entre quadros, em milissegundos.
- `DIRECOES_VALIDAS: list[int]` — as quatro teclas de seta aceitas.
- `DIRECOES_OPOSTAS: dict[int, int]` — mapeia cada direção para a oposta.

## Componentes

### `selecionar_nivel_dificuldade`

Loop de leitura: pede um número de `1` a `5`, consulta
`NIVEIS_DIFICULDADE`. Repete em caso de resposta fora do mapa — nunca
deixa uma exceção subir. Roda antes do `curses.wrapper`, em modo texto
normal (`input`/`print`).

### `desenhar_tela` / `desenhar_ator` / `desenhar_cobra`

Funções de desenho puras em relação ao estado do jogo: recebem o que
desenhar e a `janela`, e só chamam métodos de curses (`clear`, `border`,
`addch`). `desenhar_cobra` desenha a cabeça com `@` e o resto do corpo com
`#`.

### `gerar_nova_fruta`

Sorteia uma coordenada com `random.randint`, usando `janela.getmaxyx()`
para descobrir os limites e manter a fruta longe da borda (`1` até
`altura-2`/`largura-2`).

### `obter_nova_direcao`

Configura `janela.timeout(tempo_espera)` (o "relógio" do jogo — cada
quadro dura esse tempo) e chama `janela.getch()`. Só retorna a tecla se
ela estiver em `DIRECOES_VALIDAS`; qualquer outra tecla (ou nenhuma,
quando o tempo se esgota) retorna `None`.

### `direcao_e_oposta`

Consulta `DIRECOES_OPOSTAS` para bloquear o "suicídio" de virar 180°
instantaneamente.

### `mover_cobra`

Calcula a nova cabeça somando o delta da direção à cabeça atual, insere no
início da lista e remove a cauda — exceto se a cobra comeu a fruta naquele
quadro, caso em que a cauda é preservada (a cobra cresce).

### `verificar_colisoes`

Centraliza os dois testes de derrota: cabeça fora dos limites internos do
campo (`<= 0` ou `>= altura-1`/`largura-1`), ou cabeça coincidindo com
qualquer gomo do corpo (`cabeca in cobra[1:]`).

### `finalizar_jogo`

Centraliza o texto "Fim de Jogo! Frutas coletadas: N" na janela
(`curses.A_REVERSE` para destaque), atualiza a tela (`refresh`) e aguarda
3 segundos (`time.sleep`) antes de retornar — dando tempo do jogador ler o
resultado antes do `curses.wrapper` restaurar o terminal.

### `ciclo_do_jogo`

Orquestra o loop principal: a cada iteração, desenha o quadro, lê a
direção, resolve a alimentação, move a cobra e verifica colisão — encerra
com `finalizar_jogo` quando `verificar_colisoes` retorna `True`.

## Interfaces

Nenhuma — programa de terminal sem rede, arquivo ou API. A "interface" é o
protocolo de teclado (setas) e a saída via `curses`, documentado nos
requisitos funcionais.

## ADRs

### ADR-1 — `NIVEIS_DIFICULDADE`, `DIRECOES_VALIDAS` e `DIRECOES_OPOSTAS` como constantes de módulo

**Decisão.** Os três dicionários/listas fixos (regras de dificuldade,
teclas válidas, pares de direção oposta) subiram para constantes de
módulo, em vez de serem recriados a cada chamada de função.

**Alternativas.** (a) manter os três locais às funções que os usam (como
estava).

**Porquê.** `DIRECOES_VALIDAS` e `DIRECOES_OPOSTAS` eram recriados dentro
de `obter_nova_direcao` e `direcao_e_oposta` — chamadas em **todo quadro**
do jogo (até ~28 vezes por segundo na dificuldade 5, `35ms` de timeout).
Recriar uma lista/dict fixo a essa frequência é trabalho redundante sem
motivo; como constante de módulo o valor também fica visível/documentável
fora da função que o usa (o mesmo raciocínio do
`REGRAS_VITORIA` no `pedra-papel-tesoura`, aqui ainda mais justificado
pela frequência de chamada).

**Trade-off.** Nenhum relevante — os três são fixos na prática (nada no
código escreve neles depois de definidos).

### ADR-2 — Reconfigurar `sys.stdout` para UTF-8 no import

**Decisão.** `main.py` chama `sys.stdout.reconfigure(encoding="utf-8",
errors="replace")` no nível do módulo, se o atributo existir.

**Alternativas.** (a) não fazer nada (comportamento original). (b) remover
o emoji da mensagem de aviso.

**Porquê.** Confirmado ao rodar `selecionar_nivel_dificuldade` com stdout
redirecionado no Windows durante esta modernização: ao digitar uma
dificuldade inválida, o `print` do aviso (`'⚠️ Por favor, escolha...'`)
lançava `UnicodeEncodeError`, porque sem console UTF-8 o Python cai para a
codepage do sistema (`cp1252`), que não tem esses caracteres. Essa etapa
roda **antes** do `curses.wrapper` assumir o terminal — é texto normal,
sujeito ao mesmo problema já documentado no `pedra-papel-tesoura`
(ADR-4 daquela spec). Descartar (a): é a causa raiz do crash. Descartar
(b): o emoji é parte da voz didática do projeto; removê-lo é perda maior
que o custo de uma linha de configuração.

**Trade-off.** `errors="replace"` troca um caractere não suportado por
`?` em vez de crashar — aceitável, pois a única saída que perderia
fidelidade é um terminal exótico que também não suporta UTF-8.

### ADR-3 — `windows-curses` como dependência condicional por `sys_platform`

**Decisão.** `pyproject.toml` declara `windows-curses>=2.4.1; sys_platform
== 'win32'` em `[project.dependencies]`.

**Alternativas.** (a) manter fora do manifesto e pedir `pip install` manual
(como no `requirements.txt` original). (b) declarar sem marcador de
plataforma.

**Porquê.** `uv sync` resolve o marcador de ambiente sozinho — instala
`windows-curses` só em Windows e nada em Linux/macOS (onde `curses` já é
stdlib e o pacote nem compila). Descartar (a): perde o lock e a
reprodutibilidade que motivou a migração para `uv` (ver `docs/stack.md`).
Descartar (b): instalaria (ou tentaria compilar) um pacote inútil e
potencialmente quebrado fora do Windows.

**Trade-off.** Nenhum relevante — é exatamente o que o marcador de
ambiente do PEP 508 foi desenhado para resolver.

### ADR-4 — Fake de `curses.window` nos testes, em vez de mockar `curses` inteiro

**Decisão.** `tests/test_main.py` define `_FakeJanela`, uma classe simples
que implementa `getmaxyx`, `addch`, `addstr`, `clear`, `border`,
`timeout`, `getch` e `refresh` registrando as chamadas, e passa essa
instância para as funções em vez de uma `curses.window` real.

**Alternativas.** (a) `unittest.mock.MagicMock()` genérico no lugar da
janela. (b) rodar os testes dentro de `curses.wrapper` com um terminal
real (pty). (c) não testar as funções que recebem `janela`.

**Porquê.** Um `MagicMock()` aceita qualquer chamada e não obriga a
assinatura correta dos métodos de `curses.window` — um teste passaria
mesmo se o código chamasse um método inexistente. Um `pty` real (b)
funciona, mas é frágil em CI e overkill para verificar coordenadas e
caracteres desenhados. A fake explícita é pequena, tipável (`mypy strict`
cobre `tests/`) e deixa claro, lendo a classe, exatamente quais métodos de
`curses.window` o jogo usa — documentação viva da superfície de API
consumida. Descartar (c): deixaria a maior parte da lógica do jogo sem
cobertura.

**Trade-off.** A fake não valida que os métodos batem com a assinatura
real de `curses.window` (não há checagem automática de compatibilidade);
se uma versão futura do `curses` mudar uma assinatura, só o smoke test
manual (rodar o jogo de verdade) pegaria a divergência.

## Impacto no código existente

Esta spec documenta a versão já modernizada de `main.py` (type hints,
`uv`, suíte de testes, constantes promovidas, bug de codificação
corrigido). Não há código legado para migrar — é a spec fundadora do
projeto.

## Estratégia de testes

Unitária, sem integração (não há rede nem arquivo, e `ciclo_do_jogo` não é
testado diretamente — ver a seção "Testes" de `requirements.md`).
`_FakeJanela` substitui toda `curses.window` real; `input()` é mockado via
`monkeypatch.setattr("builtins.input", ...)`; `random.randint` e
`time.sleep` são mockados quando o teste precisa de determinismo ou não
pode esperar segundos reais. Ver `tests/test_main.py`.

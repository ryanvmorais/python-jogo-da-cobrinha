# A stack, e por quê

Cada tecnologia que sustenta o Jogo da Cobrinha: o que faz, por que foi
escolhida contra a alternativa, e os conceitos que valem a pena estudar
primeiro se forem novos para você.

Não é exaustivo — o grafo completo de versões (runtime + grupo de
desenvolvimento) está travado no `uv.lock`. Este doc é o mapa: a *forma* do
projeto e o raciocínio por trás de cada peça.

O projeto é um único programa: um jogo de terminal desenhado com `curses`,
com uma dependência de runtime real (`windows-curses`, só no Windows) e um
grupo de ferramentas de qualidade por fora.

```
main.py  ──►  curses (stdlib no Linux/macOS; windows-curses no Windows)
         ──►  random, time, sys (biblioteca padrão)
```

---

## Linguagem e empacotamento

### Python 3.12+

A única linguagem do projeto. 3.12 é o piso porque é a versão mínima usada
nos outros projetos do Ryan (`hub-ryan-morais`, `webvigil`,
`pedra-papel-tesoura`) — manter o mesmo piso evita "funciona num projeto e
não no outro" por causa de sintaxe.

**Por que esta:** o projeto é puramente didático (lógica de movimento,
listas dinâmicas, coordenadas) — qualquer linguagem serviria, mas Python
tem a sintaxe mais direta para quem está aprendendo esses conceitos por
trás de um jogo de terminal.

**Estudar:** `list.insert`/`list.pop`, type hints modernos (`int | None`,
`list[list[int]]`), `if __name__ == "__main__"`.

### uv

O gerenciador de pacotes e ambientes virtuais do Python (da Astral, o time
do Ruff). Substitui `pip` + `venv` manual. `uv sync` instala a dependência
de runtime e o grupo de desenvolvimento a partir do `uv.lock`; `uv run
<comando>` executa dentro do ambiente sem precisar ativá-lo.

**Por que esta:** o projeto tem uma dependência de runtime condicional por
plataforma (`windows-curses`) além das ferramentas de qualidade — `uv`
resolve o marcador `sys_platform` automaticamente, é uma ordem de magnitude
mais rápido que `pip`/`venv`, usa o `pyproject.toml` padrão (PEP 621) e
gera um lockfile real (`uv.lock`) — o mesmo gerenciador usado nos outros
projetos Python do Ryan.

**Estudar:** `uv sync`, `uv run <comando>`, `uv add <pacote>`, `uv lock`, a
sintaxe de marcador de ambiente (`; sys_platform == 'win32'`) no
`pyproject.toml`.

---

## Interface de terminal

### curses (stdlib) + windows-curses

`curses` é o módulo da biblioteca padrão para desenhar em terminais
(janelas, bordas, captura de tecla sem bloquear) — já vem pronto em
Linux/macOS. No Windows ele não existe na stdlib; `windows-curses` (um
pacote de terceiros que empacota o PDCurses) supre exatamente a mesma API,
por isso o `pyproject.toml` marca a dependência com `; sys_platform ==
'win32'` — em Linux/macOS ela nem é instalada.

**Por que esta:** é a forma clássica de fazer um jogo de terminal em tempo
real em Python sem framework de jogo — desenha caracteres em coordenadas
`(y, x)`, lê teclas com timeout (o "relógio" do jogo) e cobre os três
sistemas operacionais com o mesmo código.

**Estudar:** `curses.wrapper` (restaura o terminal mesmo se o código
quebrar), `janela.getmaxyx()`, `janela.addch(y, x, char)`,
`janela.timeout(ms)` + `janela.getch()` (captura de tecla não bloqueante),
as constantes `curses.KEY_*`.

---

## Ferramentas de qualidade

### Ruff

O linter — substitui Flake8 + isort + pyupgrade num binário só, quase
instantâneo. Aqui verifica erros óbvios (`F`), estilo `pycodestyle`
(`E`/`W`), ordena imports (`I`) e sugere sintaxe moderna (`UP`).

**Por que esta:** é o linter padrão em todos os projetos Python do Ryan; um
só comando (`ruff check .`) substitui o que antes precisava de 3-4
ferramentas separadas.

**Estudar:** `uv run ruff check .`, `uv run ruff check --fix .` (corrige o
que for seguro), a tabela `select` no `pyproject.toml` (cada letra é uma
família de regra).

### Black

O formatador — sem configuração para discutir (mesma filosofia do
`gofmt`). Reescreve o arquivo no estilo canônico do Black; ninguém revisa
espaçamento em code review.

**Por que esta:** padrão de-facto do ecossistema Python; usado sem exceção
nos outros projetos do Ryan.

**Estudar:** `uv run black .` (reformata), `uv run black --check .` (só
verifica, usado no CI).

### Mypy

O verificador de tipos estáticos, em modo `strict`. Lê as anotações de
tipo (`-> None`, `list[list[int]]`, `int | None`) e garante que elas sejam
consistentes antes mesmo de rodar o código.

**Por que esta:** o projeto é pequeno, mas tipar tudo desde o início é a
prática que os outros projetos do Ryan seguem — evita o hábito de "só ligo
o mypy quando o projeto crescer" (nunca liga). `curses.window`, o tipo da
janela, existe na stdlib e é anotável normalmente.

**Estudar:** sintaxe `X | None` / `list[X]` (não `Optional`/`List`),
`-> None` explícito em função que não retorna nada, `uv run mypy`.

### pytest

O executor de testes. `tests/test_main.py` cobre a lógica do jogo (regras
de movimento, colisão, direção oposta, sorteio de fruta) sem depender de
um terminal real, através de uma `curses.window` falsa
(`_FakeJanela`) que só registra chamadas.

**Por que esta:** padrão de-facto de testes em Python; a fixture
`monkeypatch` (nativa do pytest) permite simular `input()`, `random.randint`
e `time.sleep` sem I/O real — essencial para testar um jogo de terminal em
tempo real sem esperar segundos de verdade nem abrir uma janela.

**Estudar:** `@pytest.fixture`, `@pytest.mark.parametrize` (testar as
quatro direções e os quatro lados da borda sem repetir código),
`monkeypatch.setattr` (substituir `input`/`random.randint`/`time.sleep`
durante o teste), `capsys` (capturar o que foi impresso no terminal antes
do curses assumir a tela).

---

## Peças menores

| Peça | Papel |
|---|---|
| `random.randint` (stdlib) | sorteia a posição da fruta a cada rodada |
| `time.sleep` (stdlib) | pausa de 3s na tela de "Fim de Jogo" antes de fechar |
| `sys.stdout.reconfigure` (stdlib) | força UTF-8 na saída da seleção de dificuldade, evitando `UnicodeEncodeError` com stdout redirecionado no Windows |

---

## O que deliberadamente não está na stack

- **Um framework de jogo (Pygame, Arcade)** — o objetivo pedagógico é
  entender o game loop e a manipulação de coordenadas "na mão"; um
  framework esconderia exatamente o que o projeto ensina.
- **`colorama`/`rich`** — o jogo usa só os caracteres ASCII (`@`, `#`,
  `*`) e o `curses.A_REVERSE` nativo para o destaque final; cor colorida
  não agrega ao objetivo didático e adicionaria uma dependência de
  runtime extra além do `windows-curses` já necessário.
- **Persistência de recorde (arquivo/banco)** — fica como atividade
  proposta no README para quem quiser praticar, não como parte do jogo
  base.

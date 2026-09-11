# CLAUDE.md

Este arquivo orienta o Claude Code (claude.ai/code) ao trabalhar neste
repositório.

## Visão geral do projeto

Jogo da Cobrinha (Snake) em Python, via terminal com `curses` — material
de estudo para prática de lógica de movimento, manipulação de listas
dinâmicas e coordenadas. Um único arquivo (`main.py`), com uma dependência
de runtime condicional (`windows-curses`, só no Windows). Repositório
pessoal/educacional, público no GitHub.

## Comandos comuns

```bash
# Sincronizar o ambiente (.venv) a partir do uv.lock
uv sync

# Rodar o jogo
uv run main.py

# Rodar a suíte de testes
uv run pytest

# Rodar um teste específico
uv run pytest tests/test_main.py::test_verificar_colisoes_sem_colisao -v

# Lint, formatação e tipos (nesta ordem)
uv run ruff check .          # lint (substitui flake8 + isort)
uv run ruff check --fix .    # corrige automaticamente o que for seguro
uv run black .               # formatação
uv run mypy                  # tipos (arquivos em [tool.mypy] files)

# Gerenciar dependências
uv add <pacote>               # runtime
uv add --dev <pacote>         # ferramenta de desenvolvimento
uv remove <pacote>
uv lock --upgrade-package <pacote>
```

## Arquitetura

```
main.py              # todas as funções do jogo + ciclo_do_jogo (ponto de entrada)
tests/test_main.py   # suíte pytest (27 casos), com _FakeJanela (curses.window falsa)
docs/stack.md         # o que cada peça da stack faz e por quê
specs/                # spec-driven development (ver specs/README.md)
  001-jogo-da-cobrinha/
iniciar_jogo.bat      # atalho Windows: uv run main.py (fallback: python main.py)
iniciar_jogo.sh       # atalho Linux/macOS: uv run main.py (fallback: python3 main.py)
pyproject.toml        # gerenciado por uv — windows-curses (win32) + grupo dev
                       # com ruff/black/mypy/pytest
uv.lock               # lock do grafo de dependências — nunca editar à mão
.github/
  workflows/ci.yml    # ruff -> black --check -> mypy -> pytest, em push/PR
  dependabot.yml      # PRs semanais de atualização (uv + github-actions)
```

### `main.py`

Sem classe — o estado da partida (cobra, fruta, direção, pontuação) vive
em variáveis locais de `ciclo_do_jogo`, chamada por `curses.wrapper`
(restaura o terminal mesmo se o código quebrar). Cada responsabilidade é
uma função que recebe a `curses.window` como parâmetro: desenho
(`desenhar_tela`, `desenhar_ator`, `desenhar_cobra`), movimento
(`gerar_nova_fruta`, `obter_nova_direcao`, `direcao_e_oposta`,
`mover_cobra`) e fim de jogo (`verificar_colisoes`, `finalizar_jogo`).
Detalhamento completo (RF-NN, ADRs) em
[`specs/001-jogo-da-cobrinha/`](specs/001-jogo-da-cobrinha/requirements.md).

## Convenções

- **Idioma do código:** português — projeto pessoal/educacional (regra do
  `CLAUDE.md` global: "Pessoal solo → Português"). Exceções: keywords da
  linguagem, termos técnicos universais (`int`, `str`, `bool`).
- **Estilo de construção de arquivos** (docstrings, type hints,
  comentários, réguas de seção): ver a skill `/estilo-arquivos` — não
  repetido aqui.

## Qualidade e automação

Sequência do portão, sempre nesta ordem: `ruff check .` → `black --check
.` → `mypy` → `pytest`. O `.github/workflows/ci.yml` roda exatamente essa
sequência (Python 3.12 e 3.13, `ubuntu-latest`) em todo push na `main` e
em todo PR — um check verde no PR significa o mesmo que um clone limpo
passando.

Sem hooks de `.claude/` neste projeto (repositório pequeno demais para
justificar automação por evento); rode o portão manualmente antes de
commitar.

> **Cuidado:** o jogo abre uma janela `curses` de verdade — não tem como
> rodar `ciclo_do_jogo` de ponta a ponta num terminal não interativo (CI,
> pipe, este próprio agente). A suíte de testes cobre cada peça isolada
> via `_FakeJanela`; qualquer mudança de comportamento do loop principal
> merece um teste manual, rodando `uv run main.py` num terminal de
> verdade.

## Spec-driven development

Specs em `specs/NNN-nome/` (`requirements.md` → `design.md` → `tasks.md`),
conduzidas pela skill `/spec`. A spec `001-jogo-da-cobrinha` foi escrita
por **engenharia reversa** (o jogo já estava pronto) e é o padrão-ouro de
formato para specs futuras neste repositório — ver
[`specs/README.md`](specs/README.md).

Ao fim de cada sessão: `/atualizar-docs` e depois `/fechar-sessao` (agrupa
as mudanças, commita em Conventional Commits numa branch, dá push, abre/
atualiza o PR — para antes do merge).

## Gestão de dependências (uv)

O projeto tem uma dependência de runtime condicional:
`windows-curses; sys_platform == 'win32'` (supre o módulo `curses`, que
não existe na stdlib do Windows). O `uv` resolve o marcador de plataforma
sozinho — instala só onde faz sentido. O grupo `dev` (`ruff`, `black`,
`mypy`, `pytest`) é travado junto no `uv.lock`. Commite `pyproject.toml`
**e** `uv.lock` juntos; nunca edite o lock à mão.

> **Cuidado:** `iniciar_jogo.bat`/`.sh` preferem `uv run main.py`, mas
> caem para `python`/`python3 main.py` puro se o `uv` não estiver
> instalado. Nesse fallback, quem estiver no Windows sem `uv` precisa
> instalar o `windows-curses` manualmente (`pip install windows-curses`)
> — é assim que alguém sem `uv` (o público educacional do README) ainda
> consegue rodar o jogo.

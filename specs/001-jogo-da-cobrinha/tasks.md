---
feature: Jogo da Cobrinha (Snake) via terminal com curses
status: concluído
data: 2026-09-11
relacionado:
  - 001-jogo-da-cobrinha/requirements.md
  - 001-jogo-da-cobrinha/design.md
origem: engenharia reversa
---

# 001 — Jogo da Cobrinha — Tasks

## Etapa 0 — Jogo original (histórico, pré-modernização)

- [x] `main.py`: seleção de dificuldade, desenho do campo/cobra/fruta,
      movimento, direção oposta bloqueada, colisão e tela final. — RF-01
      a RF-06
- [x] `iniciar_jogo.bat` / `iniciar_jogo.sh`: scripts de atalho por SO.
- [x] `requirements.txt`: dependência `windows-curses` condicional a
      `sys_platform == 'win32'`.
- [x] Portão de qualidade. — verificação manual (sem suíte automatizada
      nesta etapa).

## Etapa 1 — Modernização (uv, tipos, testes, correção de bug)

- [x] `main.py`: adiciona type hints em toda assinatura (`-> None`
      explícito, `curses.window`, `list[list[int]]`, `int | None`) e
      `from __future__ import annotations`.
- [x] `main.py`: promove `NIVEIS_DIFICULDADE`, `DIRECOES_VALIDAS` e
      `DIRECOES_OPOSTAS` a constantes de módulo. — ADR-1
- [x] `main.py`: reconfigura `sys.stdout` para UTF-8 no import, corrigindo
      um `UnicodeEncodeError` real na mensagem de aviso da dificuldade
      (achado ao testar `selecionar_nivel_dificuldade` com stdout
      redirecionado durante esta modernização). — ADR-2, RNF-03
- [x] `pyproject.toml`: cria manifesto gerenciado por `uv` — dependência
      de runtime `windows-curses` condicional por `sys_platform`, grupo
      `dev` com `ruff`, `black`, `mypy`, `pytest`. — ADR-3
- [x] Remove `requirements.txt` (substituído pelo `pyproject.toml` +
      `uv.lock`).
- [x] `tests/test_main.py`: cria `_FakeJanela` (fake de `curses.window`) e
      suíte pytest cobrindo RF-01 a RF-06 (27 casos, parametrizados onde
      fazia sentido). — ADR-4
- [x] `iniciar_jogo.bat` / `iniciar_jogo.sh`: passam a preferir `uv run
      main.py`, com fallback para `python`/`python3` puro (o nome do
      arquivo já batia com `main.py` antes da modernização — nada a
      corrigir nesse ponto).
- [x] `.gitignore`: adiciona o bloco de caches de ferramentas
      (`.ruff_cache/`, `.mypy_cache/`, `.pytest_cache/`).
- [x] Portão de qualidade. — `ruff check .`, `black --check .`, `mypy` e
      `pytest` (27 passed) verdes.

## Etapa 2 — Documentação e CI

- [x] `docs/stack.md`: mapa da stack (Python, uv, curses/windows-curses,
      ruff, black, mypy, pytest).
- [x] `specs/001-jogo-da-cobrinha/`: esta spec, por engenharia reversa.
- [x] `.github/dependabot.yml`: atualização semanal de `uv` +
      `github-actions`.
- [x] `.github/workflows/ci.yml`: job `qualidade` (`ruff` → `black
      --check` → `mypy` → `pytest`) em Python 3.12 e 3.13, `ubuntu-latest`
      (o `curses` da stdlib do Linux cobre a dependência sem precisar do
      `windows-curses`).
- [x] `CLAUDE.md`: orientação de projeto para sessões futuras.
- [x] `README.md` / `CONTRIBUTING.md`: atualizados para `uv` (em vez de
      `pip`) e para a suíte de testes.
- [x] Portão de qualidade. — `ruff check .`, `black --check .`, `mypy` e
      `pytest` (27 passed) verdes.

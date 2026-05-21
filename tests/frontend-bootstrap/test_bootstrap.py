"""Testes RED para 003-react-bootstrap-home (frontend-bootstrap).

Stack: Python 3.12 + pytest (testes estruturais/processuais sobre projeto Next.js 15).
Todos os testes devem falhar (RED) até que o código de produção seja implementado.
"""

import os
import subprocess
import shutil
import time
import re
from pathlib import Path

import pytest

# Diretório raiz do projeto (dois níveis acima de tests/frontend-bootstrap/)
PROJECT_ROOT = Path(__file__).parent.parent.parent


# ---------------------------------------------------------------------------
# CA-001 — Servidor de desenvolvimento inicia sem erros
# ---------------------------------------------------------------------------

def test_dev_server_starts_without_errors():
    """CA-001: servidor de desenvolvimento inicia sem erros e exibe URL local.

    Dado que as dependências estão instaladas,
    Quando `pnpm run dev` é executado,
    Então o processo sobe sem erros e exibe uma URL local no stdout/stderr.
    """
    # Arrange
    node_modules = PROJECT_ROOT / "node_modules"
    assert node_modules.exists(), (
        "node_modules/ não encontrado — execute `pnpm install` antes de rodar CA-001"
    )

    # Act — inicia o servidor de dev e aguarda saída indicando disponibilidade
    proc = subprocess.Popen(
        ["pnpm", "run", "dev"],
        cwd=str(PROJECT_ROOT),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )

    url_pattern = re.compile(r"http://localhost:\d+")
    found_url = False
    deadline = time.time() + 30  # RNF-001: < 30 segundos

    try:
        while time.time() < deadline:
            line = proc.stdout.readline()
            if not line:
                break
            if url_pattern.search(line):
                found_url = True
                break
    finally:
        proc.terminate()
        proc.wait(timeout=10)

    # Assert
    assert found_url, (
        "CA-001 FALHOU: nenhuma URL local (ex: http://localhost:3000) foi exibida "
        "pelo servidor de desenvolvimento dentro de 30 segundos."
    )


# ---------------------------------------------------------------------------
# CA-002 — Página inicial exibe apenas o texto "funcionou"
# ---------------------------------------------------------------------------

def test_home_displays_only_funcionou_text():
    """CA-002: a página inicial exibe única e exclusivamente o texto 'funcionou'.

    Dado que o servidor de desenvolvimento está rodando,
    Quando o usuário acessa a URL local,
    Então o conteúdo textual visível é apenas 'funcionou'.
    """
    # Arrange — verificar que page.tsx existe e contém 'funcionou'
    page_tsx = PROJECT_ROOT / "src" / "app" / "page.tsx"
    assert page_tsx.exists(), (
        "CA-002 FALHOU: src/app/page.tsx não encontrado — o projeto não foi inicializado."
    )

    content = page_tsx.read_text(encoding="utf-8")

    # Assert — o arquivo deve conter o texto 'funcionou'
    assert "funcionou" in content, (
        "CA-002 FALHOU: o texto 'funcionou' não foi encontrado em src/app/page.tsx."
    )

    # Assert — NÃO deve conter strings de boilerplate do create-next-app
    boilerplate_strings = [
        "Get started by editing",
        "Edit src/app/page.tsx",
        "Deploy now",
        "Vercel",
        "Next.js",
        "<Image",
    ]
    for boilerplate in boilerplate_strings:
        assert boilerplate not in content, (
            f"CA-002 FALHOU: conteúdo de boilerplate '{boilerplate}' encontrado em "
            f"src/app/page.tsx — a página deve exibir SOMENTE 'funcionou'."
        )


# ---------------------------------------------------------------------------
# CA-003 — Texto "funcionou" está centralizado na viewport
# ---------------------------------------------------------------------------

def test_funcionou_text_is_centered():
    """CA-003: o texto 'funcionou' está centralizado vertical e horizontalmente.

    Dado que o servidor de desenvolvimento está rodando,
    Quando o usuário acessa a URL local com viewport padrão desktop,
    Então o texto está no centro horizontal e vertical da viewport.

    Estratégia: inspecionar globals.css buscando regras flexbox de centralização
    aplicadas ao body ou ao container principal (100vh + flex + center).
    """
    # Arrange
    globals_css = PROJECT_ROOT / "src" / "app" / "globals.css"
    assert globals_css.exists(), (
        "CA-003 FALHOU: src/app/globals.css não encontrado."
    )

    css_content = globals_css.read_text(encoding="utf-8")

    # Assert — deve conter propriedades de centralização flexbox
    assert "display" in css_content and "flex" in css_content, (
        "CA-003 FALHOU: globals.css não contém 'display: flex' necessário para centralização."
    )
    assert "align-items" in css_content and "center" in css_content, (
        "CA-003 FALHOU: globals.css não contém 'align-items: center' para centralização vertical."
    )
    assert "justify-content" in css_content, (
        "CA-003 FALHOU: globals.css não contém 'justify-content' para centralização horizontal."
    )

    # Assert — deve conter altura mínima de 100vh para ocupar a viewport inteira
    assert "100vh" in css_content or "100dvh" in css_content, (
        "CA-003 FALHOU: globals.css não define min-height de 100vh/100dvh — "
        "centralização vertical não pode funcionar sem altura definida na viewport."
    )


# ---------------------------------------------------------------------------
# CA-004 — Build de produção executa sem erros
# ---------------------------------------------------------------------------

def test_production_build_succeeds():
    """CA-004: o comando de build de produção finaliza com exit code 0 e gera artefatos.

    Dado que as dependências estão instaladas,
    Quando `pnpm run build` é executado,
    Então o processo finaliza com código de saída 0
    E os arquivos de bundle são gerados em .next/.
    """
    # Arrange
    node_modules = PROJECT_ROOT / "node_modules"
    assert node_modules.exists(), (
        "node_modules/ não encontrado — execute `pnpm install` antes de rodar CA-004."
    )

    # Act
    result = subprocess.run(
        ["pnpm", "run", "build"],
        cwd=str(PROJECT_ROOT),
        capture_output=True,
        text=True,
        timeout=120,  # build pode demorar mais que dev
    )

    # Assert — exit code 0
    assert result.returncode == 0, (
        f"CA-004 FALHOU: `pnpm run build` finalizou com exit code {result.returncode}.\n"
        f"STDOUT: {result.stdout[-2000:]}\nSTDERR: {result.stderr[-2000:]}"
    )

    # Assert — diretório .next/ foi gerado
    next_dir = PROJECT_ROOT / ".next"
    assert next_dir.exists() and next_dir.is_dir(), (
        "CA-004 FALHOU: diretório .next/ não foi gerado após `pnpm run build`."
    )

    # Assert — diretório .next/ não está vazio
    next_contents = list(next_dir.iterdir())
    assert len(next_contents) > 0, (
        "CA-004 FALHOU: diretório .next/ existe mas está vazio — build pode ter falhado silenciosamente."
    )


# ---------------------------------------------------------------------------
# CA-005 — Repositório contém estrutura mínima organizada
# ---------------------------------------------------------------------------

def test_repository_has_minimum_structure():
    """CA-005: o repositório contém todos os arquivos e diretórios mínimos esperados.

    Dado que o repositório foi clonado,
    Quando o conteúdo é inspecionado,
    Então existem: package.json, src/, README.md e .gitignore com node_modules/ excluído.
    """
    # Arrange + Act + Assert — package.json na raiz
    package_json = PROJECT_ROOT / "package.json"
    assert package_json.exists(), (
        "CA-005 FALHOU: package.json não encontrado na raiz do repositório."
    )

    # Assert — package.json é JSON válido com campos essenciais
    import json
    pkg = json.loads(package_json.read_text(encoding="utf-8"))
    assert "scripts" in pkg, (
        "CA-005 FALHOU: package.json não contém a chave 'scripts'."
    )
    assert "dev" in pkg["scripts"], (
        "CA-005 FALHOU: package.json não contém script 'dev'."
    )
    assert "build" in pkg["scripts"], (
        "CA-005 FALHOU: package.json não contém script 'build'."
    )

    # Assert — diretório src/ existe com código-fonte React
    src_dir = PROJECT_ROOT / "src"
    assert src_dir.exists() and src_dir.is_dir(), (
        "CA-005 FALHOU: diretório src/ não encontrado na raiz do repositório."
    )

    src_files = list(src_dir.rglob("*.tsx")) + list(src_dir.rglob("*.ts"))
    assert len(src_files) > 0, (
        "CA-005 FALHOU: diretório src/ existe mas não contém arquivos .tsx/.ts — "
        "o projeto React não foi inicializado."
    )

    # Assert — README.md na raiz
    readme = PROJECT_ROOT / "README.md"
    assert readme.exists(), (
        "CA-005 FALHOU: README.md não encontrado na raiz do repositório."
    )

    # Assert — .gitignore existe e exclui node_modules/
    gitignore = PROJECT_ROOT / ".gitignore"
    assert gitignore.exists(), (
        "CA-005 FALHOU: .gitignore não encontrado na raiz do repositório."
    )

    gitignore_content = gitignore.read_text(encoding="utf-8")
    assert "node_modules" in gitignore_content, (
        "CA-005 FALHOU: .gitignore não exclui node_modules/ — risco de commitar dependências."
    )


# ---------------------------------------------------------------------------
# CA-006 — README contém instruções de execução
# ---------------------------------------------------------------------------

def test_readme_contains_execution_instructions():
    """CA-006: o README.md contém instruções completas de instalação e execução.

    Dado que o repositório foi clonado,
    Quando o README.md é lido,
    Então contém: instrução de instalação de dependências,
                  comando para servidor de desenvolvimento,
                  comando para build de produção.
    """
    # Arrange
    readme = PROJECT_ROOT / "README.md"
    assert readme.exists(), (
        "CA-006 FALHOU: README.md não encontrado."
    )

    # Act
    content = readme.read_text(encoding="utf-8").lower()

    # Assert — instrução de instalação de dependências
    install_keywords = ["pnpm install", "npm install", "yarn install"]
    has_install = any(kw in content for kw in install_keywords)
    assert has_install, (
        "CA-006 FALHOU: README.md não contém instrução de instalação de dependências "
        f"(esperado um de: {install_keywords})."
    )

    # Assert — comando para servidor de desenvolvimento
    dev_keywords = ["pnpm dev", "npm run dev", "yarn dev", "pnpm run dev"]
    has_dev = any(kw in content for kw in dev_keywords)
    assert has_dev, (
        "CA-006 FALHOU: README.md não contém comando para iniciar o servidor de desenvolvimento "
        f"(esperado um de: {dev_keywords})."
    )

    # Assert — comando para build de produção
    build_keywords = ["pnpm build", "npm run build", "yarn build", "pnpm run build"]
    has_build = any(kw in content for kw in build_keywords)
    assert has_build, (
        "CA-006 FALHOU: README.md não contém comando de build de produção "
        f"(esperado um de: {build_keywords})."
    )


# ---------------------------------------------------------------------------
# CA-007 — Caso de erro: dependências não instaladas
# ---------------------------------------------------------------------------

def test_dev_command_fails_without_node_modules():
    """CA-007: executar `pnpm dev` sem node_modules/ resulta em erro com exit code != 0.

    Dado que o diretório node_modules/ não existe,
    Quando o comando de desenvolvimento é executado,
    Então o processo falha com exit code != 0
    E uma mensagem de erro é exibida no terminal.
    """
    import tempfile
    import shutil

    # Arrange — criar diretório temporário simulando repositório sem node_modules
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)

        # Copiar apenas package.json (sem node_modules) para simular repo recém-clonado
        package_json_src = PROJECT_ROOT / "package.json"
        if not package_json_src.exists():
            pytest.fail(
                "CA-007 FALHOU (pré-condição): package.json não encontrado — "
                "o projeto precisa existir para testar o cenário de erro."
            )

        shutil.copy(str(package_json_src), str(tmp_path / "package.json"))

        # Copiar next.config.ts se existir (necessário para o comando next dev ser reconhecido)
        next_config = PROJECT_ROOT / "next.config.ts"
        if next_config.exists():
            shutil.copy(str(next_config), str(tmp_path / "next.config.ts"))

        # Act — rodar pnpm dev sem node_modules presente
        # Usamos timeout curto: esperamos falha rápida
        result = subprocess.run(
            ["pnpm", "run", "dev"],
            cwd=str(tmp_path),
            capture_output=True,
            text=True,
            timeout=30,
        )

        # Assert — exit code deve ser diferente de 0
        assert result.returncode != 0, (
            "CA-007 FALHOU: `pnpm run dev` sem node_modules/ finalizou com exit code 0 "
            "(sucesso), mas deveria falhar."
        )

        # Assert — alguma mensagem de erro deve estar presente no output
        combined_output = (result.stdout + result.stderr).lower()
        error_indicators = [
            "error",
            "not found",
            "cannot find",
            "enoent",
            "missing",
            "no such file",
            "module not found",
            "command not found",
        ]
        has_error_message = any(indicator in combined_output for indicator in error_indicators)
        assert has_error_message, (
            "CA-007 FALHOU: o processo falhou mas não exibiu mensagem de erro reconhecível.\n"
            f"STDOUT: {result.stdout[:1000]}\nSTDERR: {result.stderr[:1000]}"
        )

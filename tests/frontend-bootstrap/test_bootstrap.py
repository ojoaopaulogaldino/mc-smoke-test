import os
import subprocess
import time
import shutil
import threading
import re

import pytest

# Root directory of the repository (two levels up from this test file)
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


def _find_package_manager():
    """Detect pnpm or npm in PATH."""
    if shutil.which("pnpm"):
        return "pnpm"
    if shutil.which("npm"):
        return "npm"
    return None


PKG_MGR = _find_package_manager()


# ---------------------------------------------------------------------------
# CA-001 — Servidor de desenvolvimento inicia sem erros
# ---------------------------------------------------------------------------

def test_dev_server_starts_without_errors():
    """
    CA-001: O servidor de desenvolvimento deve iniciar sem erros e expor uma
    URL local acessivel (ex: http://localhost:3000).
    """
    # Arrange
    assert PKG_MGR is not None, "pnpm ou npm nao encontrado no PATH"
    node_modules = os.path.join(REPO_ROOT, "node_modules")
    assert os.path.isdir(node_modules), (
        "node_modules nao encontrado — execute pnpm install antes dos testes"
    )

    url_pattern = re.compile(r"http://localhost:\d+")
    detected_url = []
    process = None

    def stream_output(proc):
        for line in proc.stdout:
            decoded = line.decode("utf-8", errors="replace")
            if url_pattern.search(decoded):
                detected_url.append(decoded.strip())

    # Act
    process = subprocess.Popen(
        [PKG_MGR, "run", "dev"],
        cwd=REPO_ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )

    reader = threading.Thread(target=stream_output, args=(process,), daemon=True)
    reader.start()

    deadline = time.time() + 30
    while time.time() < deadline:
        if detected_url:
            break
        if process.poll() is not None:
            break
        time.sleep(0.5)

    process.terminate()
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()

    # Assert
    assert detected_url, (
        "CA-001 FALHOU: nenhuma URL local foi detectada na saida do servidor "
        "de desenvolvimento dentro de 30 segundos"
    )


# ---------------------------------------------------------------------------
# CA-002 — Pagina inicial exibe apenas o texto funcionou
# ---------------------------------------------------------------------------

def test_home_displays_only_funcionou_text():
    """
    CA-002: A pagina inicial deve exibir unica e exclusivamente o texto
    exato 'funcionou', sem outros conteudos proeminentes.
    """
    # Arrange
    page_tsx_candidates = [
        os.path.join(REPO_ROOT, "src", "app", "page.tsx"),
        os.path.join(REPO_ROOT, "app", "page.tsx"),
        os.path.join(REPO_ROOT, "src", "pages", "index.tsx"),
        os.path.join(REPO_ROOT, "pages", "index.tsx"),
    ]
    found_page = None
    for candidate in page_tsx_candidates:
        if os.path.isfile(candidate):
            found_page = candidate
            break

    assert found_page is not None, (
        "CA-002 FALHOU: nenhum arquivo de pagina inicial encontrado "
        "(src/app/page.tsx, app/page.tsx, etc.)"
    )

    # Act
    with open(found_page, "r", encoding="utf-8") as fh:
        content = fh.read()

    # Assert — o arquivo deve conter 'funcionou' e NAO deve conter strings de boilerplate
    assert "funcionou" in content, (
        "CA-002 FALHOU: texto 'funcionou' nao encontrado em " + found_page
    )

    boilerplate_strings = [
        "Get started",
        "Edit src",
        "Vercel",
        "Next.js",
        "Deploy now",
        "Read our docs",
    ]
    for boilerplate in boilerplate_strings:
        assert boilerplate not in content, (
            f"CA-002 FALHOU: texto de boilerplate '{boilerplate}' encontrado em {found_page}. "
            "A pagina deve exibir APENAS 'funcionou'."
        )


# ---------------------------------------------------------------------------
# CA-003 — Texto funcionou esta centralizado na viewport
# ---------------------------------------------------------------------------

def test_funcionou_text_is_centered():
    """
    CA-003: O texto 'funcionou' deve estar centralizado vertical e
    horizontalmente na viewport usando flexbox nativo sem libs externas.
    """
    # Arrange
    css_candidates = [
        os.path.join(REPO_ROOT, "src", "app", "globals.css"),
        os.path.join(REPO_ROOT, "app", "globals.css"),
        os.path.join(REPO_ROOT, "src", "styles", "globals.css"),
        os.path.join(REPO_ROOT, "styles", "globals.css"),
    ]
    found_css = None
    for candidate in css_candidates:
        if os.path.isfile(candidate):
            found_css = candidate
            break

    assert found_css is not None, (
        "CA-003 FALHOU: arquivo globals.css nao encontrado"
    )

    # Act
    with open(found_css, "r", encoding="utf-8") as fh:
        css_content = fh.read()

    # Assert — deve conter propriedades de centralizacao via flexbox
    assert "display" in css_content and "flex" in css_content, (
        "CA-003 FALHOU: globals.css nao contém 'display: flex' "
        "necessario para centralizacao"
    )
    assert "align-items" in css_content and "center" in css_content, (
        "CA-003 FALHOU: globals.css nao contém 'align-items: center' "
        "para centralizacao vertical"
    )
    assert "justify-content" in css_content, (
        "CA-003 FALHOU: globals.css nao contém 'justify-content' "
        "para centralizacao horizontal"
    )
    # Deve haver min-height ou height referenciando 100vh para ocupar a viewport
    assert "100vh" in css_content or "100%" in css_content, (
        "CA-003 FALHOU: globals.css nao contém referencia a 100vh ou 100% "
        "de altura para centralizacao vertical na viewport"
    )


# ---------------------------------------------------------------------------
# CA-004 — Build de producao executa sem erros
# ---------------------------------------------------------------------------

def test_production_build_succeeds():
    """
    CA-004: O comando de build de producao deve finalizar com exit code 0
    e gerar os arquivos de bundle no diretorio de saida (.next/ ou dist/).
    """
    # Arrange
    assert PKG_MGR is not None, "pnpm ou npm nao encontrado no PATH"
    node_modules = os.path.join(REPO_ROOT, "node_modules")
    assert os.path.isdir(node_modules), (
        "node_modules nao encontrado — execute pnpm install antes dos testes"
    )

    # Act
    result = subprocess.run(
        [PKG_MGR, "run", "build"],
        cwd=REPO_ROOT,
        capture_output=True,
        timeout=120,
    )

    # Assert — exit code 0
    assert result.returncode == 0, (
        "CA-004 FALHOU: build retornou exit code {}. STDOUT: {}. STDERR: {}".format(
            result.returncode,
            result.stdout.decode("utf-8", errors="replace")[:500],
            result.stderr.decode("utf-8", errors="replace")[:500],
        )
    )

    # Assert — diretorio de saida existe
    next_dir = os.path.join(REPO_ROOT, ".next")
    dist_dir = os.path.join(REPO_ROOT, "dist")
    build_dir = os.path.join(REPO_ROOT, "build")
    output_exists = (
        os.path.isdir(next_dir)
        or os.path.isdir(dist_dir)
        or os.path.isdir(build_dir)
    )
    assert output_exists, (
        "CA-004 FALHOU: nenhum diretorio de saida (.next/, dist/, build/) "
        "foi criado apos o build"
    )


# ---------------------------------------------------------------------------
# CA-005 — Repositorio contém estrutura minima organizada
# ---------------------------------------------------------------------------

def test_repository_has_minimum_structure():
    """
    CA-005: O repositorio deve conter package.json, diretorio src/ (ou app/)
    com codigo React, README.md e .gitignore excluindo node_modules/.
    """
    # Arrange + Act + Assert — verificacao de cada artefato obrigatorio

    # package.json na raiz
    package_json = os.path.join(REPO_ROOT, "package.json")
    assert os.path.isfile(package_json), (
        "CA-005 FALHOU: package.json nao encontrado na raiz do repositorio"
    )

    # src/ ou app/ com codigo-fonte React
    src_dir = os.path.join(REPO_ROOT, "src")
    app_dir = os.path.join(REPO_ROOT, "app")
    has_src = os.path.isdir(src_dir)
    has_app = os.path.isdir(app_dir)
    assert has_src or has_app, (
        "CA-005 FALHOU: nenhum diretorio de codigo-fonte (src/ ou app/) "
        "encontrado na raiz do repositorio"
    )

    # README.md na raiz
    readme = os.path.join(REPO_ROOT, "README.md")
    assert os.path.isfile(readme), (
        "CA-005 FALHOU: README.md nao encontrado na raiz do repositorio"
    )

    # .gitignore deve existir e incluir node_modules
    gitignore = os.path.join(REPO_ROOT, ".gitignore")
    assert os.path.isfile(gitignore), (
        "CA-005 FALHOU: .gitignore nao encontrado na raiz do repositorio"
    )

    with open(gitignore, "r", encoding="utf-8") as fh:
        gitignore_content = fh.read()

    assert "node_modules" in gitignore_content, (
        "CA-005 FALHOU: .gitignore nao inclui 'node_modules/' "
        "expondo dependencias ao controle de versao"
    )


# ---------------------------------------------------------------------------
# CA-006 — README contém instrucoes de execucao
# ---------------------------------------------------------------------------

def test_readme_contains_execution_instructions():
    """
    CA-006: O README.md deve conter instrucoes para instalar dependencias,
    iniciar o servidor de desenvolvimento e executar o build de producao.
    """
    # Arrange
    readme = os.path.join(REPO_ROOT, "README.md")
    assert os.path.isfile(readme), (
        "CA-006 FALHOU: README.md nao encontrado na raiz do repositorio"
    )

    # Act
    with open(readme, "r", encoding="utf-8") as fh:
        readme_content = fh.read().lower()

    # Assert — instrucoes de instalacao
    install_keywords = ["install", "pnpm install", "npm install"]
    has_install = any(kw in readme_content for kw in install_keywords)
    assert has_install, (
        "CA-006 FALHOU: README.md nao contém instrucoes de instalacao de dependencias "
        "(ex: 'pnpm install' ou 'npm install')"
    )

    # Assert — instrucoes de servidor de desenvolvimento
    dev_keywords = ["pnpm dev", "npm run dev", "pnpm run dev", "yarn dev"]
    has_dev = any(kw in readme_content for kw in dev_keywords)
    assert has_dev, (
        "CA-006 FALHOU: README.md nao contém instrucoes para iniciar o servidor "
        "de desenvolvimento (ex: 'pnpm dev' ou 'npm run dev')"
    )

    # Assert — instrucoes de build de producao
    build_keywords = ["pnpm build", "npm run build", "pnpm run build", "yarn build"]
    has_build = any(kw in readme_content for kw in build_keywords)
    assert has_build, (
        "CA-006 FALHOU: README.md nao contém instrucoes para o build de producao "
        "(ex: 'pnpm build' ou 'npm run build')"
    )


# ---------------------------------------------------------------------------
# CA-007 — Caso de erro: dependencias nao instaladas
# ---------------------------------------------------------------------------

def test_dev_command_fails_without_node_modules():
    """
    CA-007: Ao executar o comando de desenvolvimento sem node_modules/
    instalado, o processo deve falhar com exit code diferente de 0
    e exibir mensagem de erro no terminal.
    """
    import tempfile
    import json

    # Arrange — criar diretorio temporario sem node_modules
    with tempfile.TemporaryDirectory() as tmp_dir:
        # Copiar apenas package.json (sem node_modules)
        src_package = os.path.join(REPO_ROOT, "package.json")
        dst_package = os.path.join(tmp_dir, "package.json")

        if os.path.isfile(src_package):
            with open(src_package, "r", encoding="utf-8") as fh:
                pkg_data = json.load(fh)
            with open(dst_package, "w", encoding="utf-8") as fh:
                json.dump(pkg_data, fh)
        else:
            # Criar package.json minimo se ainda nao existe (red test)
            minimal_pkg = {
                "name": "jsaai-frontend",
                "scripts": {"dev": "next dev"},
                "dependencies": {"next": "15.0.0"}
            }
            with open(dst_package, "w", encoding="utf-8") as fh:
                json.dump(minimal_pkg, fh)

        assert not os.path.isdir(os.path.join(tmp_dir, "node_modules")), (
            "Arrange: node_modules nao deve existir no diretorio temporario"
        )

        assert PKG_MGR is not None, "pnpm ou npm nao encontrado no PATH"

        # Act
        result = subprocess.run(
            [PKG_MGR, "run", "dev"],
            cwd=tmp_dir,
            capture_output=True,
            timeout=15,
        )

        # Assert — deve falhar (exit code != 0)
        assert result.returncode != 0, (
            "CA-007 FALHOU: o comando de desenvolvimento retornou exit code 0 "
            "mesmo sem node_modules/ instalado. Era esperada uma falha."
        )

        combined_output = (
            result.stdout.decode("utf-8", errors="replace")
            + result.stderr.decode("utf-8", errors="replace")
        ).lower()

        # Deve haver alguma mensagem de erro no output
        error_indicators = [
            "error",
            "not found",
            "cannot find",
            "missing",
            "module",
            "enoent",
        ]
        has_error_message = any(indicator in combined_output for indicator in error_indicators)
        assert has_error_message, (
            "CA-007 FALHOU: o processo falhou mas nao exibiu mensagem de erro "
            "clara no terminal. Output: " + combined_output[:300]
        )

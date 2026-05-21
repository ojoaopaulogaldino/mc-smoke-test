"""Testes RED para feature 003-react-bootstrap-home (frontend-bootstrap).

Todos os testes devem FALHAR enquanto o código de produção não existir.
Stack: Next.js 15 + React 19 + pnpm (frontend); pytest (test runner).

Pré-requisito do ambiente de CI: Node 20 LTS e pnpm devem estar instalados.
"""

import os
import subprocess
import time
import signal
import shutil
import tempfile
from pathlib import Path

import pytest
import requests

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

# Raiz do repositório: dois níveis acima de tests/frontend-bootstrap/
REPO_ROOT = Path(__file__).resolve().parents[2]

# Porta padrão do Next.js
DEV_SERVER_PORT = 3000
DEV_SERVER_URL = f"http://localhost:{DEV_SERVER_PORT}"

# Timeout máximo (segundos) para o servidor de desenvolvimento subir (RNF-001: <30s)
DEV_SERVER_STARTUP_TIMEOUT = 30


def _find_pnpm() -> str:
    """Retorna caminho do executável pnpm ou levanta FileNotFoundError."""
    pnpm = shutil.which("pnpm")
    if pnpm is None:
        raise FileNotFoundError(
            "pnpm não encontrado no PATH. Instale pnpm antes de rodar os testes."
        )
    return pnpm


def _dev_server_ready(timeout: int = DEV_SERVER_STARTUP_TIMEOUT) -> bool:
    """Tenta conectar ao servidor de desenvolvimento até o timeout."""
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        try:
            resp = requests.get(DEV_SERVER_URL, timeout=2)
            if resp.status_code == 200:
                return True
        except requests.exceptions.ConnectionError:
            pass
        time.sleep(1)
    return False


# ---------------------------------------------------------------------------
# CA-001 — Servidor de desenvolvimento inicia sem erros
# ---------------------------------------------------------------------------

def test_dev_server_starts_without_errors():
    """CA-001: servidor de desenvolvimento inicia sem erros e expõe URL local acessível."""
    # Arrange
    pnpm = _find_pnpm()
    package_json = REPO_ROOT / "package.json"
    assert package_json.exists(), (
        "package.json não encontrado na raiz do repositório — projeto ainda não inicializado."
    )
    node_modules = REPO_ROOT / "node_modules"
    assert node_modules.exists(), (
        "node_modules/ não encontrado — execute 'pnpm install' antes de rodar CA-001."
    )

    # Act: inicia o servidor de desenvolvimento em background
    process = subprocess.Popen(
        [pnpm, "run", "dev"],
        cwd=str(REPO_ROOT),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        preexec_fn=os.setsid,
    )

    try:
        # Assert: servidor deve subir dentro do timeout e responder HTTP 200
        server_ready = _dev_server_ready(timeout=DEV_SERVER_STARTUP_TIMEOUT)
        assert server_ready, (
            f"Servidor de desenvolvimento não ficou acessível em {DEV_SERVER_STARTUP_TIMEOUT}s "
            f"em {DEV_SERVER_URL}. CA-001 falhou."
        )

        # Verifica que o processo ainda está rodando (sem crash imediato)
        assert process.poll() is None, (
            "Processo 'pnpm run dev' terminou inesperadamente — exit code indica erro."
        )
    finally:
        # Cleanup: encerra o grupo de processos do servidor
        try:
            os.killpg(os.getpgid(process.pid), signal.SIGTERM)
            process.wait(timeout=10)
        except Exception:
            process.kill()


# ---------------------------------------------------------------------------
# CA-002 — Página inicial exibe apenas o texto "funcionou"
# ---------------------------------------------------------------------------

def test_home_displays_only_funcionou_text():
    """CA-002: a única mensagem visível na página inicial é o texto exato 'funcionou'."""
    # Arrange
    pnpm = _find_pnpm()
    package_json = REPO_ROOT / "package.json"
    assert package_json.exists(), "package.json não encontrado."
    node_modules = REPO_ROOT / "node_modules"
    assert node_modules.exists(), "node_modules/ não encontrado."

    process = subprocess.Popen(
        [pnpm, "run", "dev"],
        cwd=str(REPO_ROOT),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        preexec_fn=os.setsid,
    )

    try:
        server_ready = _dev_server_ready(timeout=DEV_SERVER_STARTUP_TIMEOUT)
        assert server_ready, f"Servidor não ficou disponível em {DEV_SERVER_URL}."

        # Act: busca o HTML da página inicial
        response = requests.get(DEV_SERVER_URL, timeout=10)
        html_content = response.text

        # Assert: o texto "funcionou" deve aparecer no HTML
        assert "funcionou" in html_content, (
            "O texto 'funcionou' não foi encontrado no HTML da página inicial. "
            "CA-002 falhou."
        )

        # Assert: textos típicos de boilerplate do Next.js NÃO devem estar presentes
        boilerplate_markers = [
            "Get started by editing",
            "Edit <code>",
            "Deploy now",
            "Learn",
            "Examples",
            "Go to nextjs.org",
        ]
        for marker in boilerplate_markers:
            assert marker not in html_content, (
                f"Texto de boilerplate '{marker}' encontrado na página — "
                "a página não foi limpa corretamente. CA-002 falhou."
            )
    finally:
        try:
            os.killpg(os.getpgid(process.pid), signal.SIGTERM)
            process.wait(timeout=10)
        except Exception:
            process.kill()


# ---------------------------------------------------------------------------
# CA-003 — Texto "funcionou" está centralizado na viewport
# ---------------------------------------------------------------------------

def test_funcionou_text_is_centered():
    """CA-003: o texto 'funcionou' está centralizado vertical e horizontalmente via CSS flexbox."""
    # Arrange: verifica globals.css que deve conter as regras de centralização
    # Estratégia: inspeciona o arquivo CSS fonte (sem dependência de browser headless)
    # e o HTML servido, validando presença de regras flexbox obrigatórias.
    globals_css_candidates = [
        REPO_ROOT / "src" / "app" / "globals.css",
        REPO_ROOT / "app" / "globals.css",
    ]

    css_file = None
    for candidate in globals_css_candidates:
        if candidate.exists():
            css_file = candidate
            break

    assert css_file is not None, (
        "Arquivo globals.css não encontrado em src/app/ ou app/. "
        "CA-003 falhou — sem regras CSS de centralização."
    )

    # Act
    css_content = css_file.read_text(encoding="utf-8")

    # Assert: propriedades flexbox obrigatórias para centralização devem existir
    required_flex_properties = ["display: flex", "align-items: center", "justify-content: center"]
    missing = [prop for prop in required_flex_properties if prop not in css_content]
    assert not missing, (
        f"Propriedades CSS de centralização ausentes em {css_file}: {missing}. "
        "CA-003 falhou — texto 'funcionou' não está centralizado."
    )

    # Assert: deve haver height/min-height que garanta centralização vertical
    has_full_height = any(
        keyword in css_content
        for keyword in ["min-height: 100vh", "height: 100vh", "min-height:100vh", "height:100vh"]
    )
    assert has_full_height, (
        "Nenhuma regra de altura total (100vh) encontrada em globals.css. "
        "Sem isso, a centralização vertical não funcionará. CA-003 falhou."
    )


# ---------------------------------------------------------------------------
# CA-004 — Build de produção executa sem erros
# ---------------------------------------------------------------------------

def test_production_build_succeeds():
    """CA-004: 'pnpm run build' finaliza com exit code 0 e gera arquivos de bundle."""
    # Arrange
    pnpm = _find_pnpm()
    package_json = REPO_ROOT / "package.json"
    assert package_json.exists(), "package.json não encontrado."
    node_modules = REPO_ROOT / "node_modules"
    assert node_modules.exists(), "node_modules/ não encontrado."

    # Act: executa o build de produção
    result = subprocess.run(
        [pnpm, "run", "build"],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        timeout=300,  # build pode demorar mais em CI
    )

    # Assert: exit code deve ser 0
    assert result.returncode == 0, (
        f"'pnpm run build' falhou com exit code {result.returncode}.\n"
        f"STDOUT:\n{result.stdout}\n"
        f"STDERR:\n{result.stderr}\n"
        "CA-004 falhou."
    )

    # Assert: diretório de saída do Next.js deve existir
    next_build_dir = REPO_ROOT / ".next"
    assert next_build_dir.exists() and next_build_dir.is_dir(), (
        "Diretório .next/ não foi criado após o build. "
        "CA-004 falhou — bundle de produção não gerado."
    )

    # Assert: deve haver arquivos dentro de .next/static/ (chunks JS/CSS)
    static_dir = next_build_dir / "static"
    assert static_dir.exists(), (
        ".next/static/ não encontrado — build incompleto. CA-004 falhou."
    )
    static_files = list(static_dir.rglob("*"))
    assert len(static_files) > 0, (
        ".next/static/ existe mas está vazio — bundle não gerado corretamente. CA-004 falhou."
    )


# ---------------------------------------------------------------------------
# CA-005 — Repositório contém estrutura mínima organizada
# ---------------------------------------------------------------------------

def test_repository_has_minimum_structure():
    """CA-005: repositório clonado contém package.json, src/ (ou app/), README.md e .gitignore adequado."""
    # Arrange / Act / Assert — verificações de sistema de arquivos

    # Assert: package.json na raiz
    package_json = REPO_ROOT / "package.json"
    assert package_json.exists(), (
        "package.json não encontrado na raiz do repositório. CA-005 falhou."
    )

    # Assert: diretório de código-fonte React (src/app/ ou app/)
    src_app_dir = REPO_ROOT / "src" / "app"
    app_dir = REPO_ROOT / "app"
    assert src_app_dir.exists() or app_dir.exists(), (
        "Nenhum diretório src/app/ ou app/ encontrado. "
        "Estrutura de código-fonte React ausente. CA-005 falhou."
    )

    # Assert: README.md na raiz
    readme = REPO_ROOT / "README.md"
    assert readme.exists(), (
        "README.md não encontrado na raiz do repositório. CA-005 falhou."
    )

    # Assert: .gitignore existe e contém node_modules/
    gitignore = REPO_ROOT / ".gitignore"
    assert gitignore.exists(), (
        ".gitignore não encontrado na raiz do repositório. CA-005 falhou."
    )
    gitignore_content = gitignore.read_text(encoding="utf-8")
    assert "node_modules" in gitignore_content, (
        ".gitignore não exclui node_modules/. "
        "Risco de commitar dependências. CA-005 falhou."
    )

    # Assert (edge case): .gitignore também deve excluir .next/ (gerado pelo build)
    assert ".next" in gitignore_content, (
        ".gitignore não exclui .next/ (diretório de build do Next.js). "
        "CA-005 falhou — artefatos de build podem ser commitados."
    )


# ---------------------------------------------------------------------------
# CA-006 — README contém instruções de execução
# ---------------------------------------------------------------------------

def test_readme_contains_execution_instructions():
    """CA-006: README.md contém instruções de instalação, desenvolvimento e build."""
    # Arrange
    readme = REPO_ROOT / "README.md"
    assert readme.exists(), "README.md não encontrado. CA-006 falhou."

    # Act
    readme_content = readme.read_text(encoding="utf-8")

    # Assert: instruções de instalação de dependências
    install_keywords = ["pnpm install", "npm install", "yarn install"]
    has_install = any(kw in readme_content for kw in install_keywords)
    assert has_install, (
        f"README.md não contém instrução de instalação de dependências "
        f"(esperado um de: {install_keywords}). CA-006 falhou."
    )

    # Assert: comando para iniciar servidor de desenvolvimento
    dev_keywords = ["pnpm dev", "npm run dev", "pnpm run dev", "yarn dev"]
    has_dev = any(kw in readme_content for kw in dev_keywords)
    assert has_dev, (
        f"README.md não contém comando de servidor de desenvolvimento "
        f"(esperado um de: {dev_keywords}). CA-006 falhou."
    )

    # Assert: comando de build de produção
    build_keywords = ["pnpm build", "npm run build", "pnpm run build", "yarn build"]
    has_build = any(kw in readme_content for kw in build_keywords)
    assert has_build, (
        f"README.md não contém comando de build de produção "
        f"(esperado um de: {build_keywords}). CA-006 falhou."
    )


# ---------------------------------------------------------------------------
# CA-007 — Caso de erro: dependências não instaladas
# ---------------------------------------------------------------------------

def test_dev_command_fails_without_node_modules():
    """CA-007: executar 'pnpm run dev' sem node_modules/ resulta em exit code != 0 e mensagem de erro."""
    # Arrange: cria um diretório temporário com package.json mínimo mas SEM node_modules/
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)

        # Copia o package.json real (se existir) para simular projeto sem deps instaladas
        real_package_json = REPO_ROOT / "package.json"
        if real_package_json.exists():
            import shutil as _shutil
            _shutil.copy(real_package_json, tmp_path / "package.json")
        else:
            # Fallback: cria package.json mínimo com script dev apontando para next
            (tmp_path / "package.json").write_text(
                '{"name":"jsaai-frontend","scripts":{"dev":"next dev"},"dependencies":{"next":"15.0.0"}}',
                encoding="utf-8",
            )

        # Garante que node_modules/ NÃO existe no diretório temporário
        node_modules_tmp = tmp_path / "node_modules"
        assert not node_modules_tmp.exists(), (
            "node_modules/ não deveria existir no diretório temporário — setup do teste incorreto."
        )

        pnpm = _find_pnpm()

        # Act: tenta executar pnpm run dev sem dependências instaladas
        result = subprocess.run(
            [pnpm, "run", "dev"],
            cwd=str(tmp_path),
            capture_output=True,
            text=True,
            timeout=30,
        )

        # Assert: processo deve falhar (exit code != 0)
        assert result.returncode != 0, (
            "'pnpm run dev' retornou exit code 0 mesmo sem node_modules/ instalado. "
            "O projeto deveria falhar com erro claro. CA-007 falhou."
        )

        # Assert: saída de erro deve conter indicação do problema
        combined_output = (result.stdout or "") + (result.stderr or "")
        error_indicators = [
            "not found",
            "Cannot find",
            "Module not found",
            "ERR",
            "error",
            "ENOENT",
            "missing",
            "next: command not found",
            "next" ,
        ]
        has_error_message = any(
            indicator.lower() in combined_output.lower() for indicator in error_indicators
        )
        assert has_error_message, (
            "'pnpm run dev' falhou (exit code != 0) mas não exibiu mensagem de erro reconhecível. "
            f"Output combinado:\n{combined_output}\nCA-007 falhou."
        )

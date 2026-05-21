"""Testes RED para 003-react-bootstrap-home — frontend-bootstrap.

Stack: Python/pytest controlando subprocessos e sistema de arquivos.
Os testes DEVEM falhar (red) enquanto o código de produção não existir.
"""

import os
import shutil
import subprocess
import time
import socket
import threading
import urllib.request
import urllib.error
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

# Raiz do repositório: dois níveis acima de tests/frontend-bootstrap/
REPO_ROOT = Path(__file__).resolve().parents[2]


def _find_free_port() -> int:
    """Retorna uma porta livre no loopback."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        return s.getsockname()[1]


def _detect_pkg_manager() -> str:
    """Retorna 'pnpm' se disponível, senão 'npm'."""
    if shutil.which("pnpm"):
        return "pnpm"
    return "npm"


def _wait_for_port(host: str, port: int, timeout: float = 30.0) -> bool:
    """Aguarda até timeout segundos até a porta responder."""
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        try:
            with socket.create_connection((host, port), timeout=1):
                return True
        except OSError:
            time.sleep(0.5)
    return False


# ---------------------------------------------------------------------------
# CA-001 — Servidor de desenvolvimento inicia sem erros
# ---------------------------------------------------------------------------

def test_dev_server_starts_without_errors():
    """CA-001: servidor de desenvolvimento inicia sem erros e expõe URL local."""
    # Arrange
    pkg = _detect_pkg_manager()
    node_modules = REPO_ROOT / "node_modules"
    assert node_modules.exists(), (
        f"node_modules não encontrado em {node_modules}. "
        "Execute `pnpm install` (ou `npm install`) antes de rodar os testes."
    )

    dev_port = 3000  # porta padrão do Next.js
    env = {**os.environ, "PORT": str(dev_port)}

    # Act — inicia servidor em background
    proc = subprocess.Popen(
        [pkg, "run", "dev"],
        cwd=REPO_ROOT,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )

    try:
        server_up = _wait_for_port("localhost", dev_port, timeout=30)
        output_lines = []
        # Lê algumas linhas do stdout para verificar URL
        t_end = time.monotonic() + 5
        while time.monotonic() < t_end:
            line = proc.stdout.readline()
            if line:
                output_lines.append(line)
            if any("localhost" in l for l in output_lines):
                break

        # Assert
        assert server_up, (
            f"Servidor de desenvolvimento não respondeu na porta {dev_port} em 30 s. "
            f"Saída parcial: {''.join(output_lines[:20])}"
        )
        assert proc.returncode is None, (
            f"Processo dev encerrou prematuramente com código {proc.returncode}."
        )
        combined_output = "".join(output_lines)
        assert "localhost" in combined_output or server_up, (
            f"URL local não encontrada no output do servidor. Output: {combined_output[:500]}"
        )
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()


# ---------------------------------------------------------------------------
# CA-002 — Página inicial exibe apenas o texto "funcionou"
# ---------------------------------------------------------------------------

def test_home_displays_only_funcionou_text():
    """CA-002: a única mensagem visível na página inicial é o texto exato 'funcionou'."""
    # Arrange
    pkg = _detect_pkg_manager()
    node_modules = REPO_ROOT / "node_modules"
    assert node_modules.exists(), "node_modules ausente — rode pnpm install."

    dev_port = 3001  # porta alternativa para evitar conflito com CA-001
    env = {**os.environ, "PORT": str(dev_port)}

    proc = subprocess.Popen(
        [pkg, "run", "dev"],
        cwd=REPO_ROOT,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )

    try:
        server_up = _wait_for_port("localhost", dev_port, timeout=30)
        assert server_up, f"Servidor não subiu na porta {dev_port} em 30 s."

        # Act
        with urllib.request.urlopen(f"http://localhost:{dev_port}/", timeout=10) as resp:
            html_body = resp.read().decode("utf-8", errors="replace")

        # Assert — texto "funcionou" deve estar presente
        assert "funcionou" in html_body, (
            f"Texto 'funcionou' não encontrado no HTML retornado. "
            f"Início do body: {html_body[:300]}"
        )

        # Textos de boilerplate do create-next-app NÃO devem aparecer
        unwanted_phrases = [
            "Get started",
            "Edit src",
            "Vercel",
            "Deploy now",
            "by running",
            "Learn more",
        ]
        for phrase in unwanted_phrases:
            assert phrase not in html_body, (
                f"Texto indesejado de boilerplate encontrado: '{phrase}'. "
                "A página deve exibir APENAS 'funcionou'."
            )
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()


# ---------------------------------------------------------------------------
# CA-003 — Texto "funcionou" está centralizado na viewport
# ---------------------------------------------------------------------------

def test_funcionou_text_is_centered():
    """CA-003: o texto 'funcionou' está centralizado vertical e horizontalmente via CSS flexbox."""
    # Arrange — verificação via arquivo CSS estático (não requer browser headless)
    # De acordo com o plan.md, a centralização é feita via globals.css com flexbox.

    # Possíveis localizações do globals.css (com ou sem src/ dir)
    candidate_css_paths = [
        REPO_ROOT / "src" / "app" / "globals.css",
        REPO_ROOT / "app" / "globals.css",
    ]
    css_file = next((p for p in candidate_css_paths if p.exists()), None)
    assert css_file is not None, (
        f"globals.css não encontrado. Candidatos verificados: {candidate_css_paths}"
    )

    # Act
    css_content = css_file.read_text(encoding="utf-8")

    # Assert — regras de centralização obrigatórias
    assert "display" in css_content and "flex" in css_content, (
        f"'display: flex' não encontrado em {css_file}. "
        "A centralização deve ser feita via flexbox."
    )
    assert "align-items" in css_content, (
        f"'align-items' não encontrado em {css_file}. "
        "Necessário para centralização vertical."
    )
    assert "justify-content" in css_content, (
        f"'justify-content' não encontrado em {css_file}. "
        "Necessário para centralização horizontal."
    )
    # Deve haver regra de altura mínima para cobrir a viewport
    assert "100vh" in css_content or "100dvh" in css_content, (
        f"Nenhuma regra de altura '100vh' ou '100dvh' encontrada em {css_file}. "
        "O container deve ocupar a altura total da viewport."
    )

    # Verifica também que page.tsx usa <main> ou container adequado
    candidate_page_paths = [
        REPO_ROOT / "src" / "app" / "page.tsx",
        REPO_ROOT / "app" / "page.tsx",
    ]
    page_file = next((p for p in candidate_page_paths if p.exists()), None)
    assert page_file is not None, (
        f"page.tsx não encontrado. Candidatos: {candidate_page_paths}"
    )
    page_content = page_file.read_text(encoding="utf-8")
    assert "funcionou" in page_content, (
        f"Texto 'funcionou' não encontrado em {page_file}."
    )


# ---------------------------------------------------------------------------
# CA-004 — Build de produção executa sem erros
# ---------------------------------------------------------------------------

def test_production_build_succeeds():
    """CA-004: `pnpm build` (ou `npm run build`) finaliza com exit code 0 e gera bundle."""
    # Arrange
    pkg = _detect_pkg_manager()
    node_modules = REPO_ROOT / "node_modules"
    assert node_modules.exists(), "node_modules ausente — rode pnpm install."

    # Remove build anterior para garantir teste limpo
    next_dir = REPO_ROOT / ".next"
    if next_dir.exists():
        shutil.rmtree(next_dir)

    # Act
    result = subprocess.run(
        [pkg, "run", "build"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        timeout=120,  # builds do Next.js podem demorar
    )

    # Assert
    assert result.returncode == 0, (
        f"Build falhou com exit code {result.returncode}.\n"
        f"STDOUT:\n{result.stdout[-2000:]}\n"
        f"STDERR:\n{result.stderr[-2000:]}"
    )
    # Diretório de saída do Next.js deve existir após build bem-sucedido
    assert next_dir.exists(), (
        f"Diretório .next/ não encontrado após build em {REPO_ROOT}. "
        "O build pode ter falhado silenciosamente."
    )
    # Deve haver pelo menos um arquivo JS gerado
    js_files = list(next_dir.rglob("*.js"))
    assert len(js_files) > 0, (
        f"Nenhum arquivo .js encontrado em {next_dir} após o build."
    )


# ---------------------------------------------------------------------------
# CA-005 — Repositório contém estrutura mínima organizada
# ---------------------------------------------------------------------------

def test_repository_has_minimum_structure():
    """CA-005: repositório contém package.json, src/ (ou app/), README.md e .gitignore correto."""
    # Arrange / Act / Assert — verificações de sistema de arquivos

    # package.json na raiz
    package_json = REPO_ROOT / "package.json"
    assert package_json.exists(), (
        f"package.json não encontrado na raiz do repositório ({REPO_ROOT})."
    )

    # Conteúdo mínimo do package.json
    import json
    pkg_data = json.loads(package_json.read_text(encoding="utf-8"))
    assert "scripts" in pkg_data, "package.json não contém a chave 'scripts'."
    assert "dev" in pkg_data["scripts"], (
        "package.json não contém script 'dev' em 'scripts'."
    )
    assert "build" in pkg_data["scripts"], (
        "package.json não contém script 'build' em 'scripts'."
    )

    # Estrutura de código-fonte React (src/app/ ou app/)
    src_app_dir = REPO_ROOT / "src" / "app"
    app_dir = REPO_ROOT / "app"
    has_src_dir = src_app_dir.exists() or app_dir.exists()
    assert has_src_dir, (
        f"Nenhum diretório de fonte React encontrado. "
        f"Verificados: {src_app_dir}, {app_dir}"
    )

    # README.md na raiz
    readme = REPO_ROOT / "README.md"
    assert readme.exists(), (
        f"README.md não encontrado na raiz do repositório ({REPO_ROOT})."
    )

    # .gitignore existente e contendo node_modules
    gitignore = REPO_ROOT / ".gitignore"
    assert gitignore.exists(), (
        f".gitignore não encontrado na raiz do repositório ({REPO_ROOT})."
    )
    gitignore_content = gitignore.read_text(encoding="utf-8")
    assert "node_modules" in gitignore_content, (
        ".gitignore não contém entrada para 'node_modules'. "
        "Diretório de dependências não deve ser versionado."
    )
    # .next/ também deve estar no .gitignore
    assert ".next" in gitignore_content, (
        ".gitignore não contém entrada para '.next'. "
        "O diretório de build do Next.js não deve ser versionado."
    )


# ---------------------------------------------------------------------------
# CA-006 — README contém instruções de execução
# ---------------------------------------------------------------------------

def test_readme_contains_execution_instructions():
    """CA-006: README.md contém instruções para instalar dependências, rodar dev e build."""
    # Arrange
    readme = REPO_ROOT / "README.md"
    assert readme.exists(), (
        f"README.md não encontrado em {REPO_ROOT}. "
        "Crie o arquivo conforme especificado na CA-006."
    )

    # Act
    readme_content = readme.read_text(encoding="utf-8")

    # Assert — instrução de instalação de dependências
    install_indicators = ["pnpm install", "npm install", "yarn install", "install"]
    has_install = any(kw in readme_content for kw in install_indicators)
    assert has_install, (
        f"README.md não contém instrução de instalação de dependências. "
        f"Esperado: algum de {install_indicators}.\nConteúdo: {readme_content[:500]}"
    )

    # Assert — instrução para iniciar servidor de desenvolvimento
    dev_indicators = ["pnpm dev", "npm run dev", "yarn dev", "run dev"]
    has_dev = any(kw in readme_content for kw in dev_indicators)
    assert has_dev, (
        f"README.md não contém instrução para iniciar o servidor de desenvolvimento. "
        f"Esperado: algum de {dev_indicators}.\nConteúdo: {readme_content[:500]}"
    )

    # Assert — instrução para executar build de produção
    build_indicators = ["pnpm build", "npm run build", "yarn build", "run build"]
    has_build = any(kw in readme_content for kw in build_indicators)
    assert has_build, (
        f"README.md não contém instrução para build de produção. "
        f"Esperado: algum de {build_indicators}.\nConteúdo: {readme_content[:500]}"
    )


# ---------------------------------------------------------------------------
# CA-007 — Caso de erro: dependências não instaladas
# ---------------------------------------------------------------------------

def test_dev_command_fails_without_node_modules(tmp_path):
    """CA-007: `dev` falha com exit code != 0 quando node_modules não existe."""
    # Arrange — cria um mini-projeto Next.js simulado SEM node_modules
    # para garantir isolamento e não destruir o repositório real.
    fake_project = tmp_path / "fake_next_project"
    fake_project.mkdir()

    # package.json mínimo apontando para script dev com next
    import json
    package_json_content = {
        "name": "fake-next-project",
        "version": "0.1.0",
        "private": True,
        "scripts": {
            "dev": "next dev",
            "build": "next build"
        },
        "dependencies": {
            "next": "15.0.0",
            "react": "19.0.0",
            "react-dom": "19.0.0"
        }
    }
    (fake_project / "package.json").write_text(
        json.dumps(package_json_content, indent=2), encoding="utf-8"
    )

    # Garante que node_modules NÃO existe neste diretório temporário
    node_modules_fake = fake_project / "node_modules"
    assert not node_modules_fake.exists(), (
        "node_modules não deveria existir no diretório temporário de teste."
    )

    pkg = _detect_pkg_manager()

    # Act — tenta rodar dev sem node_modules (processo com timeout curto)
    result = subprocess.run(
        [pkg, "run", "dev"],
        cwd=fake_project,
        capture_output=True,
        text=True,
        timeout=15,  # deve falhar rapidamente
    )

    # Assert — deve falhar (exit code != 0)
    assert result.returncode != 0, (
        f"Esperado falha (exit code != 0) ao rodar '{pkg} run dev' sem node_modules, "
        f"mas o processo retornou exit code {result.returncode}.\n"
        f"STDOUT: {result.stdout[:500]}\n"
        f"STDERR: {result.stderr[:500]}"
    )

    # Deve haver mensagem de erro no output
    combined_output = (result.stdout + result.stderr).lower()
    error_indicators = [
        "not found",
        "cannot find",
        "module not found",
        "missing",
        "error",
        "enoent",
        "command not found",
        "no such file",
    ]
    has_error_message = any(indicator in combined_output for indicator in error_indicators)
    assert has_error_message, (
        f"Nenhuma mensagem de erro reconhecível encontrada no output ao rodar sem node_modules. "
        f"Output combinado: {(result.stdout + result.stderr)[:500]}"
    )

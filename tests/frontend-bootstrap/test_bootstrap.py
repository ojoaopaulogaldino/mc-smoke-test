import os
import subprocess
import time
import shutil
import threading
import re
from pathlib import Path

import pytest

# Detecta raiz do repositório (dois níveis acima de tests/frontend-bootstrap/)
REPO_ROOT = Path(__file__).resolve().parents[2]


def test_dev_server_starts_without_errors():
    """CA-001: Servidor de desenvolvimento inicia sem erros e exibe URL local acessível."""
    # Arrange
    package_json = REPO_ROOT / "package.json"
    assert package_json.exists(), "package.json não encontrado — projeto não inicializado"

    pnpm_exec = shutil.which("pnpm") or shutil.which("npm")
    assert pnpm_exec is not None, "nenhum gerenciador de pacotes (pnpm/npm) encontrado no PATH"

    node_modules = REPO_ROOT / "node_modules"
    assert node_modules.exists(), "node_modules ausente — execute pnpm install antes dos testes CA-001"

    output_lines = []
    error_lines = []
    url_found = threading.Event()
    process_ref = []

    def run_dev():
        proc = subprocess.Popen(
            [pnpm_exec, "run", "dev"],
            cwd=str(REPO_ROOT),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
        process_ref.append(proc)
        for line in proc.stdout:
            output_lines.append(line)
            # Next.js imprime algo como "http://localhost:3000" quando pronto
            if re.search(r"http://localhost:\d+", line, re.IGNORECASE) or \
               re.search(r"ready\s+(started|in|on)", line, re.IGNORECASE) or \
               re.search(r"Local:\s+http", line, re.IGNORECASE):
                url_found.set()

    # Act
    t = threading.Thread(target=run_dev, daemon=True)
    t.start()
    server_ready = url_found.wait(timeout=30)

    # Assert
    try:
        assert server_ready, (
            f"Servidor dev não ficou pronto em 30 segundos. "
            f"Saída capturada:\n{''.join(output_lines)}"
        )
        combined = "".join(output_lines)
        url_match = re.search(r"http://localhost:\d+", combined, re.IGNORECASE)
        assert url_match is not None, (
            f"Nenhuma URL local (http://localhost:PORT) encontrada na saída.\n{combined}"
        )
    finally:
        if process_ref:
            process_ref[0].terminate()
            try:
                process_ref[0].wait(timeout=5)
            except subprocess.TimeoutExpired:
                process_ref[0].kill()


def test_home_displays_only_funcionou_text():
    """CA-002: Página inicial exibe apenas o texto 'funcionou'."""
    # Arrange
    page_tsx = REPO_ROOT / "src" / "app" / "page.tsx"
    if not page_tsx.exists():
        page_tsx = REPO_ROOT / "app" / "page.tsx"

    assert page_tsx.exists(), (
        f"Arquivo page.tsx não encontrado em src/app/page.tsx nem em app/page.tsx. "
        f"Raiz verificada: {REPO_ROOT}"
    )

    # Act
    content = page_tsx.read_text(encoding="utf-8")

    # Assert — o componente deve conter o texto 'funcionou' e não deve conter textos de boilerplate
    assert "funcionou" in content, (
        "O texto 'funcionou' não foi encontrado em page.tsx"
    )

    boilerplate_terms = [
        "Get started",
        "Edit src/app",
        "Deploy now",
        "Read our docs",
        "vercel.com",
        "next.js",
        "Learn",
    ]
    found_boilerplate = [t for t in boilerplate_terms if t.lower() in content.lower()]
    assert not found_boilerplate, (
        f"Boilerplate do template Next.js ainda presente em page.tsx: {found_boilerplate}"
    )


def test_funcionou_text_is_centered():
    """CA-003: Texto 'funcionou' está centralizado vertical e horizontalmente na viewport."""
    # Arrange
    globals_css = REPO_ROOT / "src" / "app" / "globals.css"
    if not globals_css.exists():
        globals_css = REPO_ROOT / "app" / "globals.css"

    assert globals_css.exists(), (
        f"globals.css não encontrado. Raiz: {REPO_ROOT}"
    )

    # Act
    css_content = globals_css.read_text(encoding="utf-8")

    # Assert — centralização via flexbox ou grid
    has_flex_or_grid = (
        re.search(r"display\s*:\s*flex", css_content) or
        re.search(r"display\s*:\s*grid", css_content)
    )
    assert has_flex_or_grid, (
        "globals.css deve conter 'display: flex' ou 'display: grid' para centralização"
    )

    has_align_center = (
        re.search(r"align-items\s*:\s*center", css_content) or
        re.search(r"place-items\s*:\s*center", css_content)
    )
    assert has_align_center, (
        "globals.css deve conter 'align-items: center' (ou 'place-items: center') para centralização vertical"
    )

    has_justify_center = (
        re.search(r"justify-content\s*:\s*center", css_content) or
        re.search(r"place-items\s*:\s*center", css_content)
    )
    assert has_justify_center, (
        "globals.css deve conter 'justify-content: center' (ou 'place-items: center') para centralização horizontal"
    )

    has_full_height = (
        re.search(r"min-height\s*:\s*100vh", css_content) or
        re.search(r"height\s*:\s*100vh", css_content) or
        re.search(r"min-height\s*:\s*100%", css_content)
    )
    assert has_full_height, (
        "globals.css deve conter 'min-height: 100vh' (ou equivalente) para ocupar a viewport inteira"
    )


def test_production_build_succeeds():
    """CA-004: Build de produção executa sem erros, exit code 0, bundle gerado."""
    # Arrange
    package_json = REPO_ROOT / "package.json"
    assert package_json.exists(), "package.json não encontrado"

    pnpm_exec = shutil.which("pnpm") or shutil.which("npm")
    assert pnpm_exec is not None, "gerenciador de pacotes não encontrado"

    node_modules = REPO_ROOT / "node_modules"
    assert node_modules.exists(), "node_modules ausente — execute pnpm install antes"

    # Act
    result = subprocess.run(
        [pnpm_exec, "run", "build"],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        timeout=120,
    )

    # Assert
    assert result.returncode == 0, (
        f"pnpm build falhou com exit code {result.returncode}.\n"
        f"STDOUT:\n{result.stdout}\n"
        f"STDERR:\n{result.stderr}"
    )

    # Next.js gera o bundle em .next/
    next_dir = REPO_ROOT / ".next"
    assert next_dir.exists(), (
        f"Diretório de build '.next/' não foi gerado após pnpm build. "
        f"Verificado em: {next_dir}"
    )

    build_manifest = next_dir / "build-manifest.json"
    server_dir = next_dir / "server"
    assert build_manifest.exists() or server_dir.exists(), (
        "Artefatos de build esperados (.next/build-manifest.json ou .next/server/) não encontrados"
    )


def test_repository_has_minimum_structure():
    """CA-005: Repositório contém estrutura mínima: package.json, src/, README.md, .gitignore com node_modules/."""
    # Arrange / Act / Assert
    package_json = REPO_ROOT / "package.json"
    assert package_json.exists(), (
        f"package.json ausente na raiz do repositório: {REPO_ROOT}"
    )

    # src/ pode estar em src/app/ ou direto em app/ (App Router sem src dir)
    src_dir = REPO_ROOT / "src"
    app_dir = REPO_ROOT / "app"
    assert src_dir.exists() or app_dir.exists(), (
        f"Nenhum diretório de código-fonte encontrado (src/ ou app/) em {REPO_ROOT}"
    )

    # Verifica que há pelo menos um arquivo .tsx dentro
    tsx_files = list((src_dir if src_dir.exists() else app_dir).rglob("*.tsx"))
    assert len(tsx_files) > 0, (
        "Nenhum arquivo .tsx encontrado dentro do diretório de código-fonte"
    )

    readme = REPO_ROOT / "README.md"
    assert readme.exists(), (
        f"README.md ausente na raiz do repositório: {REPO_ROOT}"
    )

    gitignore = REPO_ROOT / ".gitignore"
    assert gitignore.exists(), (
        f".gitignore ausente na raiz do repositório: {REPO_ROOT}"
    )

    gitignore_content = gitignore.read_text(encoding="utf-8")
    assert "node_modules" in gitignore_content, (
        ".gitignore não contém 'node_modules' — node_modules pode ser commitado acidentalmente"
    )


def test_readme_contains_execution_instructions():
    """CA-006: README.md contém instruções de instalação, comando dev e comando build."""
    # Arrange
    readme = REPO_ROOT / "README.md"
    assert readme.exists(), f"README.md não encontrado em {REPO_ROOT}"

    # Act
    content = readme.read_text(encoding="utf-8")

    # Assert — deve conter referência à instalação de dependências
    has_install = (
        re.search(r"pnpm install", content, re.IGNORECASE) or
        re.search(r"npm install", content, re.IGNORECASE) or
        re.search(r"yarn install", content, re.IGNORECASE) or
        re.search(r"instala", content, re.IGNORECASE)
    )
    assert has_install, (
        "README.md não contém instrução para instalar dependências (ex: 'pnpm install')"
    )

    # Assert — deve conter comando para iniciar servidor de desenvolvimento
    has_dev = (
        re.search(r"pnpm (run )?dev", content, re.IGNORECASE) or
        re.search(r"npm run dev", content, re.IGNORECASE) or
        re.search(r"yarn dev", content, re.IGNORECASE)
    )
    assert has_dev, (
        "README.md não contém comando para iniciar servidor de desenvolvimento (ex: 'pnpm dev')"
    )

    # Assert — deve conter comando de build
    has_build = (
        re.search(r"pnpm (run )?build", content, re.IGNORECASE) or
        re.search(r"npm run build", content, re.IGNORECASE) or
        re.search(r"yarn build", content, re.IGNORECASE)
    )
    assert has_build, (
        "README.md não contém comando de build de produção (ex: 'pnpm build')"
    )


def test_dev_command_fails_without_node_modules():
    """CA-007: Executar comando dev sem node_modules/ resulta em exit code != 0 com mensagem de erro."""
    # Arrange
    package_json = REPO_ROOT / "package.json"
    assert package_json.exists(), "package.json não encontrado"

    pnpm_exec = shutil.which("pnpm") or shutil.which("npm")
    assert pnpm_exec is not None, "gerenciador de pacotes não encontrado"

    # Simular ausência de node_modules usando um diretório temporário sem node_modules
    import tempfile
    import json

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)

        # Copiar package.json para o diretório temporário sem instalar dependências
        original_pkg = json.loads(package_json.read_text(encoding="utf-8"))
        (tmp_path / "package.json").write_text(
            json.dumps(original_pkg), encoding="utf-8"
        )

        # Garantir que node_modules NÃO existe
        assert not (tmp_path / "node_modules").exists(), (
            "node_modules não deveria existir no diretório temporário"
        )

        # Act — tentar rodar dev sem node_modules
        result = subprocess.run(
            [pnpm_exec, "run", "dev"],
            cwd=str(tmp_path),
            capture_output=True,
            text=True,
            timeout=15,
        )

    # Assert — deve falhar (exit code != 0)
    assert result.returncode != 0, (
        f"Esperado falha (exit code != 0) ao rodar dev sem node_modules, "
        f"mas o processo retornou exit code {result.returncode}.\n"
        f"STDOUT: {result.stdout}\nSTDERR: {result.stderr}"
    )

    combined_output = result.stdout + result.stderr
    has_error_message = len(combined_output.strip()) > 0
    assert has_error_message, (
        "Nenhuma mensagem de erro exibida ao tentar rodar dev sem node_modules"
    )

"""Testes RED para 001-health-endpoint — platform-observability.

Escritos em modo CURRANTE: todos devem falhar (red) enquanto o código de produção
(`modules/platform_observability/application/health_router.py` + `app/main.py`) não existir.

Stack: Python 3.12 + FastAPI 0.110+ + pytest (uv)
"""
import json
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient


def _build_client() -> TestClient:
    """Importa a aplicação real de produção.

    Esta função DEVE falhar com ImportError enquanto app/main.py não existir,
    garantindo o estado RED exigido pelo fluxo CURRANTE.
    """
    # Importação dentro da função para que o módulo de testes seja coletável
    # pelo pytest mesmo que o código de produção ainda não exista — o erro
    # só ocorre na execução do teste, não na fase de coleta.
    from app.main import app  # noqa: PLC0415  # produção ainda não existe → ImportError RED
    return TestClient(app)


# ---------------------------------------------------------------------------
# CA-001
# ---------------------------------------------------------------------------

def test_health_returns_200_with_ok_body():
    """CA-001: GET /health retorna HTTP 200 e corpo JSON exato {\"status\": \"ok\"}.

    Dado que o serviço está em execução
    Quando uma requisição GET /health é enviada sem body e sem headers especiais
    Então a resposta HTTP deve ter status code 200
    E o corpo da resposta deve ser exatamente {"status": "ok"}
    """
    # Arrange
    client = _build_client()

    # Act
    response = client.get("/health")

    # Assert — status code
    assert response.status_code == 200, (
        f"Esperado HTTP 200, obtido {response.status_code}. "
        "Verifique se o router health está registrado em app/main.py."
    )

    # Assert — corpo exato (RF-002: exatamente {"status": "ok"}, sem campos extras)
    body = response.json()
    assert body == {"status": "ok"}, (
        f"Corpo esperado: {{\"status\": \"ok\"}}, obtido: {body}. "
        "Use JSONResponse direto com dict literal, não modelo Pydantic com campos opcionais."
    )


# ---------------------------------------------------------------------------
# CA-002
# ---------------------------------------------------------------------------

def test_health_returns_json_content_type():
    """CA-002: GET /health responde com Content-Type contendo 'application/json'.

    Dado que o serviço está em execução
    Quando uma requisição GET /health é enviada
    Então o header Content-Type da resposta deve conter 'application/json'
    """
    # Arrange
    client = _build_client()

    # Act
    response = client.get("/health")

    # Assert
    content_type = response.headers.get("content-type", "")
    assert "application/json" in content_type, (
        f"Content-Type esperado conter 'application/json', obtido: '{content_type}'. "
        "Garanta que a resposta é JSONResponse (FastAPI padrão) e não PlainTextResponse."
    )


# ---------------------------------------------------------------------------
# CA-003
# ---------------------------------------------------------------------------

def test_health_post_returns_405():
    """CA-003: POST /health retorna HTTP 405 Method Not Allowed sem expor informações internas.

    Dado que o serviço está em execução
    Quando uma requisição POST /health é enviada (método não suportado)
    Então a resposta HTTP deve ter status code 405
    E o corpo não deve conter stack traces ou informações internas de infraestrutura
    """
    # Arrange
    client = _build_client()

    # Act
    response = client.post("/health", json={})

    # Assert — código HTTP
    assert response.status_code == 405, (
        f"Esperado HTTP 405 Method Not Allowed, obtido {response.status_code}. "
        "FastAPI deve rejeitar métodos não registrados automaticamente."
    )

    # Assert — ausência de informações internas sensíveis no corpo
    raw_body = response.text.lower()

    FORBIDDEN_PATTERNS = [
        "traceback",
        "stack trace",
        "file \"",        # caminho de arquivo Python em traceback
        "line ",          # linha de traceback
        "exception",
        "internal server",
        "sqlalchemy",
        "postgres",
        "redis",
        "secret",
        "password",
        "token",
    ]

    for pattern in FORBIDDEN_PATTERNS:
        assert pattern not in raw_body, (
            f"Corpo da resposta 405 expõe informação interna proibida: '{pattern}'. "
            f"Corpo recebido: {response.text[:300]!r}"
        )

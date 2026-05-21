"""Testes RED para feature 001-health-endpoint (platform-observability).

Modo CURRANTE: todos os testes devem falhar (red) pois o código de produção ainda não existe.
Stack: Python 3.12 + FastAPI 0.110+ + pytest
"""
import json
import pytest


def _get_test_client():
    """Importa o app FastAPI e retorna o TestClient.
    Encapsulado em função para que o ImportError ocorra em runtime (no teste),
    não na coleta — permitindo que o pytest colete os testes mesmo sem código de produção.
    """
    from fastapi.testclient import TestClient  # fastapi já é dependência declarada
    from app.main import app  # ainda não existe — causará ImportError (red)
    return TestClient(app)


def test_health_returns_200_with_ok_body():
    """CA-001: GET /health retorna HTTP 200 com body exatamente {\"status\": \"ok\"}.

    Dado que o serviço está em execução e acessível
    Quando um cliente envia uma requisição GET /health
    Então a resposta deve ter status HTTP 200
    E o body da resposta deve ser exatamente {"status": "ok"}
    """
    # Arrange
    client = _get_test_client()

    # Act
    response = client.get("/health")

    # Assert
    assert response.status_code == 200, (
        f"CA-001: esperado HTTP 200, obtido {response.status_code}"
    )
    body = response.json()
    assert body == {"status": "ok"}, (
        f"CA-001: body esperado {{\"status\": \"ok\"}}, obtido {json.dumps(body)}"
    )


def test_health_returns_json_content_type():
    """CA-002: GET /health retorna header Content-Type contendo application/json.

    Dado que o serviço está em execução e acessível
    Quando um cliente envia uma requisição GET /health
    Então o header Content-Type da resposta deve conter application/json
    """
    # Arrange
    client = _get_test_client()

    # Act
    response = client.get("/health")

    # Assert
    content_type = response.headers.get("content-type", "")
    assert "application/json" in content_type, (
        f"CA-002: Content-Type esperado conter 'application/json', obtido '{content_type}'"
    )


def test_health_method_not_allowed():
    """CA-003: POST /health retorna HTTP 405 (método não permitido).

    Dado que o serviço está em execução e acessível
    Quando um cliente envia uma requisição POST /health
    Então a resposta deve ter status HTTP 405
    """
    # Arrange
    client = _get_test_client()

    # Act
    response = client.post("/health")

    # Assert
    assert response.status_code == 405, (
        f"CA-003: esperado HTTP 405 para POST /health, obtido {response.status_code}"
    )

from fastapi.testclient import TestClient

from app.core.config import settings


def test_pec_mock_configuracoes(client: TestClient) -> None:
    response = client.post(
        f"{settings.API_V1_STR}/pec/mock/graphql",
        json={"operationName": "Configuracoes", "variables": {}},
    )

    assert response.status_code == 200
    assert response.json()[0]["data"]["info"]["versao"] == "5.4.36"


def test_pec_mock_login_sets_session_cookie(client: TestClient) -> None:
    response = client.post(
        f"{settings.API_V1_STR}/pec/mock/graphql",
        json={
            "operationName": "Login",
            "variables": {"input": {"username": "12345678901", "password": "Senha1234!"}},
        },
    )

    assert response.status_code == 200
    assert response.json()[0]["data"]["login"]["success"] is True
    assert "pec_mock_session" in response.cookies

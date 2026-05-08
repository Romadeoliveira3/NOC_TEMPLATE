from __future__ import annotations

from copy import deepcopy
from typing import Any


def _normalize_username(username: str) -> str:
    return "".join(char for char in username if char.isdigit())


def _session_snapshot(
    username: str,
    session_id: str,
    users: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    profissional = deepcopy(users[username]["profissional"])
    return {
        "id": session_id,
        "timeout": 3610,
        "expDateAccessTokenGovBr": None,
        "recursos": [
            "/cidadao/read",
            "/cidadao/detail",
            "/agenda/read",
        ],
        "sessionProvider": "PEC",
        "acesso": None,
        "profissional": profissional,
        "__typename": "Sessao",
    }


def _unsupported_operation(operation_name: str) -> dict[str, Any]:
    return {
        "data": None,
        "errors": [{"message": f"Unsupported operation: {operation_name}"}],
    }

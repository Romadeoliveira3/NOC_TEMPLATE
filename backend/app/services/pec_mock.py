from __future__ import annotations

from copy import deepcopy
from typing import Any
from uuid import uuid4

from fastapi import Response

from app.schemas.pec_mock import PecMockOperation
from app.services.helpers.pec_mock import (
    _normalize_username,
    _session_snapshot,
    _unsupported_operation,
)
from app.services.helpers.pec_mock_data import (
    MOCK_CONFIG,
    MOCK_FLAGS,
    MOCK_PEC_USERS,
    SESSION_COOKIE_NAME,
)

MOCK_SESSIONS: dict[str, dict[str, Any]] = {}


def process_pec_mock_operations(
    operations: list[PecMockOperation] | PecMockOperation,
    response: Response,
    pec_mock_session: str | None,
) -> list[dict[str, Any]]:
    operation_list = operations if isinstance(operations, list) else [operations]
    current_session = MOCK_SESSIONS.get(pec_mock_session) if pec_mock_session else None
    results: list[dict[str, Any]] = []

    for operation in operation_list:
        operation_name = operation.operationName
        variables = operation.variables or {}

        if operation_name == "Configuracoes":
            results.append({"data": {"info": deepcopy(MOCK_CONFIG)}})
            continue

        if operation_name == "Flags":
            results.append(
                {
                    "data": {
                        "info": {
                            "id": "1",
                            "flags": deepcopy(MOCK_FLAGS),
                            "__typename": "Info",
                        }
                    }
                }
            )
            continue

        if operation_name == "Sessao":
            sessao = deepcopy(current_session["sessao"]) if current_session else None
            results.append({"data": {"sessao": sessao}})
            continue

        if operation_name == "Login":
            input_data = variables.get("input", {})
            username = _normalize_username(str(input_data.get("username", "")))
            password = str(input_data.get("password", ""))
            user = MOCK_PEC_USERS.get(username)

            if not user or user["password"] != password:
                results.append(
                    {
                        "data": {
                            "login": {
                                "success": False,
                                "__typename": "LoginPayload",
                            }
                        },
                        "errors": [{"message": "BadCredentialsException"}],
                    }
                )
                continue

            session_id = str(uuid4())
            session_snapshot = _session_snapshot(username, session_id, MOCK_PEC_USERS)
            MOCK_SESSIONS[session_id] = {
                "username": username,
                "sessao": session_snapshot,
            }
            current_session = MOCK_SESSIONS[session_id]
            response.set_cookie(
                key=SESSION_COOKIE_NAME,
                value=session_id,
                httponly=True,
                samesite="lax",
            )
            results.append(
                {
                    "data": {
                        "login": {
                            "success": True,
                            "__typename": "LoginPayload",
                        }
                    }
                }
            )
            continue

        results.append(_unsupported_operation(operation_name))

    return results

from __future__ import annotations

from copy import deepcopy
from typing import Any
from uuid import uuid4

from fastapi import Response

from app.schemas.pec_mock import PecMockOperation
from app.services.helpers.pec_mock import (
    _citizen_basic,
    _citizen_detail,
    _citizen_header,
    _extract_terms,
    _find_citizen_by_id,
    _normalize_username,
    _not_authenticated_error,
    _now_millis,
    _search_citizens,
    _session_snapshot,
    _unsupported_operation,
)
from app.services.helpers.pec_mock_data import (
    MOCK_CITIZENS,
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

        if operation_name == "ConfiguracaoVideochamadas":
            results.append(
                {
                    "data": {
                        "conexao": {
                            "videochamadas": {
                                "id": "1",
                                "habilitado": False,
                                "__typename": "ConfiguracaoVideochamadas",
                            },
                            "__typename": "ConfiguracaoConexao",
                        }
                    }
                }
            )
            continue

        if operation_name == "GetServerTime":
            results.append(
                {
                    "data": {
                        "serverTime": _now_millis(),
                        "serverTimezoneOffset": -180,
                    }
                }
            )
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

        if operation_name == "Logout":
            logout_snapshot = deepcopy(current_session["sessao"]) if current_session else None
            if current_session:
                session_id = current_session["sessao"]["id"]
                MOCK_SESSIONS.pop(session_id, None)
            elif pec_mock_session:
                MOCK_SESSIONS.pop(pec_mock_session, None)
            current_session = None
            response.delete_cookie(key=SESSION_COOKIE_NAME)
            results.append({"data": {"logout": logout_snapshot}})
            continue

        if current_session is None:
            results.append(_not_authenticated_error())
            continue

        if operation_name == "CidadaoAtendimentoPorCpfSelectField":
            terms = _extract_terms(variables.get("input"))
            citizens = _search_citizens(terms, mode="cpf", citizens=MOCK_CITIZENS)
            results.append(
                {
                    "data": {
                        "cidadaosComboByCpf": [_citizen_basic(citizen) for citizen in citizens]
                    }
                }
            )
            continue

        if operation_name == "CidadaoAtendimentoPorNomeSelectField":
            terms = _extract_terms(variables.get("input"))
            citizens = _search_citizens(terms, mode="name", citizens=MOCK_CITIZENS)
            results.append(
                {
                    "data": {
                        "cidadaosComboByNome": [_citizen_basic(citizen) for citizen in citizens]
                    }
                }
            )
            continue

        if operation_name == "CidadaoAtendimentoSelectField":
            terms = _extract_terms(variables.get("input"))
            retrieve_contact = bool(variables.get("retrieveContato", False))
            citizens = _search_citizens(terms, mode="general", citizens=MOCK_CITIZENS)
            results.append(
                {
                    "data": {
                        "cidadaosCombo": [
                            _citizen_basic(citizen)
                            | {
                                "isCidadaoAusente": citizen["isCidadaoAusente"],
                                "contato": (
                                    {
                                        "id": f"contato-{citizen['id']}",
                                        "telefoneCelular": citizen["telefoneCelular"],
                                        "email": citizen["email"],
                                    }
                                    if retrieve_contact
                                    else None
                                ),
                            }
                            for citizen in citizens
                        ]
                    }
                }
            )
            continue

        if operation_name == "AtendimentoHeaderCidadao":
            citizen = _find_citizen_by_id(
                str(variables.get("cidadaoId")),
                citizens=MOCK_CITIZENS,
            )
            if not citizen:
                results.append({"data": {"cidadao": None}})
                continue
            include_contacts = bool(
                variables.get("fetchCidadaoVinculacaoEquipeAndTelefones", False)
            )
            results.append({"data": {"cidadao": _citizen_header(citizen, include_contacts)}})
            continue

        if operation_name == "BuscaDetailCidadao":
            citizen = _find_citizen_by_id(str(variables.get("id")), citizens=MOCK_CITIZENS)
            results.append(
                {
                    "data": {
                        "cidadao": _citizen_detail(citizen) if citizen else None,
                    }
                }
            )
            continue

        if operation_name == "Cidadao":
            citizen = _find_citizen_by_id(str(variables.get("id")), citizens=MOCK_CITIZENS)
            if not citizen:
                results.append({"data": {"cidadao": None}})
                continue
            results.append(
                {
                    "data": {
                        "cidadao": {
                            "id": citizen["id"],
                            "nome": citizen["nome"],
                            "nomeSocial": citizen["nomeSocial"],
                            "cpf": citizen["cpf"],
                            "cns": citizen["cns"],
                            "nomeMae": citizen["nomeMae"],
                            "dataNascimento": citizen["dataNascimento"],
                            "sexo": citizen["sexo"],
                            "identidadeGeneroDbEnum": citizen["identidadeGeneroDbEnum"],
                            "faleceu": citizen["faleceu"],
                            "isCidadaoAusente": citizen["isCidadaoAusente"],
                            "__typename": "Cidadao",
                        }
                    }
                }
            )
            continue

        results.append(_unsupported_operation(operation_name))

    return results

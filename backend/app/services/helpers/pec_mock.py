from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
from typing import Any


def _now_millis() -> int:
    return int(datetime.now(tz=timezone.utc).timestamp() * 1000)


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


def _citizen_basic(citizen: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": citizen["id"],
        "nome": citizen["nome"],
        "nomeSocial": citizen["nomeSocial"],
        "nomeTradicional": citizen["nomeTradicional"],
        "cpf": citizen["cpf"],
        "cns": citizen["cns"],
        "nomeMae": citizen["nomeMae"],
        "dataNascimento": citizen["dataNascimento"],
        "presenteListaAtendimento": False,
        "__typename": "CidadaoBasico",
    }


def _citizen_header(citizen: dict[str, Any], include_contacts: bool) -> dict[str, Any]:
    payload = {
        "id": citizen["id"],
        "cpf": citizen["cpf"],
        "cns": citizen["cns"],
        "nome": citizen["nome"],
        "nomeSocial": citizen["nomeSocial"],
        "nomeTradicional": citizen["nomeTradicional"],
        "dataNascimento": citizen["dataNascimento"],
        "sexo": citizen["sexo"],
        "nomeMae": citizen["nomeMae"],
        "identidadeGeneroDbEnum": citizen["identidadeGeneroDbEnum"],
        "ativo": citizen["ativo"],
        "faleceu": citizen["faleceu"],
        "unificado": citizen["unificado"],
        "unificacaoBase": citizen["unificacaoBase"],
        "__typename": "Cidadao",
    }
    if include_contacts:
        payload["telefoneResidencial"] = citizen["telefoneResidencial"]
        payload["telefoneCelular"] = citizen["telefoneCelular"]
        payload["telefoneContato"] = citizen["telefoneContato"]
        payload["cidadaoVinculacaoEquipe"] = citizen["cidadaoVinculacaoEquipe"]
    return payload


def _citizen_detail(citizen: dict[str, Any]) -> dict[str, Any]:
    return deepcopy(citizen) | {"__typename": "Cidadao"}


def _extract_terms(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        cleaned = value.strip().lower()
        return [cleaned] if cleaned else []
    if isinstance(value, dict):
        terms: list[str] = []
        for item in value.values():
            terms.extend(_extract_terms(item))
        return terms
    if isinstance(value, list):
        terms: list[str] = []
        for item in value:
            terms.extend(_extract_terms(item))
        return terms
    return []


def _find_citizen_by_id(
    cidadao_id: str | None,
    citizens: list[dict[str, Any]],
) -> dict[str, Any] | None:
    if not cidadao_id:
        return None
    for citizen in citizens:
        if citizen["id"] == cidadao_id:
            return citizen
    return None


def _search_citizens(
    terms: list[str],
    mode: str,
    citizens: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    if not terms:
        return deepcopy(citizens)

    numeric_terms = [
        "".join(char for char in term if char.isdigit())
        for term in terms
        if any(char.isdigit() for char in term)
    ]
    matches: list[dict[str, Any]] = []
    for citizen in citizens:
        cpf = citizen["cpf"]
        name = citizen["nome"].lower()
        social_name = (citizen["nomeSocial"] or "").lower()
        cns = citizen["cns"]

        if mode == "cpf":
            if any(term and term in cpf for term in numeric_terms):
                matches.append(deepcopy(citizen))
            continue

        if mode == "name":
            if any(term in name or term in social_name for term in terms):
                matches.append(deepcopy(citizen))
            continue

        if any(
            term in name
            or term in social_name
            or term in cpf
            or term in cns
            or term in citizen["nomeMae"].lower()
            for term in terms
        ):
            matches.append(deepcopy(citizen))

    return matches


def _not_authenticated_error() -> dict[str, Any]:
    return {
        "data": None,
        "errors": [{"message": "NotAuthenticated"}],
    }


def _unsupported_operation(operation_name: str) -> dict[str, Any]:
    return {
        "data": None,
        "errors": [{"message": f"Unsupported operation: {operation_name}"}],
    }

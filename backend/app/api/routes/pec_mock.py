from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from fastapi import APIRouter, Cookie, Response
from pydantic import BaseModel, Field

router = APIRouter(prefix="/pec/mock", tags=["pec-mock"])

SESSION_COOKIE_NAME = "pec_mock_session"


class PecMockOperation(BaseModel):
    operationName: str
    variables: dict[str, Any] = Field(default_factory=dict)
    query: str | None = None


MOCK_SESSIONS: dict[str, dict[str, Any]] = {}

MOCK_CONFIG = {
    "id": "1",
    "smtpConfigurado": False,
    "internetHabilitada": True,
    "linkInstalacaoConfigurado": True,
    "govBREnabled": False,
    "versao": "5.4.36",
    "buscaCidadaoPorPropriedadesEnabled": False,
    "oldPecConnected": True,
    "firebaseEnabled": False,
    "ativado": True,
    "treinamento": True,
    "isPrescricaoDigitalEnabled": False,
    "rocksdbEnabled": True,
    "tipoInstalacao": "PRONTUARIO",
    "cadastroDomiciliarViaCdsEnabled": False,
    "anexoArquivosEnabled": True,
    "frontendLogLevel": "OFF",
    "__typename": "Info",
}

MOCK_FLAGS = [
    {
        "id": "36",
        "nome": "ULTIMOS_ACESSOS_ENABLED",
        "valor": True,
        "__typename": "FlagInfo",
    },
    {
        "id": "38",
        "nome": "M_CHAT_ENABLED",
        "valor": True,
        "__typename": "FlagInfo",
    },
    {
        "id": "40",
        "nome": "PROGRAMA_DIGNIDADE_MENSTRUAL_ENABLED",
        "valor": True,
        "__typename": "FlagInfo",
    },
]

MOCK_PEC_USERS = {
    "12345678901": {
        "password": "Senha1234!",
        "profissional": {
            "id": "7",
            "cpf": "12345678901",
            "cns": "898001160123456",
            "nome": "Profissional Demo",
            "nomeSocial": None,
            "conselhoClasse": {
                "id": "461",
                "sigla": "CRM",
                "descricao": "CONSELHO REGIONAL DE MEDICINA",
                "__typename": "ConselhoClasse",
            },
            "numeroConselhoClasse": "12345",
            "ufEmissoraConselhoClasse": {
                "id": "7",
                "nome": "DISTRITO FEDERAL",
                "sigla": "DF",
                "__typename": "UF",
            },
            "usuario": {
                "id": "7",
                "aceitouTermosUso": True,
                "aceitouTermoTeleinterconsulta": False,
                "forcarTrocaSenha": False,
                "visualizouNovidades": True,
                "mostrarPesquisaSatisfacao": False,
                "notificaNovidadesVersao": True,
                "hashId": "demo-user-hash",
                "__typename": "Usuario",
            },
            "acessos": [
                {
                    "id": "590",
                    "tipo": "LOTACAO",
                    "cbo": {
                        "id": "461",
                        "nome": "MEDICO DE FAMILIA E COMUNIDADE",
                        "cbo2002": "225142",
                        "actions": {
                            "cadastroDomiciliar": {
                                "enabled": True,
                                "hint": None,
                                "__typename": "Action",
                            },
                            "cadastroIndividual": {
                                "enabled": True,
                                "hint": None,
                                "__typename": "Action",
                            },
                            "atividadeColetiva": {
                                "enabled": True,
                                "hint": None,
                                "__typename": "Action",
                            },
                            "__typename": "CboActions",
                        },
                        "__typename": "Cbo",
                    },
                    "equipe": {
                        "id": "1",
                        "nome": "Equipe ESF 1",
                        "ine": "2561267370",
                        "__typename": "Equipe",
                    },
                    "unidadeSaude": {
                        "id": "1",
                        "nome": "UBS Demo Centro",
                        "cnes": "1234567",
                        "tipo": {
                            "id": "1",
                            "codigoMs": "01",
                            "__typename": "TipoUnidadeSaude",
                        },
                        "subtipo": None,
                        "tipoEstabelecimento": "UBS",
                        "isEstabelecimentoAtencaoPrimaria": True,
                        "__typename": "UnidadeSaude",
                    },
                    "__typename": "Lotacao",
                }
            ],
            "__typename": "Profissional",
        },
    }
}

MOCK_CITIZENS = [
    {
        "id": "1001",
        "cpf": "11122233344",
        "cns": "898001160000111",
        "nisPisPasep": None,
        "nome": "Maria Silva",
        "nomeSocial": None,
        "nomeTradicional": None,
        "dataNascimento": "1989-04-12",
        "dataAtualizado": "2026-05-01T10:00:00Z",
        "dataObito": None,
        "numeroDocumentoObito": None,
        "sexo": "FEMININO",
        "nomeMae": "Ana Silva",
        "nomePai": "Jose Silva",
        "telefoneResidencial": "6133334444",
        "telefoneCelular": "61999990001",
        "telefoneContato": "61988887777",
        "email": "maria.silva@example.test",
        "area": "01",
        "microArea": "001",
        "endereco": {
            "cep": "70000000",
            "uf": {"id": "7", "nome": "DISTRITO FEDERAL"},
            "municipio": {"id": "5300108", "nome": "BRASILIA"},
            "bairro": "CENTRO",
            "tipoLogradouro": {"id": "1", "nome": "RUA"},
            "logradouro": "RUA DAS FLORES",
            "numero": "100",
            "semNumero": False,
            "complemento": "CASA 2",
            "pontoReferencia": "PROXIMO A PRACA",
        },
        "localidadeExterior": None,
        "prontuario": {
            "id": "9001",
            "gestacoes": [],
            "preNatalAtivo": None,
            "puerpera": False,
        },
        "identidadeGeneroDbEnum": "CIS_FEMININO",
        "etnia": None,
        "racaCor": {"id": "1", "nome": "BRANCA", "racaCorDbEnum": "BRANCA"},
        "cbo": None,
        "escolaridade": {"id": "3", "nome": "ENSINO MEDIO COMPLETO"},
        "ativo": True,
        "localidadeNascimento": {
            "id": "5300108",
            "nome": "BRASILIA",
            "uf": {"id": "7", "sigla": "DF"},
        },
        "faleceu": False,
        "possuiAgendamento": False,
        "unificado": False,
        "unificacaoBase": False,
        "cidadaoVinculacaoEquipe": {
            "id": "2001",
            "tpCdsOrigem": "PEC",
            "utilizarCadastroIndividual": True,
            "unidadeSaude": {"id": "1", "nome": "UBS Demo Centro"},
            "equipe": {"id": "1", "nome": "Equipe ESF 1", "ine": "2561267370"},
        },
        "tipoSanguineo": "O_POSITIVO",
        "orientacaoSexualDbEnum": None,
        "estadoCivil": {"id": "2", "nome": "CASADA"},
        "paisExterior": None,
        "nacionalidade": {"id": "1", "nacionalidadeDbEnum": "BRASILEIRA"},
        "portariaNaturalizacao": None,
        "dataNaturalizacao": None,
        "paisNascimento": {"id": "76", "nome": "BRASIL"},
        "dataEntradaBrasil": None,
        "stCompartilhaProntuario": True,
        "periodoAusenciaList": [],
        "cidadaoAldeado": None,
        "isCidadaoAusente": False,
    },
    {
        "id": "1002",
        "cpf": "55566677788",
        "cns": "898001160000222",
        "nisPisPasep": None,
        "nome": "Joao Pereira",
        "nomeSocial": "Joao P.",
        "nomeTradicional": None,
        "dataNascimento": "1977-09-05",
        "dataAtualizado": "2026-04-28T15:30:00Z",
        "dataObito": None,
        "numeroDocumentoObito": None,
        "sexo": "MASCULINO",
        "nomeMae": "Clara Pereira",
        "nomePai": "Mario Pereira",
        "telefoneResidencial": None,
        "telefoneCelular": "61999990002",
        "telefoneContato": None,
        "email": "joao.pereira@example.test",
        "area": "02",
        "microArea": "004",
        "endereco": {
            "cep": "70123456",
            "uf": {"id": "7", "nome": "DISTRITO FEDERAL"},
            "municipio": {"id": "5300108", "nome": "BRASILIA"},
            "bairro": "SUL",
            "tipoLogradouro": {"id": "2", "nome": "AVENIDA"},
            "logradouro": "AVENIDA CENTRAL",
            "numero": "500",
            "semNumero": False,
            "complemento": "APTO 12",
            "pontoReferencia": "BLOCO B",
        },
        "localidadeExterior": None,
        "prontuario": {
            "id": "9002",
            "gestacoes": [],
            "preNatalAtivo": None,
            "puerpera": False,
        },
        "identidadeGeneroDbEnum": "CIS_MASCULINO",
        "etnia": None,
        "racaCor": {"id": "2", "nome": "PARDA", "racaCorDbEnum": "PARDA"},
        "cbo": None,
        "escolaridade": {"id": "4", "nome": "SUPERIOR COMPLETO"},
        "ativo": True,
        "localidadeNascimento": {
            "id": "5300108",
            "nome": "BRASILIA",
            "uf": {"id": "7", "sigla": "DF"},
        },
        "faleceu": False,
        "possuiAgendamento": True,
        "unificado": False,
        "unificacaoBase": False,
        "cidadaoVinculacaoEquipe": {
            "id": "2002",
            "tpCdsOrigem": "PEC",
            "utilizarCadastroIndividual": True,
            "unidadeSaude": {"id": "1", "nome": "UBS Demo Centro"},
            "equipe": {"id": "1", "nome": "Equipe ESF 1", "ine": "2561267370"},
        },
        "tipoSanguineo": "A_POSITIVO",
        "orientacaoSexualDbEnum": None,
        "estadoCivil": {"id": "1", "nome": "SOLTEIRO"},
        "paisExterior": None,
        "nacionalidade": {"id": "1", "nacionalidadeDbEnum": "BRASILEIRA"},
        "portariaNaturalizacao": None,
        "dataNaturalizacao": None,
        "paisNascimento": {"id": "76", "nome": "BRASIL"},
        "dataEntradaBrasil": None,
        "stCompartilhaProntuario": True,
        "periodoAusenciaList": [],
        "cidadaoAldeado": None,
        "isCidadaoAusente": False,
    },
]


def _now_millis() -> int:
    return int(datetime.now(tz=timezone.utc).timestamp() * 1000)


def _normalize_username(username: str) -> str:
    return "".join(char for char in username if char.isdigit())


def _session_snapshot(username: str, session_id: str) -> dict[str, Any]:
    profissional = deepcopy(MOCK_PEC_USERS[username]["profissional"])
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


def _find_citizen_by_id(cidadao_id: str | None) -> dict[str, Any] | None:
    if not cidadao_id:
        return None
    for citizen in MOCK_CITIZENS:
        if citizen["id"] == cidadao_id:
            return citizen
    return None


def _search_citizens(terms: list[str], mode: str) -> list[dict[str, Any]]:
    if not terms:
        return deepcopy(MOCK_CITIZENS)

    numeric_terms = [
        "".join(char for char in term if char.isdigit())
        for term in terms
        if any(char.isdigit() for char in term)
    ]
    matches: list[dict[str, Any]] = []
    for citizen in MOCK_CITIZENS:
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


@router.post("/graphql")
def pec_mock_graphql(
    operations: list[PecMockOperation] | PecMockOperation,
    response: Response,
    pec_mock_session: str | None = Cookie(default=None, alias=SESSION_COOKIE_NAME),
) -> list[dict[str, Any]]:
    """
    Lightweight GraphQL-like dispatcher for PEC e-SUS APS contract tests.
    """
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
            session_snapshot = _session_snapshot(username, session_id)
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
            citizens = _search_citizens(terms, mode="cpf")
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
            citizens = _search_citizens(terms, mode="name")
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
            citizens = _search_citizens(terms, mode="general")
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
            citizen = _find_citizen_by_id(str(variables.get("cidadaoId")))
            if not citizen:
                results.append({"data": {"cidadao": None}})
                continue
            include_contacts = bool(
                variables.get("fetchCidadaoVinculacaoEquipeAndTelefones", False)
            )
            results.append({"data": {"cidadao": _citizen_header(citizen, include_contacts)}})
            continue

        if operation_name == "BuscaDetailCidadao":
            citizen = _find_citizen_by_id(str(variables.get("id")))
            results.append(
                {
                    "data": {
                        "cidadao": _citizen_detail(citizen) if citizen else None,
                    }
                }
            )
            continue

        if operation_name == "Cidadao":
            citizen = _find_citizen_by_id(str(variables.get("id")))
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

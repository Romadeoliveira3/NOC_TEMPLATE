SESSION_COOKIE_NAME = "pec_mock_session"

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

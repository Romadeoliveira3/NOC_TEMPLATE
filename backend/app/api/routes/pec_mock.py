from fastapi import APIRouter, Cookie, Response

from app.services.pec_mock import (
    SESSION_COOKIE_NAME,
    process_pec_mock_operations,
)
from app.schemas.pec_mock import PecMockOperation

router = APIRouter(prefix="/pec/mock", tags=["pec-mock"])


@router.post("/graphql")
def pec_mock_graphql(
    operations: list[PecMockOperation] | PecMockOperation,
    response: Response,
    pec_mock_session: str | None = Cookie(default=None, alias=SESSION_COOKIE_NAME),
) -> list[dict]:
    """
    Lightweight GraphQL-like dispatcher for PEC e-SUS APS contract tests.
    """
    return process_pec_mock_operations(
        operations=operations,
        response=response,
        pec_mock_session=pec_mock_session,
    )

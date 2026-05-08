from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class PecMockOperation(BaseModel):
    operationName: str
    variables: dict[str, Any] = Field(default_factory=dict)
    query: str | None = None

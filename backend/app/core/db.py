from sqlmodel import Session, create_engine

from app.core.config import settings

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))


# make sure all SQLModel models are imported (app.models) before initializing DB
# otherwise, SQLModel might fail to initialize relationships properly
# for more details: https://github.com/fastapi/full-stack-fastapi-template/issues/28


def init_db(_session: Session) -> None:
    """Initialize application data.

    The template superuser seed was removed with the template auth routes.
    Keep this hook for future project-specific bootstrap data.
    """
    return None

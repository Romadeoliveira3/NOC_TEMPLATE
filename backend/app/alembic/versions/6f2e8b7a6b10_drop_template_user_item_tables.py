"""Drop template user and item tables

Revision ID: 6f2e8b7a6b10
Revises: fe56fa70289e
Create Date: 2026-05-07 00:00:00.000000

"""

from alembic import op


revision = "6f2e8b7a6b10"
down_revision = "fe56fa70289e"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute('DROP TABLE IF EXISTS item CASCADE')
    op.execute('DROP TABLE IF EXISTS "user" CASCADE')


def downgrade() -> None:
    # Template tables intentionally removed. Recreate them from older revisions
    # only by downgrading before this migration.
    pass

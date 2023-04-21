"""convert users to organizations

Revision ID: de0eebb699a0
Revises: c5965229defb
Create Date: 2023-04-21 15:28:57.262713

"""
import sqlalchemy as sa  # noqa: F401

from alembic import op

# revision identifiers, used by Alembic.
revision = "de0eebb699a0"
down_revision = "c5965229defb"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.rename_table("users", "organizations")


def downgrade() -> None:
    op.rename_table("organizations", "users")

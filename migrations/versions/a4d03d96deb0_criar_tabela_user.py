"""Criar tabela user

Revision ID: a4d03d96deb0
Revises: 7345ccfe942e
Create Date: 2025-02-07 18:41:12.203936

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "a4d03d96deb0"
down_revision = "7345ccfe942e"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "user",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("username", sa.String(80), unique=True, nullable=False),
        sa.Column("password_hash", sa.String(256), nullable=False),
    )


def downgrade():
    op.drop_table("user")

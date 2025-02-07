"""Recriar tabela user com tamanho correto para password_hash

Revision ID: 7345ccfe942e
Revises: 43c74097d663
Create Date: 2025-02-05 17:39:29.012692

"""

from alembic import op
import sqlalchemy as sa

# Revisão e identificadores de downgrade
revision = "nova_revision_id"
down_revision = "43c74097d663"
branch_labels = None
depends_on = None


def upgrade():
    # Recriar tabela user
    op.create_table(
        "user",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(length=80), nullable=False),
        sa.Column("password_hash", sa.String(length=256), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("username"),
    )


def downgrade():
    # Remover tabela user
    op.drop_table("user")

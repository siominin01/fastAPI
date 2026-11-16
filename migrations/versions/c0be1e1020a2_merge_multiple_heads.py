"""merge multiple heads

Revision ID: c0be1e1020a2
Revises: 7a985bb84fcc, aebd266eb90c
Create Date: 2026-11-11 20:37:53.668111

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c0be1e1020a2'
down_revision = ('7a985bb84fcc', 'aebd266eb90c')
branch_labels = None
depends_on = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass

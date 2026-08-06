"""initial migration

Revision ID: 0001_initial
Revises: None
Create Date: 2026-08-05 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa

revision = '0001_initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Initial migration placeholder for Phase 1 database setup.
    pass


def downgrade() -> None:
    pass

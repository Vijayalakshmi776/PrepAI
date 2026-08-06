"""A generic, single-database Alembic environment.

Revision ID: ${up_revision}
Revises: ${down_revision | none}
Create Date: ${create_date}
"""
from alembic import op
import sqlalchemy as sa

${imports if imports else ''}

# revision identifiers, used by Alembic.
revision = ${repr(up_revision)}
down_revision = ${repr(down_revision)}
branch_labels = ${repr(branch_labels)}
defines = ${repr(defines)}


def upgrade() -> None:
${upgrades if upgrades else '    pass'}


def downgrade() -> None:
${downgrades if downgrades else '    pass'}

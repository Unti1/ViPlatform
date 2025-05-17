"""add_new_fields_to_quiz

Revision ID: dd626e00bbd6
Revises: 4383e3378773
Create Date: 2025-05-15 23:42:03.651555

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dd626e00bbd6'
down_revision: Union[str, None] = '4383e3378773'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass

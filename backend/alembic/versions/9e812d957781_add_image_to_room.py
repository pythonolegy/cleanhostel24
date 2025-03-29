"""Add image to room

Revision ID: 9e812d957781
Revises: 7c28ec44a6b8
Create Date: 2025-03-29 14:31:19.327573

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9e812d957781'
down_revision: Union[str, None] = '7c28ec44a6b8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute("UPDATE rooms SET image = '' WHERE image IS null;")

    op.alter_column('rooms', 'price',
               existing_type=sa.DOUBLE_PRECISION(precision=53),
               nullable=True,
               existing_server_default=sa.text("'0'::double precision"))
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('rooms', 'price',
               existing_type=sa.DOUBLE_PRECISION(precision=53),
               nullable=False,
               existing_server_default=sa.text("'0'::double precision"))
    op.drop_column('rooms', 'image')
    # ### end Alembic commands ###

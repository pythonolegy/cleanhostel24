"""Add price column to Room

Revision ID: d49f30bb1263
Revises: 5a95b4af5cd5
Create Date: 2025-03-29 14:22:33.317181

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd49f30bb1263'
down_revision: Union[str, None] = '5a95b4af5cd5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('rooms', sa.Column('image', sa.String(), nullable=True))
    op.execute("UPDATE rooms SET image = 'asdasd' WHERE image IS null;")

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

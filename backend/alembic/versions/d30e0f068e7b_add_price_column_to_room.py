"""Add price column to Room

Revision ID: d30e0f068e7b
Revises: 
Create Date: 2025-03-29 13:26:19.705112

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd30e0f068e7b'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Добавление нового столбца 'price'
    op.add_column('rooms', sa.Column('price', sa.Integer(), nullable=True))

    # Устанавливаем значение по умолчанию для существующих записей
    op.execute("UPDATE rooms SET price = 0 WHERE price IS null;")

    # Если нужно, можно задать поле как не NULL с дефолтным значением
    op.alter_column('rooms', 'price', nullable=False, server_default='0')

def downgrade():
    # Удаление столбца 'price' при откате миграции
    op.drop_column('rooms', 'price')

"""add_chain_otrosi_table

Revision ID: xxxxxxxxxxxx
Revises: 6e24fe41d7cb
Create Date: 2024-xx-xx xx:xx:xx.xxxxxx

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'xxxxxxxxxxxx'
down_revision = '6e24fe41d7cb'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table('chain_otrosi',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('output_prompt_extractor', sa.JSON(), nullable=True),
        sa.Column('output_prompt_estandarizador', sa.JSON(), nullable=True),
        sa.Column('tokens_input', sa.Integer(), nullable=True),
        sa.Column('tokens_output', sa.Integer(), nullable=True),
        sa.Column('total_tokens', sa.Integer(), nullable=True),
        sa.Column('otrosi_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['otrosi_id'], ['otrosi.id_documento'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_chain_otrosi_id'), 'chain_otrosi', ['id'], unique=False)

def downgrade():
    op.drop_index(op.f('ix_chain_otrosi_id'), table_name='chain_otrosi')
    op.drop_table('chain_otrosi')

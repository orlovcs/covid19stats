"""empty message

Revision ID: d6f19db91f01
Revises: 
Create Date: 2020-05-18 18:46:41.754140

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd6f19db91f01'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('us_infections',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('combined_key', sa.String(), nullable=True),
    sa.Column('date', sa.String(), nullable=True),
    sa.Column('cases', sa.Integer(), nullable=True),
    sa.Column('country_region', sa.String(), nullable=True),
    sa.Column('province_state', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('us_infections')
    # ### end Alembic commands ###

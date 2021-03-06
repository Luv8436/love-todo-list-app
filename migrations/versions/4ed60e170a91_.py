"""empty message

Revision ID: 4ed60e170a91
Revises: d1b2caec7056
Create Date: 2020-07-21 08:30:01.063902

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4ed60e170a91'
down_revision = 'd1b2caec7056'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('todos', sa.Column('completed', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###
    op.execute('UPDATE todos SET completed=False WHERE completed is NULL;')
    op.alter_column('todos' , 'completed' , nullable=False)


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('todos', 'completed')
    # ### end Alembic commands ###

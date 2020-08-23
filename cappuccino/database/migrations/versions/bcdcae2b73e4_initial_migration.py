"""Initial migration.

Revision ID: bcdcae2b73e4
Revises: 
Create Date: 2020-03-02 01:21:17.719685

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'bcdcae2b73e4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('discord_id', sa.BigInteger(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('discriminator', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('discord_id')
    )
    op.create_table('user_profile_fields',
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('category', sa.String(), nullable=False),
    sa.Column('value', sa.String(), nullable=False),
    sa.Column('list_position', sa.Integer(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.discord_id'], ),
    sa.PrimaryKeyConstraint('user_id', 'category', 'value')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_profile_fields')
    op.drop_table('users')
    # ### end Alembic commands ###
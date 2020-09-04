"""Rename guild_members and user_profile_fields

Revision ID: 29987e15121d
Revises: 5ef8ed75d713
Create Date: 2020-09-04 18:06:48.418040

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = '29987e15121d'
down_revision = '5ef8ed75d713'
branch_labels = None
depends_on = None


def upgrade():
    op.rename_table('user_profile_fields', 'user_profiles')
    op.rename_table('guild_members', 'user_nicks')


def downgrade():
    op.rename_table('user_profiles', 'user_profile_fields')
    op.rename_table('user_nicks', 'guild_members')

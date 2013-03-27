"""Add enzyme info

Revision ID: 26259a28fa2e
Revises: None
Create Date: 2013-03-27 16:37:26.332804

"""

# revision identifiers, used by Alembic.
revision = '26259a28fa2e'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('movies', sa.Column('acodec', sa.String))
    op.add_column('movies', sa.Column('vcodec', sa.String))
    op.add_column('movies', sa.Column('vwidth', sa.Integer))
    op.add_column('tv_episodes', sa.Column('acodec', sa.String))
    op.add_column('tv_episodes', sa.Column('vcodec', sa.String))
    op.add_column('tv_episodes', sa.Column('vwidth', sa.Integer))


def downgrade():
    op.add_column('movies', sa.Column('acodec', sa.String))
    op.add_column('movies', sa.Column('vcodec', sa.String))
    op.add_column('movies', sa.Column('vwidth', sa.Integer))
    op.add_column('tv_episodes', sa.Column('acodec', sa.String))
    op.add_column('tv_episodes', sa.Column('vcodec', sa.String))
    op.add_column('tv_episodes', sa.Column('vwidth', sa.Integer))

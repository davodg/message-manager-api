from alembic import op
import sqlalchemy as sa


revision = '0001'
down_revision = None


def upgrade():
    op.execute("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";")


def downgrade():
    op.execute("DROP EXTENSION IF EXISTS \"uuid-ossp\";")

from alembic import op
import sqlalchemy as sa

revision = '0003'
down_revision = '0002'

def upgrade():
    op.create_table(
        'messages',
        sa.Column('id', sa.String(36), primary_key=True, server_default=sa.text("uuid_generate_v4()")),
        sa.Column('status', sa.String(20), nullable=False),
        sa.Column('text', sa.JSON, nullable=False),
        sa.Column('error', sa.Text, nullable=True),
        sa.Column('creation_date', sa.DateTime, server_default=sa.func.now(), nullable=False),
        sa.Column('update_date', sa.DateTime, server_default=None, nullable=True)
    )


def downgrade():
    op.drop_table('messages')

from alembic import op
import sqlalchemy as sa

revision = '0002'
down_revision = '0001'

def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.String(36), primary_key=True, server_default=sa.text("uuid_generate_v4()")),
        sa.Column('name', sa.String(70), nullable=False),
        sa.Column('email', sa.String(50), nullable=False),
        sa.Column('phone', sa.String(15), nullable=False),
        sa.Column('ageg', sa.Integer, nullable=False),
        sa.Column('creation_date', sa.DateTime, server_default=sa.func.now(), nullable=False),
        sa.Column('update_date', sa.DateTime, server_default=None, nullable=True)
    )


def downgrade():
    op.drop_table('users')

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic
revision = '764d7c4d8db2'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Paso 1: Agregar la columna permitiendo valores nulos temporalmente
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('role', sa.String(length=20), nullable=True))

    # Paso 2: Asignar 'usuario' a los registros existentes que no tengan un rol
    op.execute("UPDATE user SET role = 'usuario' WHERE role IS NULL")

    # Paso 3: Hacer la columna obligatoria (nullable=False)
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('role', nullable=False)

def downgrade():
    # Si hay que revertir la migración, eliminamos la columna
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('role')

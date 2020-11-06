from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
usuarios = Table('usuarios', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('username', String(length=200), nullable=False),
    Column('password_hash', String(length=128), nullable=False),
    Column('admin', Boolean, default=ColumnDefault(False)),
    Column('latchAccountId', String(length=200)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['usuarios'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['usuarios'].drop()

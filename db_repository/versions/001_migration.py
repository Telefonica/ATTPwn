from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
DataStore = Table('DataStore', post_meta,
    Column('IDData', Integer, primary_key=True, nullable=False),
    Column('IDWarrior', Integer, nullable=False),
    Column('User', String(length=100)),
    Column('IP', String(length=100)),
    Column('Password', String(length=100)),
    Column('NTLM', String(length=100)),
    Column('LM', String(length=100)),
    Column('Port', String(length=100)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['DataStore'].columns['Port'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['DataStore'].columns['Port'].drop()

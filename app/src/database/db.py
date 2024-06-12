from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.engine.reflection import Inspector
from sqlalchemy.schema import (
        DropConstraint,
        DropTable,
        MetaData,
        Table,
        ForeignKeyConstraint,
    )


from src.params.config import config
from .models.base import Base


url = f'postgresql+asyncpg://{config.dbuser}:{config.dbpassword}@{config.dbhost}:{config.dbport}/{config.dbname}'

engine = create_async_engine(
    url, 
    future=True,
    echo=False,
    pool_pre_ping=True
)

async_session = sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession
)


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session


def drop_everything(engine):
    con = engine.connect()
    trans = con.begin()
    inspector = Inspector.from_engine(engine)

    meta = MetaData()
    tables = []
    all_fkeys = []

    for table_name in inspector.get_table_names():
        fkeys = []

        for fkey in inspector.get_foreign_keys(table_name):
            if not fkey['name']:
                continue

            fkeys.append(ForeignKeyConstraint((), (), name=fkey['name']))

        tables.append(Table(table_name, meta, *fkeys))
        all_fkeys.extend(fkeys)

    for fkey in all_fkeys:
        con.execute(DropConstraint(fkey))

    for table in tables:
        con.execute(DropTable(table))

    trans.commit()


def db_create() -> None:
    if config.reset_db:
        sync_url = f'postgresql://{config.dbuser}:{config.dbpassword}@{config.dbhost}:{config.dbport}/{config.dbname}'
        sync_engine = create_engine(sync_url)
        drop_everything(sync_engine)
        Base.metadata.create_all(sync_engine)
        print('Database reseted')
    else:
        print('Database up-to-date')

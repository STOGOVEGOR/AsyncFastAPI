import os
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import sessionmaker, declarative_base, DeclarativeBase

# DATABASE_URL = "postgresql+asyncpg://pgadmin:pgadmin@127.0.0.1:5432/apitest"
DATABASE_URL = "postgresql+asyncpg://pgadmin:pgadmin@db:5432/apitest"
# DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


Base = declarative_base()
# class Base(AsyncAttrs, DeclarativeBase):
#     pass

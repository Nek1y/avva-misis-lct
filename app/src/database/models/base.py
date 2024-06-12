from sqlalchemy.orm import declarative_base, DeclarativeBase


class Base(DeclarativeBase):
    async def update(self, **kwargs):
        for key, val in kwargs.items():
            if hasattr(self, key) and val:
                setattr(self, key, val)

from typing import Any

from sqlalchemy.sql import expression
from sqlalchemy.types import DateTime
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.ext.declarative import as_declarative, declared_attr


class UtcNow(expression.FunctionElement):
    type = DateTime()


@compiles(UtcNow, 'postgresql')
def pg_utcnow(element, compiler, **kw):
    return "TIMEZONE('utc', CURRENT_TIMESTAMP)"


@as_declarative()
class Base:
    id: Any
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(self) -> str:
        return self.__name__.lower()

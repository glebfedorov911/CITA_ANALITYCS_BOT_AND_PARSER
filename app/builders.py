from .interfaces import QueryBuilderImpl

from config.models.parsinginformation import ParsingInformation 
from config.models.base import type_base

from sqlalchemy import select, Result 
from sqlalchemy.sql import Select
from sqlalchemy.sql.elements import ColumnElement
from sqlalchemy.ext.asyncio import AsyncSession

from typing import List, Self


class QueryBuilder(QueryBuilderImpl):
    def __init__(self, model: type_base):
        self.model = model
        self.query = self._set_query_to_start()

    def limit(self, value_limit: int) -> Self:
        self.query = self.query.limit(limit=value_limit)
        return self

    def order_by(self, columns: List[ColumnElement]) -> Self:
        self.query = self.query.order_by(*columns)
        return self

    def add_condition(self, column: ColumnElement, value: any) -> Self:
        self.query = self.query.where(column == value)
        return self

    async def execute(self, session: AsyncSession) -> List[type_base]:
        result: Result = await session.execute(self.query)
        self.query = self._set_query_to_start()
        return result.scalars().all()

    def _set_query_to_start(self) -> Select:
        query = select(self.model)
        return query

class ParsingInformationQueryBuilder(QueryBuilder):
    def __init__(self, model: ParsingInformation):
        super().__init__(model)
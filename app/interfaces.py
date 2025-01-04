from abc import abstractmethod, ABC

from pydantic import BaseModel

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.elements import ColumnElement

from config.models.base import type_base 
from .schemas import ParsingInformationCreate, ParsingInformationUpdate, FullCitaInformation

from typing import List, Optional, Self


class ModelRepositoryImpl(ABC):

    @abstractmethod
    async def get_all(self) -> List[type_base]:
        ...

    @abstractmethod
    async def get_by_id(self, id_value: int) -> List[type_base]:
        ...

    @abstractmethod
    async def create(self, info_for_create: BaseModel) -> Optional[type_base]:
        ...

    @abstractmethod
    async def delete(self, id_value: int) -> bool:
        ...

    @abstractmethod
    async def update(self, id_value: int, info_for_update: BaseModel) -> Optional[type_base]:
        ...

class ParsingInformationImpl(ModelRepositoryImpl):

    @abstractmethod
    async def get_by_full_cita_information(self, cita_info: FullCitaInformation) -> List[type_base]:
        ...

class QueryBuilderImpl(ABC):
    
    @abstractmethod
    def limit(self, value_limit: int) -> Self:
        ...

    @abstractmethod
    def order_by(self, columns: List[ColumnElement]) -> Self:
        ...

    @abstractmethod
    def add_condition(self, column: ColumnElement, value: any) -> Self:
        ...
        
    @abstractmethod
    async def execute(self, session: AsyncSession) -> List[type_base]:
        ...
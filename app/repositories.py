from config.database import db_helper, DataBaseHelper
from config.models.parsinginformation import ParsingInformation 

from sqlalchemy import select, Result 
from sqlalchemy.ext.asyncio import AsyncSession

from .interfaces import ParsingInformationImpl, QueryBuilderImpl
from .schemas import ParsingInformationCreate, ParsingInformationUpdate, FullCitaInformation
from .builders import ParsingInformationQueryBuilder
from .logs import logger

from typing import List, Self, Optional

import asyncio


class ParsingInformationRepository(ParsingInformationImpl):
    
    def __init__(self, db_helper: DataBaseHelper):
        self.model = ParsingInformation
        self.db_helper = db_helper
        self.query_builder: QueryBuilderImpl = ParsingInformationQueryBuilder(self.model)

    async def get_all(self) -> List[ParsingInformation]:
        async for session in self.db_helper.session():
            result = await self.query_builder.execute(session=session)
        return self.__check_result_to_empty(result=result)

    async def get_by_id(self, id_value: int)-> Optional[ParsingInformation]:
        async for session in self.db_helper.session():
            self.query_builder = self.query_builder.add_condition(self.model.id, id_value)
            result = await self.query_builder.execute(session=session)
        return result[0] if result else None

    async def get_by_full_cita_information(self, cita_info: FullCitaInformation)-> Optional[List[ParsingInformation]]:
        async for session in self.db_helper.session():
            self.query_builder = self.query_builder\
                .add_condition(self.model.region, cita_info.region)\
                .add_condition(self.model.service, cita_info.service)\
                .add_condition(self.model.office, cita_info.office)
            result = await self.query_builder.execute(session=session)
        return self.__check_result_to_empty(result=result)

    @staticmethod
    def __check_result_to_empty(result) -> Optional[List[ParsingInformation]]:
        return result if result else None

    async def create(self, info_for_create: ParsingInformationCreate) -> Optional[ParsingInformation]:
        try:
            return await self.__create_new_data(data=info_for_create)
        except Exception as e:
            self.__log_write_error(e)
            return None

    async def __create_new_data(self, data: ParsingInformationCreate) -> Optional[ParsingInformation]:
        async for session in self.db_helper.session():
            parsing_info = self.model(**data.dict())
            result = await self.__add_to_db(session=session, data=parsing_info)
        return result

    async def delete(self, id_value: int) -> None:
        try:
            return await self.__delete_all_references(id_value=id_value)
        except Exception as e:
            self.__log_write_error(e)
            return None

    async def __delete_all_references(self, id_value: int) -> None:
        async for session in self.db_helper.session():
            data = await self.get_by_id(id_value=id_value)
            await session.delete(data)
            await self.__commit_session(session=session)

    async def update(self, id_value: int, info_for_update: ParsingInformationUpdate) -> Optional[ParsingInformation]:
        try:
            return await self.__update_data(id_value=id_value, data_for_update=info_for_update)
        except Exception as e:
            self.__log_write_error(e)
            return None

    async def __update_data(self, id_value: int, data_for_update: ParsingInformation):
        async for session in self.db_helper.session():
            data = await self.get_by_id(id_value=id_value)
            update_data = self.__update_value_from_data(exist_data=data, data_for_update=data_for_update)
            result = await self.__add_to_db(session=session, data=update_data)
        return result

    def __update_value_from_data(self, exist_data: ParsingInformation, data_for_update: ParsingInformationUpdate) -> ParsingInformation:
            for key, value in data_for_update:
                if hasattr(data_for_update, key) and value:
                    setattr(exist_data, key, value)
            return exist_data

    async def __add_to_db(self, session: AsyncSession, data: ParsingInformation) -> Optional[ParsingInformation]:
        session.add(data)
        await self.__commit_session(session=session)
        return data

    @staticmethod
    async def __commit_session(session: AsyncSession):
        await session.commit()

    @staticmethod
    def __log_write_error(message):
        logger.error(message)
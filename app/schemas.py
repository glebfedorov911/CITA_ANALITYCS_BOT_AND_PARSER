from pydantic import BaseModel

from typing import Optional


class ParsingInformationCreate(BaseModel):
    name: Optional[str] = None
    region: str 
    office: str 
    service: str

class ParsingInformationUpdate(BaseModel):
    name: Optional[str] = None
    region: Optional[str] = None 
    office: Optional[str] = None 
    service: Optional[str] = None
    was_get: Optional[str] = None

class FullCitaInformation(BaseModel):
    region: str
    office: str
    service: str
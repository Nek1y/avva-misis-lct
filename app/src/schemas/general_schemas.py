from datetime import datetime

from pydantic import BaseModel


class GeneralPlantCreate(BaseModel):
    name: str
    image: str = ''
    plant_type: str = ''
    temperature: float
    humidity: float
    soil_type: str = ''
    soil_acidity_type: str = ''


class GeneralPlantGet(GeneralPlantCreate):
    id: int

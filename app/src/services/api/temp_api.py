from datetime import datetime

from fastapi import HTTPException, status

from src.services.api.default_api import DefaultAPI
from src.schemas.general_schemas import *


class TempAPI(DefaultAPI):
    def __init__(self, token: str):
       pass

    def check_token(self):
        pass

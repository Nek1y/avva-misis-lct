from abc import abstractstaticmethod

from src.services.api.default_api import DefaultAPI
from src.services.api.temp_api import TempAPI


class FabricAPIWrap():
    def __init__(self) -> None:
        pass

    @classmethod
    def create_api_wrap(cls, cond: str, **kwargs) -> DefaultAPI:
        market_api_wrap = cls._get_api_wrap(cond)
        new_api_wrap = market_api_wrap(**kwargs)
        return new_api_wrap

    @classmethod
    def _get_api_wrap(cls, cond: str) -> DefaultAPI:
        api_by_market_type = {
            'condition_for_temp_api': cls._create_temp_api
        }
        return api_by_market_type[cond]

    @classmethod
    def _create_temp_api(cls, token: str, client_id: int):
        new_api_wrap = TempAPI(token, client_id)
        return new_api_wrap

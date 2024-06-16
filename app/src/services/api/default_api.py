from abc import ABC, abstractmethod
import requests
from copy import copy
from datetime import datetime, timedelta
from fastapi import HTTPException, status


class DefaultAPI(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def check_token(self):
        pass

    # TODO написать свое исключение, чтобы обработать невалидность токена
    def requests_get(self, route: str, headers: dict, body: dict | None = None):
        req = requests.get(route, headers=headers, json=body)
        if req.status_code != 200:
            auth_params = [f'{key}={val}' for key, val in headers.items()]
            except_detail = ' or'.join(auth_params) + ' is invalid'

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=except_detail
            )

        return req

    def requests_post(self, route: str, headers: dict, body: dict | None = None):
        req = requests.post(route, headers=headers, json=body)
        if req.status_code != 200:
            auth_params = [f'{key}={val}' for key, val in headers.items()]
            except_detail = ' or'.join(auth_params) + ' is invalid'

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=except_detail
            )

        return req

    def requests_patch(self, route: str, headers: dict, body: dict | None = None):
        req = requests.patch(route, headers=headers, json=body)
        if req.status_code not in (200, 204, 409):
            auth_params = [f'{key}={val}' for key, val in headers.items()]
            except_detail = ' or'.join(auth_params) + ' is invalid'

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=except_detail
            )

        return req

    def requests_delete(self, route: str, headers: dict, body: dict | None = None):
        req = requests.delete(route, headers=headers, json=body)
        if req.status_code not in (200, 204, 409):
            auth_params = [f'{key}={val}' for key, val in headers.items()]
            except_detail = ' or'.join(auth_params) + ' is invalid'

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=except_detail
            )

        return req

    # TODO Вырезать если не понадобится
    def get_date_range(self, start_date: datetime, end_date: datetime, date_range: timedelta):
        date_delta = end_date - start_date
        n = date_delta.days // date_range.days

        temp_date = copy(start_date)
        date_list = [temp_date]
        for _ in range(n):
            temp_date += date_range
            date_list.append(temp_date)

        date_list.append(end_date)

        return date_list

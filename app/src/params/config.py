from pydantic_settings import BaseSettings


class Config(BaseSettings):
    dbuser: str
    dbpassword: str
    dbhost: str
    dbname: str
    dbport: str
    reset_db: bool

config = Config(_env_file='.env', _env_file_encoding='utf-8')

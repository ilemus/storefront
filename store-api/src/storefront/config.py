from pydantic import BaseModel, BaseSettings

class MySQLConnection(BaseModel):
    hostname: str = 'adminer'
    port: int = 8080
    username: str = 'webapp'
    password: str = 'test_wrong_password'
    database: str = 'storefront'


class Settings(BaseSettings):
    mysql: MySQLConnection = ()
    connect_to_database: int = 0

    class Config:
        env_nested_delimiter = '__'


settings = Settings()

from pydantic import BaseSettings
from dataclasses import dataclass

@dataclass
class MySQLConnection:
    hostname: str = 'adminer'
    port: int = 8080
    username: str = 'webapp'
    password: str = 'webbapp_secret_password'

mysql_conn = MySQLConnection()


class Settings(BaseSettings):
    mysql: MySQLConnection = mysql_conn
    connect_to_database: bool = False


settings = Settings()

from pydantic import BaseSettings


class Settings(BaseSettings):
    database_hostname: str
    database_name: str
    database_username: str
    database_password: str
    database_port: str
    secrect_key: str
    algorithm: str
    access_token_expire_minutes: int
    
    class Config: # this is to import reference or import environment variables from .env file in this project
        env_file = ".env"

settings = Settings()


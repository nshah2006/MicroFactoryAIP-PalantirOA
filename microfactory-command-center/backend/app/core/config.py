from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql+psycopg://postgres:postgres@localhost:5432/microfactory"
    backend_cors_origins: str = "http://localhost:3000"
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "qwen2.5:7b-instruct"

    class Config:
        env_file = "../.env"
        extra = "ignore"


settings = Settings()

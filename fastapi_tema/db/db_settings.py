"""File with settings and configs for the project"""
from envparse import Env

env = Env()

REAL_DATABASE_URL = env.str(
    "REAL_DATABASE_URL",
    default="postgresql+asyncpg://postgres_fastapi_tema_ilya:postgres_fastapi_tema_ilya@127.0.0.1:5432/postgres_fastapi_tema_ilya",
)  # connect string for the real database
APP_PORT = env.int("APP_PORT", default=8080)

SECRET_KEY: str = env.str("SECRET_KEY", default="secret_key")
ALGORITHM: str = env.str("ALGORITHM", default="HS256")
ACCESS_TOKEN_EXPIRE_MINUTES: int = env.int("ACCESS_TOKEN_EXPIRE_MINUTES", default=30)
# SENTRY_URL: str = env.str("SENTRY_URL")

# test envs
TEST_DATABASE_URL = env.str(
    "TEST_DATABASE_URL",
    default="postgresql+asyncpg://postgres_fastapi_tema_ilya_test:postgres_fastapi_tema_ilya_test@localhost:5433/postgres_fastapi_tema_ilya_test",
)  # connect string for the test database

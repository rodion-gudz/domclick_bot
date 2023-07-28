from typing import Optional

from pydantic import BaseModel, BaseSettings, PostgresDsn, RedisDsn, SecretStr


class BotConfig(BaseModel):
    token: SecretStr


class WebhookConfig(BaseModel):
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    path: str = "/webhook"
    set_at_startup: bool = False
    url: str = "https://example.com"
    secret: Optional[SecretStr] = None


class RedisConfig(BaseModel):
    host: str = "localhost"
    port: int = 6379
    db: int = 0
    password: Optional[str] = None

    @property
    def dsn(self) -> str:
        return RedisDsn.build(
            scheme="redis",
            password=self.password,
            host=self.host,
            port=f"{self.port}",
            path=f"/{self.db}",
        )


class PostgresConfig(BaseModel):
    host: str = "localhost"
    port: int = 5432
    user: str = "postgres"
    password: Optional[str] = None
    database: str = "postgres"

    echo: bool = False

    @property
    def dsn(self) -> str:
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            user=self.user,
            password=self.password,
            host=self.host,
            port=f"{self.port}",
            path=f"/{self.database}",
        )


class FluentConfig(BaseModel):
    root_locale: str = "ru"


class Config(BaseSettings):
    bot: BotConfig
    redis: RedisConfig
    postgres: PostgresConfig
    webhook: WebhookConfig = WebhookConfig()
    fluent: FluentConfig = FluentConfig()

    class Config:
        frozen = True

        env_file = ".env"
        env_nested_delimiter = "__"
        env_file_encoding = "utf-8"


if __name__ == "__main__":
    stub_config = Config(
        bot=BotConfig(
            token=SecretStr("1234567890:ABCDEF1234567890abcdef1234567890"),
        ),
        webhook=WebhookConfig(),
        redis=RedisConfig(),
        postgres=PostgresConfig(),
    ).dict()

    # Generate example.env file and prints it to stdout
    # After it needs to be transferred to .env and changed
    # Should be replaced in the future with something better
    # SRC: https://stackoverflow.com/a/6027615/10473182
    def flatten(d: dict, parent_key="", sep="__", depth: int = 0):
        items = []
        for k, v in d.items():
            new_key = parent_key + sep + k if parent_key else k
            new_key = new_key.upper()
            if isinstance(v, dict) and depth < 1:
                items.extend(
                    flatten(v, new_key, sep=sep, depth=depth + 1).items()
                )
            else:
                items.append((new_key, v))
        return dict(items)

    print("\n".join(f"{k}={v}" for k, v in flatten(stub_config).items()))

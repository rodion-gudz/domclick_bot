import logging

from app.web import app, config


def main() -> None:
    import uvicorn

    uvicorn.run(
        app,
        host=config.webhook.app_host,
        port=config.webhook.app_port,
        log_level="info",
    )


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
    )
    main()

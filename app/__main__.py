import logging

from app.bot import create_bot, create_dispatcher
from app.config_reader import Config


def main() -> None:
    config = Config()

    bot = create_bot(config)
    dp = create_dispatcher(config)

    dp.run_polling(
        bot,
        allowed_updates=dp.resolve_used_update_types(),
    )


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
    )
    main()

from pathlib import Path

from fluent_compiler.bundle import FluentBundle
from fluentogram import FluentTranslator

from app.config_reader import FluentConfig
from app.services.fluent.translator_hub import EscapedTranslatorHub


def generate_hub(config: FluentConfig) -> EscapedTranslatorHub:
    """
    Generate TranslatorHub instance with FluentTranslator instances
    Search for all .ftl files in `app/services/fluent/locales/`
    and generate FluentTranslator for each locale
    :param config: FluentConfig instance
    :return: TranslatorHub instance
    """
    locales_dir = Path(__file__).parent.joinpath("locales")
    locales = [locale.stem for locale in locales_dir.glob("*")]

    return EscapedTranslatorHub(
        locales_map={  # ("eo", "ru") and ("ru")
            locale: (locale, config.root_locale)
            if locale != config.root_locale
            else (locale,)
            for locale in locales
        },
        translators=[
            FluentTranslator(
                locale,
                translator=FluentBundle.from_files(
                    locale,
                    _get_ftl_files(locales_dir, locale),
                    use_isolating=False,
                ),
            )
            for locale in locales
        ],
        root_locale=config.root_locale,
        separator="-",
    )


def _get_ftl_files(locales_dir: Path, locale: str) -> list[Path]:
    """
    Get all .ftl files for specified locale
    :param locales_dir: Path to locales directory
    :param locale: Locale name
    :return: List of Path objects
    """
    return [
        locales_dir / locale / filename
        for filename in (locales_dir / locale).glob("*.ftl")
    ]

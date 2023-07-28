from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.config_reader import Config
from app.services.fluent import I18n
from app.services.fluent.translator_hub import EscapedTranslatorHub


class SetLang(CallbackData, prefix="lang"):
    lang: str


class Buttons:
    def __init__(
        self, i18n: I18n, config: Config, translator_hub: EscapedTranslatorHub
    ):
        self.i18n = i18n
        self.translators = translator_hub.translators
        self.translators.sort(  # Needed to make root locale first
            key=lambda t: t.locale != translator_hub.root_locale
        )

    def web_link(self) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()

        builder.button(
            text=self.i18n.button.web_link(),
            url="https://domclick.ru/ipoteka/programs/onlajn-zayavka.",
        ),

        return builder.as_markup()

    def lang(self):
        builder = InlineKeyboardBuilder()

        for translator in self.translators:
            builder.button(
                text=translator.get("lang"),
                callback_data=SetLang(lang=translator.locale),
            )

        return builder.adjust(1).as_markup()

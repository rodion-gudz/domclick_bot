from fluentogram import TranslatorHub

from app.services.fluent.i18n import I18n


class EscapedTranslatorHub(TranslatorHub):
    def get_translator_by_locale(self, locale: str) -> I18n:
        # Because of the stub, creation of class instance
        # is broken
        return I18n(
            translators=self.translators_map.get(locale)  # noqa
            or self.translators_map[self.root_locale],
            separator=self.separator,  # noqa
        )

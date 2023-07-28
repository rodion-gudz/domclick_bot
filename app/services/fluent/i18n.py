import html
from typing import TYPE_CHECKING

from fluentogram import TranslatorRunner

if TYPE_CHECKING:
    from fluent_stub import TranslatorRunner  # noqa


class I18n(TranslatorRunner):
    # Only for better naming
    def _get_translation(self, key, **kwargs):
        if kwargs.get("internal_do_not_escape"):
            if result := super()._get_translation(  # noqa: Replaced by stub
                key, **kwargs
            ):
                return result
            else:
                raise KeyError(key)

        result = super()._get_translation(  # noqa: Replaced by stub
            key,
            **{
                k: html.escape(v) if isinstance(v, str) else v
                for k, v in kwargs.items()
            },
        )
        if not result:
            raise KeyError(key)
        return result

from app.services.fluent import I18n


def duration(i18n: I18n, days: int) -> str:
    months, days = divmod(days, 30)

    if months == 0:
        return i18n.days(count=days)

    if days == 0:
        return i18n.months(count=months)

    return f"{i18n.months(count=months)} {i18n.days(count=days)}"

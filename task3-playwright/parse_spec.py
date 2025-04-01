from playwright.sync_api import Page
from typing import Dict


def get_specs(page: Page) -> Dict[str, str]:
    """Парсит характеристики товара с Rozetka."""
    item_characteristics = {}

    try:
        # Ожидаем загрузки основного блока (с таймаутом 30 сек)
        page.wait_for_selector(
            "//main[contains(@class, 'product-tabs__content')]",
            timeout=30000
        )

        # Ищем все блоки характеристик
        items = page.query_selector_all(
            "//main[contains(@class, 'product-tabs__content')]//*[contains(@class, 'item')]"
        )

        for item in items:
            try:
                # Название характеристики
                title_element = item.query_selector(".//*[contains(@class, 'label')]//span")
                title = title_element.inner_text() if title_element else None

                # Значение характеристики
                value_element = item.query_selector(".//*[contains(@class, 'value')]")
                value = value_element.inner_text() if value_element else None

                if title and value:
                    item_characteristics[title] = value

            except Exception:
                continue  # Пропускаем битые элементы

    except Exception as e:
        print(f"Ошибка при парсинге характеристик: {str(e)}")

    return item_characteristics

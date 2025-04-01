from playwright.sync_api import Page
from typing import Dict


def get_specs(page: Page) -> Dict[str, str]:
    item_characteristics = {}

    try:
        page.wait_for_selector(
            "//main[contains(@class, 'product-tabs__content')]",
            timeout=30000
        )

        items = page.query_selector_all(
            "//main[contains(@class, 'product-tabs__content')]//*[contains(@class, 'item')]"
        )

        for item in items:
            try:
                title_element = item.query_selector(".//*[contains(@class, 'label')]//span")
                title = title_element.inner_text() if title_element else None

                value_element = item.query_selector(".//*[contains(@class, 'value')]")
                value = value_element.inner_text() if value_element else None

                if title and value:
                    item_characteristics[title] = value

            except Exception:
                continue

    except Exception as e:
        print(f"error: {str(e)}")

    return item_characteristics

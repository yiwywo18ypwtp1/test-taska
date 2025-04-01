from playwright.sync_api import sync_playwright
import time
import random

from parse_details import get_details
from export import save_to_json, save_to_excel


# имитируем поведение человека
def human_delay():
    time.sleep(random.uniform(0.5, 2.0))


with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=False,
        channel="chrome",
        args=[
            "--disable-blink-features=AutomationControlled",
            "--start-maximized"
        ],
        slow_mo=500  # замедление действий (специально)
    )

    context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        viewport={"width": 1920, "height": 1080}
    )

    page = context.new_page()

    try:
        page.goto('https://rozetka.com.ua/', timeout=15000)
        human_delay()

        search = page.locator("input[name='search']")
        search.click(delay=100)
        human_delay()

        search.fill("Apple iPhone 15 128GB Black")
        human_delay()

        search.press("Enter", delay=100)
        human_delay()

        page.screenshot(path="result/images/search_result.png")



        page.wait_for_selector("div.goods-tile", timeout=5000)

        item = page.locator("div.goods-tile").first

        # кликаем по товару
        with page.expect_navigation():
            item.locator("a").first.click(delay=100)

        human_delay()

        page.screenshot(path="result/images/product_page.png")



        # получаем данные о товаре и принтим в консоль
        product_data = get_details(page)
        print(product_data)


        # експорт в xlsx
        save_to_excel(product_data)

        # експорт .json (для теста/себя)
        save_to_json(product_data)

    except Exception as e:
        print(f"error: {e}")
        page.screenshot(path="result/images/error_final.png")



    finally:
        browser.close()

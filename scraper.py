import asyncio
from playwright.async_api import Playwright, async_playwright
import json


async def scrape_data(page):
    scraped_elements = []
    items = await page.query_selector_all("div.ps-biblio-data")

    for item in items:
        scraped_element = {}
        labels = await item.query_selector_all(".ps-biblio-field--label")

        for label in labels:
            field_name = await label.inner_text()

            try:
                field_element = await label.query_selector("xpath=..")
                field_value_element = await field_element.query_selector(".ps-biblio-field--value")
                field_value = await field_value_element.inner_text()
                scraped_element[field_name] = field_value
            except:
                scraped_element[field_name] = None

        scraped_elements.append(scraped_element)

    return scraped_elements


async def run(playwright: Playwright) -> None:
    browser = await playwright.chromium.launch(headless=False)
    context = await browser.new_context()
    page = await context.new_page()

    await page.goto("https://patentscope.wipo.int/search/en/detail.jsf?docId=US368140439&_cid=P21-LK8IYP-07879-1")
    await page.wait_for_selector("div.ps-biblio-data")

    data = await scrape_data(page)

    # Save data to JSON file
    with open('patent.json', 'a+') as file:
        json.dump(data, file)

    print("Data saved to 'patent.json'")

    await context.close()
    await browser.close()


async def main() -> None:
    async with async_playwright() as playwright:
        await run(playwright)


asyncio.run(main())

import asyncio
from playwright.async_api import Playwright, async_playwright
import json


async def scrape_data(page):
    # Create an empty list to store the scraped data for each item
    scraped_elements = []
    
    # Find all the items with class 'ps-biblio-data'
    items = await page.query_selector_all("div.ps-biblio-data")

    for item in items:
        # Create an empty dictionary to store the scraped data for each item
        scraped_element = {}
        
        # Find all the labels with class 'ps-biblio-field--label' within the current item
        labels = await item.query_selector_all(".ps-biblio-field--label")

        for label in labels:
            # Get the field name by extracting the inner text of the label element
            field_name = await label.inner_text()

            try:
                # Try to find the parent element of the current label using XPath (.. means parent)
                field_element = await label.query_selector("xpath=..")
                
                # Within the parent element, find the element with class 'ps-biblio-field--value'
                field_value_element = await field_element.query_selector(".ps-biblio-field--value")
                
                # Get the field value by extracting the inner text of the value element
                field_value = await field_value_element.inner_text()
                
                # Add the field name and its corresponding value to the scraped_element dictionary
                scraped_element[field_name] = field_value
            except:
                # If any error occurs (e.g., element not found), set the field value to None
                scraped_element[field_name] = None

        # Add the scraped_element dictionary to the list of scraped_elements
        scraped_elements.append(scraped_element)

    # Return the list of dictionaries, each containing the scraped data for a single item
    return scraped_elements


async def run(playwright: Playwright) -> None:
    # Launch the Chromium browser in non-headless mode (headless=False)
    # I did this so you could see the progress going on in the browser
    browser = await playwright.chromium.launch(headless=False)
    
    # Create a new browser context
    context = await browser.new_context()
    
    # Create a new page within the context
    page = await context.new_page()

    # Navigate to the specified URL
    await page.goto("https://patentscope.wipo.int/search/en/detail.jsf?docId=US368140439&_cid=P21-LK8IYP-07879-1")
    
    # Wait for the div with class 'ps-biblio-data' to be loaded on the page
    await page.wait_for_selector("div.ps-biblio-data")

    # Scrape data from the page using the scrape_data function
    data = await scrape_data(page)

    # Save data to a JSON file named 'patent.json'
    with open('patent.json', 'a+') as file:
        json.dump(data, file)

    # Print a message indicating that data has been saved to the file
    print("Data saved to 'patent.json'")

    # Close the browser context and the browser
    await context.close()
    await browser.close()


async def main() -> None:
    # Use Playwright to asynchronously run the code in the run function
    async with async_playwright() as playwright:
        await run(playwright)


# Use asyncio to run the main function asynchronously
asyncio.run(main())

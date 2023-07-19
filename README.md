# Documentation for Playwright Web Scraper
Scraper designed to scrape the WIPO webpage. It will dynamicaly search for label classes and then find the correct value for that label. The scraper will combine those two terms into a dict and then send each dict to a list. That list then gets written to a json file.

The json file has been included for you to see what the putput should look like.

An exapmple url is 'https://patentscope.wipo.int/search/en/detail.jsf?docId=US368140439&_cid=P21-LK8IYP-07879-1'

## Setup
First, set up a virtual environment.

Create a folder called *playwrightscraping* in the virtual environment.

Clone the repository into the *playwrightscraping* folder.

Open the repo in your IDE of choice.

Once the repo is loaded in your IDE, navigate your terminal to the correct path of the *playwrightscraping* folder.

Once on the correct path download playright with - **pip install playwright**

Install Browser requirements - **playwright install**


## Implementation
After finishing the downloads you should be ready to run the scraper.

Very simple to run. Add the WIPO web page you want to scrape in the **await page.goto()** function and then run the code.

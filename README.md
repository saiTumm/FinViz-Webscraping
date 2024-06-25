**FinViz-Webscraping**

The purpose of this project is not to give financial advice but to see the sentiment toward various stocks based on headlines containing their ticker. This is done by web scraping using BS4 from the FINVIZ.com website.

Then, Vader sentiment analysis generates a score for each headline and aggregates. This score is ultimately displayed in a table format in Excel.


Future Goals:

- Incorporate Alpha Vantage API to track the stock price at both the start and end of the day
- Train an ML model with day-by-day data to simulate/project what the stock price will be in real-time after each headline.

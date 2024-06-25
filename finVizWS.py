import requests  # Library for making HTTP requests
from bs4 import BeautifulSoup  # Library for parsing HTML
import pandas as pd  # Library for data manipulation and saving to Excel

def get_finviz_news(ticker):
    # Construct the URL for the given ticker
    url = f'https://finviz.com/quote.ashx?t={ticker}&p=d'
    
    # Set headers to mimic a browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    # Request the page content from the URL
    response = requests.get(url, headers=headers)
    
    # Raise an exception if the request was unsuccessful
    response.raise_for_status()
    
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the table containing news headlines
    news_table = soup.find('table', class_='fullview-news-outer')
    
    # Initialize an empty list to store headlines
    headlines = []
    
    # Iterate over each row in the news table
    for row in news_table.findAll('tr'):
        # Extract the date/time text from the first <td> element
        date_time = row.td.text.strip()
        
        # Find the <a> element containing the headline
        headline_tag = row.a
        
        # Check if the <a> element exists
        if headline_tag:
            # Extract the headline text from the <a> element
            headline = headline_tag.text.strip()
            # Append the date/time and headline as a list to the headlines list
            headlines.append([date_time, headline])
    
    # Return the list of headlines
    return headlines

def save_to_excel(headlines, ticker):
    # Convert the list of headlines to a pandas DataFrame
    df = pd.DataFrame(headlines, columns=['DateTime', 'Headline'])
    
    # Save the DataFrame to an Excel file named after the ticker
    df.to_excel(f'{ticker}_headlines.xlsx', index=False)
    
    # Print a success message
    print(f'Successfully saved {ticker} headlines to Excel.')

if __name__ == "__main__":
    # Define the ticker symbol (change this to scrape a different stock)
    ticker = 'AAPL'
    
    # Call the function to scrape news headlines for the given ticker
    headlines = get_finviz_news(ticker)
    
    # Call the function to save the scraped headlines to an Excel file
    save_to_excel(headlines, ticker)

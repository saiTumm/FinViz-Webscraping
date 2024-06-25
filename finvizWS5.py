import requests  # Library for making HTTP requests
from bs4 import BeautifulSoup  # Library for parsing HTML
import pandas as pd  # Library for data manipulation and saving to Excel
import re  # Library for regular expression operations
from nltk.sentiment.vader import SentimentIntensityAnalyzer  # VADER sentiment analysis
import nltk

# Download the VADER lexicon
nltk.download('vader_lexicon')

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
            
            # Use regular expression to find text within parentheses
            source_match = re.search(r'\((.*?)\)$', headline)
            if source_match:
                source = source_match.group(1)
                # Remove the source part from the headline
                headline = re.sub(r'\s*\(.*?\)$', '', headline)
            else:
                source = "Unknown"
            
            # Append the date/time, headline, and source as a list to the headlines list
            headlines.append([date_time, headline, source])
    
    # Return the list of headlines
    return headlines

def analyze_sentiment(headlines):
    # Initialize the VADER sentiment intensity analyzer
    sid = SentimentIntensityAnalyzer()
    
    # Initialize variables to accumulate sentiment scores
    total_negative = 0
    total_neutral = 0
    total_positive = 0
    total_compound = 0
    
    # Add sentiment scores for each headline
    for headline in headlines:
        # Get VADER sentiment scores
        sentiment_scores = sid.polarity_scores(headline[1])
        negative = sentiment_scores['neg']
        neutral = sentiment_scores['neu']
        positive = sentiment_scores['pos']
        compound = sentiment_scores['compound']
        
        # Accumulate scores
        total_negative += negative
        total_neutral += neutral
        total_positive += positive
        total_compound += compound
        
        # Append the sentiment scores to the headline
        headline.extend([negative, neutral, positive, compound])
    
    # Calculate average scores
    num_headlines = len(headlines)
    avg_negative = total_negative / num_headlines
    avg_neutral = total_neutral / num_headlines
    avg_positive = total_positive / num_headlines
    avg_compound = total_compound / num_headlines
    
    # Return the headlines with sentiment scores and aggregate scores
    return headlines, avg_negative, avg_neutral, avg_positive, avg_compound

def save_to_excel(headlines, ticker, avg_negative, avg_neutral, avg_positive, avg_compound):
    # Convert the list of headlines to a pandas DataFrame
    df = pd.DataFrame(headlines, columns=['DateTime', 'Headline', 'Source', 'Negative', 'Neutral', 'Positive', 'Compound'])
    
    # Save the DataFrame to an Excel file named after the ticker
    df.to_excel(f'{ticker}_headlines.xlsx', index=False)
    
    # Print aggregate scores
    print(f'Aggregate Scores for {ticker}:')
    print(f'Negative: {avg_negative:.4f}')
    print(f'Neutral: {avg_neutral:.4f}')
    print(f'Positive: {avg_positive:.4f}')
    print(f'Compound: {avg_compound:.4f}')
    
    # Print a success message
    print(f'Successfully saved {ticker} headlines to Excel.')

if __name__ == "__main__":
    # Define the ticker symbol (change this to scrape a different stock)
    ticker = 'AAPL'
    
    # Call the function to scrape news headlines for the given ticker
    headlines = get_finviz_news(ticker)
    
    # Call the function to perform sentiment analysis on the headlines
    headlines, avg_negative, avg_neutral, avg_positive, avg_compound = analyze_sentiment(headlines)
    
    # Call the function to save the scraped headlines to an Excel file
    save_to_excel(headlines, ticker, avg_negative, avg_neutral, avg_positive, avg_compound)

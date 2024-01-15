import os
import time
import requests
import csv
from datetime import datetime, timedelta
import re


# XRapid API Key:
XRapidAPIKey = "XRapidAPIKey"

# Define your headers and API details here
twitter_api_url = "https://twitter-api45.p.rapidapi.com/search.php"
chatgpt_api_url = "https://chatgpt-chatgpt3-5-chatgpt4.p.rapidapi.com/v1/chat/completions"

twitter_headers = {
    "X-RapidAPI-Key": XRapidAPIKey,
    "X-RapidAPI-Host": "twitter-api45.p.rapidapi.com",
}
chatgpt_headers = {
    "content-type": "application/json",
    "X-RapidAPI-Key": XRapidAPIKey,
    "X-RapidAPI-Host": "chatgpt-chatgpt3-5-chatgpt4.p.rapidapi.com"
}


# Set parameters directly in the code
start_date_str = '2023-01-01'  # Start date for data fetching (YYYY-MM-DD)
end_date_str = '2024-01-01'    # End date for data fetching (YYYY-MM-DD)

search_word = 'iphone-15-pro-max'  # Keyword for search
not_containing_str = 'Lightroom'  # Terms to exclude from search
min_faves = '10'  # Minimum number of likes
num_pages = 50  # Number of pages to fetch


# Check if not_containing_str is not empty and doesn't consist solely of spaces
if not_containing_str.strip():
    # Assign not_containing with the formatted string only if the condition is true
    not_containing = f'-{not_containing_str.strip()}'
else:
    not_containing = not_containing_str


# Function to create a date range
def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days) + 1):
        yield start_date + timedelta(n)


def parse_date(created_at_str):
    if created_at_str:  # Check if the created_at_str is not None
        tweet_date = datetime.strptime(created_at_str, '%a %b %d %H:%M:%S %z %Y')
        date = tweet_date.strftime('%d/%m/%Y')  # Includes date only
        time = tweet_date.strftime('%H:%M:%S')  # Extract time in hh:mm:ss format
        year, month, day_of_week = tweet_date.year, tweet_date.strftime('%B'), tweet_date.strftime('%A')
        day = tweet_date.day  # Extract day of the month
        return date, year, month, day, day_of_week, time
    else:
        # Return None or some default values if created_at is None
        return None, None, None, None, None, None


def extract_data(tweet, query, keyword):
    user_info = tweet.get('user_info', {})
    created_at = tweet.get('created_at', '')
    date, year, month, day, day_of_week, time = parse_date(created_at)

    if not all([date, year, month, day, day_of_week, time]):  # Check if any date parts are None
        print(f"Skipping tweet due to missing date information: {tweet.get('tweet_id', '')}")
        return None  # Return None to indicate this tweet should be skipped

    data_dict = {
        'keyword': keyword,
        'date': date,
        'tweet_id': tweet.get('tweet_id', ''),
        'screen_name': user_info.get('screen_name', ''),
        'name': user_info.get('name', ''),
        'text': tweet.get('text', ''),
        'created_at': tweet.get('created_at', ''),
        'year': year,
        'month': month,
        'day': day,
        'day_of_week': day_of_week,
        'time': time,
        'lang': tweet.get('lang', ''),
        'views': tweet.get('views', ''),
        'favorites': tweet.get('favorites', ''),
        'bookmarks': tweet.get('bookmarks', ''),
        'quotes': tweet.get('quotes', ''),
        'replies': tweet.get('replies', ''),
        'retweets': tweet.get('retweets', ''),
        'followers_count': user_info.get('followers_count', ''),
        'friends_count': user_info.get('friends_count', ''),
        'favourites_count': user_info.get('favourites_count', ''),
        'verified': user_info.get('verified', '')}
    return data_dict


# Function to get the sentiments, criticisms and praising using GPT:
def get_sentiment_analysis(tweets, keyword):
    cleaned_tweets_with_ids = []
    for tweet in tweets:
        # Splitting the tweet into its components (ID and text)
        parts = tweet.split(" | ")
        if len(parts) > 1:
            tweet_id_part, text_part = parts[0], parts[1]
            # Extracting the ID and the text
            tweet_id = tweet_id_part.replace("tweetid: ", "").strip()
            text = clean_tweet_text(text_part.replace("text: ", ""))
            # Combining the tweet ID and cleaned text
            cleaned_tweet_with_id = f"tweetid: {tweet_id} | text: {text}"
            cleaned_tweets_with_ids.append(cleaned_tweet_with_id)
    # Joining the cleaned tweets with IDs into a single string for analysis
    content = ' || '.join(cleaned_tweets_with_ids)
    print(content)
    # Construct the messages part of the payload with all tweets.
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {
                "role": "system",
                "content": f'You will receive a number of texts from various twitter ids. for each tweetid, your task is to find out where there is a reference to the word [{keyword}], and analyze the attitude toward it and to classify it. get probabilities from 0.00 to 1.00 for sentiments (the sum of all three probabilities of the three sentiments must equal to 1.00) and rating numbers from 0 to 100 for emotions for how much the text fit the category. also please mention as short as possible with 10 words maximum what is the criticism toward the keyword, and also what is good about the keyword (or praising toward the keyword). if there is no praising or criticism, simply write none. the output results must be only in the following format for example: INDEX: 1 || tweetid: id number | sentiments - negative: 0.25, positive: 0.55, neutral: 0.25 | emotions - anticipation: 83, happiness: 15, sadness: 22, anger: 50, fear: 67, disgust: 68, surprise: 32, contempt: 0, guilt: 21, shame: 80, curiosity: 2, pride: 8, sympathy: 100 | criticism: he must release the hostages | praising: it is great to have such a president INDEX: 2 || tweetid: id number |... there is no need to give any explanations for the classifications or the texts, just write the output format I mentioned. notice that if the texts contain emojis, so take them into consideration when classifying.',
            },
            {
                "role": "user",
                "content": content
            }
        ],
        "temperature": 0.5,  # higher value mean more diversity in the results
    }

    results = []
    max_retries = 3  # Maximum number of retries
    retry_count = 0  # Current retry attempt

    while retry_count <= max_retries:
        try:
            # Make the API call.
            response = requests.post(chatgpt_api_url, json=payload, headers=chatgpt_headers, timeout=120)
            print(response)
            if response.status_code == 200:
                data = response.json()
                results = data['choices'][0]['message']['content']
                break  # Successful response, exit the loop
            else:
                print(f"Failed to retrieve data: {response.status_code}")
                # You might want to handle specific status codes differently here
                retry_count += 1

        except (requests.exceptions.Timeout, requests.exceptions.RequestException) as e:
            print(f"Request for GPT timed out or failed.")
            print(f"Request failed: {e}")
            retry_count += 1  # Increment the retry counter

        if retry_count <= max_retries:
            print(f"Attempt {retry_count} of {max_retries}. Retrying in 30 seconds...")
            time.sleep(30)  # Wait for 30 seconds before retrying
        else:
            print("Max retries exceeded. No more attempts will be made.")
            break  # Exit the loop after reaching max retries

    return results


# Clean tweet from hashtags, links...
def clean_tweet_text(text):
    if text is None:  # Check if the text is None
        return ''  # Return an empty string if text is None
    text = re.sub(r'#\w+', '', text)  # Remove hashtags
    text = re.sub(r'https?:\/\/\S+', '', text)  # Remove links
    text = text.replace('\n', ' ')  # Replace newlines with spaces
    return text.strip()


# Parse data output from GPT:
def parse_sentiment_data(sentiment_data):
    tweets_data = [data for data in sentiment_data.split("INDEX:") if data.strip()]
    sentiment_info = {}
    for tweet_data in tweets_data:
        try:
            tweet_id_match = re.search(r'tweetid: (\d+)', tweet_data)
            if not tweet_id_match:
                print(f"Tweet ID not found in data: {tweet_data}")
                continue
            tweet_id = tweet_id_match.group(1)

            sentiments_match = re.search(
                r'sentiments - (negative: [0-1]\.\d+, positive: [0-1]\.\d+, neutral: [0-1]\.\d+)', tweet_data)
            if sentiments_match:
                sentiments_str = sentiments_match.group(1)
                sentiments = dict(item.split(": ") for item in sentiments_str.split(", "))
            else:
                print(f"Sentiments not found or malformed in data: {tweet_data}")
                continue

            emotions_match = re.search(
                r'emotions - (anticipation: \d+, happiness: \d+, sadness: \d+, anger: \d+, fear: \d+, disgust: \d+, surprise: \d+, contempt: \d+, guilt: \d+, shame: \d+, curiosity: \d+, pride: \d+, sympathy: \d+)',
                tweet_data)
            if emotions_match:
                emotions_str = emotions_match.group(1)
                emotions = dict(item.split(": ") for item in emotions_str.split(", "))
            else:
                print(f"Emotions not found or malformed in data: {tweet_data}")
                continue

            # Extracting criticism and praising
            criticism_match = re.search(r'criticism: (none|[^\|]+)', tweet_data)
            criticism = criticism_match.group(1).strip() if criticism_match and criticism_match.group(
                1).lower() != 'none' else ''

            praising_match = re.search(r'praising: (none|[^\|]+)', tweet_data)
            praising = praising_match.group(1).strip() if praising_match and praising_match.group(
                1).lower() != 'none' else ''

            sentiment_info[tweet_id] = {**sentiments, **emotions, 'criticism': criticism, 'praising': praising}
        except Exception as e:
            print(f"Error parsing tweet data: {e}. Data: {tweet_data}")

    return sentiment_info


# Add or append row data to the dataframe:
def append_to_csv(tweets, sentiments, search_word, filename):
    # Updated to include search word in the file name
    keyword_filename = search_word + '_' + filename
    filepath = os.path.join(keyword_filename)
    existing_tweet_ids = set()
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            existing_tweet_ids = {row['tweet_id'] for row in reader}

    # Extend fields to include emotional values
    emotion_fields = [
        'negative', 'positive', 'neutral', 'anticipation', 'happiness', 'sadness', 'anger', 'fear',
        'disgust', 'surprise', 'contempt', 'guilt', 'shame', 'curiosity', 'pride', 'sympathy'
    ]

    # Fields for the CSV file
    fields = [
                 'keyword', 'tweet_id', 'screen_name', 'name', 'text', 'bookmarks', 'favorites',
                 'created_at', 'year', 'month', 'day', 'day_of_week', 'time', 'date', 'lang', 'views', 'quotes',
                 'replies',
                 'retweets', 'followers_count', 'friends_count', 'favourites_count', 'verified',
                 'criticism', 'praising'
             ] + emotion_fields

    with open(filepath, 'a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        if file.tell() == 0:
            writer.writeheader()
        for tweet in tweets:
            if tweet['tweet_id'] not in existing_tweet_ids:  # Check for duplicates
                # Merge tweet data with its corresponding sentiment data
                tweet_with_sentiment = {**tweet, **sentiments.get(tweet['tweet_id'], {})}
                writer.writerow(tweet_with_sentiment)
                existing_tweet_ids.add(tweet['tweet_id'])


def update_with_sentiment(tweets, sentiments):
    for tweet in tweets:
        tweet_id = tweet.get('tweet_id', '')
        if tweet_id in sentiments:
            tweet.update(sentiments[tweet_id])
    return tweets


# Get data for the date range:
def get_data_for_date(date, search_keyword, num_pages, min_faves, not_containing, page_counter_signal, formatted_date, formatted_end_date):
    formatted_date = date.strftime("%Y-%m-%d")
    formatted_end_date = (date + timedelta(days=1)).strftime("%Y-%m-%d")

    max_retries = 3  # Maximum number of retries
    retry_count = 0  # Current retry attempt

    next_cursor = None  # Reset the cursor for each keyword
    page_counter = 0  # Initialize the page counter for each keyword

    while page_counter < num_pages:
        querystring = {
            "query": f"since:{formatted_date} until:{formatted_end_date} min_faves:{min_faves} lang:en ({search_keyword}) {not_containing} -128GB -256GB -512GB -1TB",
            "cursor": next_cursor, "search_type": "Latest"
        }

        print(f"Processing Date: {formatted_date} to {formatted_end_date}, Page: {page_counter} for keyword: {search_keyword}")

        try:
            response = requests.get(twitter_api_url, headers=twitter_headers, params=querystring, timeout=60)
            if response.status_code == 200:
                data_comp = response.json()
                #print('data_comp:', data_comp)
                data = data_comp['timeline']
                print('data:', data)

                #print('data:', data)

                # Extract tweet data here before sentiment analysis
                tweet_data = [extract_data(tweet, querystring["query"], search_keyword) for tweet in data]
                tweet_data = [t for t in tweet_data if t is not None]  # Filter out None values

                next_cursor = data_comp.get('next_cursor', None)
                tweets_for_analysis = [{"tweet_id": tweet["tweet_id"], "text": tweet["text"]} for tweet in data
                                       if tweet.get("tweet_id") and tweet.get("text")]
                tweet_texts = [f"tweetid: {tweet['tweet_id']} | text: {clean_tweet_text(tweet['text'])}" for
                               tweet in tweets_for_analysis]

                sentiment_results = get_sentiment_analysis(tweet_texts, search_keyword)
                print('sentiment_results:', sentiment_results)
                parsed_sentiments = parse_sentiment_data(sentiment_results)
                print('parsed_sentiments:', parsed_sentiments)
                updated_tweets = update_with_sentiment(tweet_data, parsed_sentiments)
                print('updated_tweets:', updated_tweets)
                append_to_csv(updated_tweets, parsed_sentiments, search_keyword, 'twitter_fetch.csv')

                page_counter += 1  # Increment the page counter
                retry_count = 0

                if not next_cursor or page_counter >= num_pages:  # Check if maximum pages reached or no more data
                    break
            else:
                print(f"Failed to retrieve data: {response.status_code}")
                raise Exception("Non-200 status code received")

        except (requests.exceptions.Timeout, requests.exceptions.RequestException) as e:
            print(f"Request for {formatted_date} to {formatted_end_date} timed out.")
            retry_count += 1
            print(f"Request failed: {e}")
            if retry_count <= max_retries:
                print(f"Attempt {retry_count} of {max_retries}. Retrying in 30 seconds...")
                time.sleep(30)  # Wait for 30 seconds before retrying
                continue  # Retry the request
            else:
                print("Max retries exceeded. Moving to the next page/date.")
                break  # Break out of the loop after reaching max retries

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            break  # Break out of the loop after reaching max retries

        print(f"Completed fetching data for {formatted_date} with keyword: {search_keyword}")
    return page_counter


if __name__ == '__main__':
    # Convert string dates to datetime objects
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

    # Main loop for data fetching
    for single_date in daterange(start_date, end_date):
        formatted_date = single_date.strftime("%Y-%m-%d")
        formatted_end_date = (single_date + timedelta(days=1)).strftime("%Y-%m-%d")

        # Call the main function to start fetching data
        get_data_for_date(single_date, search_word, num_pages, min_faves, not_containing,
                          lambda x: None, formatted_date, formatted_end_date)
        print(f"Completed fetching data for {formatted_date} with keyword: {search_word}")
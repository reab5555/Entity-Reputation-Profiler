# Entity Reputation Profiler
The purpose of this project is to extract a large number of tweets from the social network X that contain some keyword, and to create a profile of the criticsms and praisings, as well as emotions and sentiments toward that keyword for a predefined time period. this may be used for analyzing newley products, public figures, and organizations for marketing, PI, forensic, intelligence, or research purposes.

## Description
The tool is designed to create a reputation profile for a specific keyword by analyzing large amount of tweets that contain the keyword from the social network X. The keyword can be a certain product that has just been released, a public figure, an organization, or a name of a country.
First, the algorithm is designed to fetch, analyze, and store Twitter data related to a specific keyword within a specified date range. Using API calls, it retrieves or search for specific tweets that contain the keyword within a date period, filters them based on various parameters or queries like the number of favorites and exclusion terms, and uses sentiment analysis (using OpenAI GPT) to categorize emotions and attitudes towards the keyword. The analyzed data, along with detailed tweet information, is then saved into a dataframe for further use or analysis.
Secondly, it uses natural language processing to preprocess and cluster the criticisms and praisings summaries from the fetched dataframe, then employs a GPT-based model to analyze the clustered text for deeper insights, facilitating an understanding of the prominent themes in the criticism and praising categories.

## The Scripts
There are two separate scripts:
twitter_x_ext.py for extracting the tweets by keyword within a date period, as well as utilizing GPT for finding criticisms and praisings from the tweets, and twitter_x_cluster.py for reducing the criticisms and praisings into a meaningful list of insights by clustering and profiling major problems, issues, advantages, and other useful information for further improvements.

### Fetching: twitter_x_ext.py
1. Data Collection Setup: The script initializes with API keys and URLs for Twitter and GPT APIs, sets search parameters such as the keyword, date range, and filters for the tweets. start and end dates, the search word (keyword), the keyword to exclude, the minimum favorites for a tweet, and the number of pages to be fetched must be set manually. API service must be regestered beforehead trough Rapid API service, since it is the cheapest and fastest option for fetching the data.
2. Fetching Tweets: For each day in the specified date range, the script makes requests to the Twitter API to fetch tweets that match the search criteria.
3. Tweet Data Extraction and Cleaning: Extracts relevant information from each tweet (like user info, tweet content, date, etc.) and cleans the text by removing URLs, hashtags, and newlines.  
4. Sentiment Analysis: The cleaned tweets are then sent to the GPT API, which performs sentiment analysis. The analysis includes determining attitudes (positive, negative, neutral) towards the keyword and extracting specific criticisms or praises mentioned in the tweets.  
5. Parsing and Storing Results: The sentiment analysis results are parsed, combined with the original tweet data, and then saved into a CSV file. The script ensures that each tweet's information and its sentiment analysis are stored together.  
6. Execution: The main execution loop of the script runs these steps for each day in the date range, starting from the 'start date' to the 'end date', thus creating a comprehensive dataset of tweets related to the keyword with their corresponding sentiment analysis over the specified period.  

### Clustering: twitter_x_cluster.py
1. Preprocessing Text Data: After selecting the fetched data file, the script preprocesses the texts in the 'criticism' and 'praising' columns of the CSV file. It removes URLs, non-word characters, digits, and applies lemmatization to the words. It also excludes certain words based on stop words and filename variations.  
2. Text Clustering: The preprocessed text data is then clustered using the KMeans algorithm. The script identifies the main nouns, adjectives, and verbs in each cluster, focusing on the most significant words as determined by TF-IDF (Term Frequency-Inverse Document Frequency) scores.  
3. Removing Dominant Cluster Names: The script identifies and removes dominant cluster names which appear in more than half of the data entries, to avoid skewed analysis or misdetect the search word as a cluster.  
4. GPT-Based Cluster Analysis: The script uses the GPT model to analyze each cluster, seeking to summarize the relationship of the clustered texts with a specified cluster name.  
5. Parsing Data: The script exports the updated DataFrame, now including the cluster analysis results, back to a CSV file. It also generates a TXT file summarizing the clusters, listing each cluster name along with its frequency or count number. furthermore, it parses the TXT file to extract cluster data, which includes the cluster name, explanation, count, and type (Criticism or Praising). This data is then used to create a new DataFrame or a CSV file.  
6. Final Output: In summary, the script not only clusters the text data but also enriches it with detailed analysis, making it easier to understand key patterns and sentiments expressed in the text. The final output includes both CSV and TXT files, offering different formats for reviewing and utilizing the results of this comprehensive text analysis process.

## Examples:
### Product Analysis
Let's demonstrate the work of the algorithm as a way of analyzing and creating a profile for a product like the iPhone 15 Pro Max. First, we will extract tweets from the social network containing the keyword iPhone 15 Pro Max. The API uses a query, which means the keyword should be written in this way: 'iPhone-15-Pro-Max'. After that, we will specify the time range from which we would like to retrieve the tweets, for example, a start date of 2023-09-01 and an end date of 2024-01-01. In addition we would like to retrieve tweets with a minimum of 10 Favorites (likes) to limit our search to more popular tweets. We'll also want to specify which word we  want to exclude or don't want to appear in the tweets, for example we don't want the word 'Lightroom' to appear so that tweets talking about photo editing won't be extracted as it is not relevant for profiling criticisms and praisings. In this example we extracted a relatively small number of tweets for iPhone-15-Pro-Max (about 4400 tweets for the specified date period). Let's check the data we have extracted so far. We will load them into a graph referring to some of the features:




### Political Analysis


## Requirements:
* Make sure to create an account and set the X-Rapid API Key in config.py - https://rapidapi.com/hub.
* Make sure that all the latest required packages are installed from requirements.txt.
* In twitter_x_ext.py: start and end dates (start_date_str, end_date_str), the search word (search_word), the word to exclude (not_containing_str), the minimum favorites for a tweet (min_faves), and the number of pages (num_pages) to be fetched must be set manually.

```bash
git clone https://github.com/reab5555/Entity-Reputation-Profiler.git
cd Entity-Reputation-Profiler
pip install -r requirements.txt

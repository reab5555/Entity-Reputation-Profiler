# Entity Reputation Profiler
The purpose of the tool is to extract a large number of tweets from the social network X that contain some keyword, and to find the disadvantages and advantages of that keyword for a predefined time period (criticisms and praises).

## Description
This tool is designed to examine the reputation profile of a certain keyword by analyzing large amount of tweets from the social network X. The keyword can be a certain product that has just been released, a public figure, an organization, or a country.
First, the algorithm  is designed to fetch, analyze, and store Twitter data related to a specific keyword within a specified date range. It retrieves tweets, filters them based on various parameters or queries like the number of favorites and exclusion terms, and uses sentiment analysis (using OpenAI GPT) to categorize emotions and attitudes towards the keyword. The analyzed data, along with detailed tweet information, is then saved into a CSV file for further use or analysis.
Secondly, it utilize NLP clustering models in order to interpret texts related to criticisms and praisings.  It uses natural language processing to preprocess and cluster the criticisms and praisings summaries, then employs a GPT-based model to analyze the clustered text for deeper insights. The results, including the clusters and their analysis, are saved into a CSV file and a summary is written to a TXT file, facilitating an understanding of the prominent themes in the criticism and praising categories.

## The Script:
There are two separate scripts, one (twitter_x_ext.py) for extracting the tweets by keyword and date range, as well as utilizing GPT for finding criticisms and praisings from the tweets, and the second (twitter_x_cluster.py) for reducing the criticisms and praisings to a meaningful list of insights by clustering and reporting major problems, criticisms, praisings, and other insights for further improvements.

### The working steps of the algorithm
#### Fetching: twitter_x_ext.py
Fetching Tweets and their related Data + Getting Criticisms and Praisings:
Data Collection Setup: The script initializes with API keys and URLs for Twitter and ChatGPT APIs, sets search parameters such as the keyword, date range, and filters for the tweets.
Fetching Tweets: For each day in the specified date range, the script makes requests to the Twitter API to fetch tweets that match the search criteria, including filters like minimum favorites and exclusion of certain terms.
Tweet Data Extraction and Cleaning: Extracts relevant information from each tweet (like user info, text, date, etc.) and cleans the text by removing URLs, hashtags, and newlines.
Sentiment Analysis: The cleaned tweets are then sent to the ChatGPT API, which performs sentiment analysis. The analysis includes determining attitudes (positive, negative, neutral) towards the keyword and extracting specific criticisms or praises mentioned in the tweets.
Parsing and Storing Results: The sentiment analysis results are parsed, combined with the original tweet data, and then saved into a CSV file. The script ensures that each tweet's information and its sentiment analysis are stored together.
Iterative Data Processing: The script processes data day-by-day, iterating through the entire date range specified. For each day, it repeats the steps of fetching data, analyzing sentiment, and storing the results.
Error Handling and Retries: The script includes mechanisms for handling errors and retries, particularly when making API requests. This ensures that temporary issues like timeouts or request failures don't halt the entire data collection process.
Execution: The main execution loop of the script runs these steps for each day in the date range, starting from the 'start_date' to the 'end_date', thus creating a comprehensive dataset of tweets related to the keyword with their corresponding sentiment analysis over the specified period.

#### Clustering: twitter_x_cluster.py
This script performs text analysis and clustering on data from a CSV file, focusing on processing, clustering, and analyzing text in 'criticism' and 'praising' columns. The working steps are as follows:
Setup and File Selection: It initializes the environment, downloads necessary NLTK resources, and uses a Tkinter file dialog for the user to select a CSV file.
Preprocessing Text Data: The script preprocesses text in the 'criticism' and 'praising' columns of the CSV file. It removes URLs, non-word characters, digits, and applies lemmatization to the words. It also excludes certain words based on stop words and filename variations.
Text Clustering: The preprocessed text data is then clustered using the KMeans algorithm. The script identifies the main nouns, adjectives, and verbs in each cluster, focusing on the most significant words as determined by TF-IDF (Term Frequency-Inverse Document Frequency) scores.
Storing Clustered Data: The script saves the clustering results, including key nouns and verbs/adjectives for each cluster, back into a new CSV file.
Removing Dominant Cluster Names: The script identifies and removes dominant cluster names which appear in more than half of the data entries, to avoid skewed analysis.
GPT-Based Cluster Analysis: The script uses the GPT model to analyze each cluster, seeking to summarize the relationship of the clustered texts with a specified keyword.
Progress Tracking and Error Handling: The script uses a progress bar to track the cluster analysis process and includes error handling, particularly for the GPT API calls.
Results Integration and Cleanup: The analyzed cluster data is integrated back into the DataFrame. The script replaces empty cells with NaN, then
fills NaN values with empty strings. It also removes preprocessed columns which are no longer needed.
Exporting Final Results: The script exports the updated DataFrame, now including the cluster analysis results, back to a CSV file. It also generates a TXT file summarizing the clusters, listing each cluster name along with its frequency.
Parsing and Reformatting Data: The script parses the TXT file to extract cluster data, which includes the cluster name, explanation, count, and type (Criticism or Praising). This data is then used to create a new DataFrame.
Sorting and Saving Cluster Data: The DataFrame is sorted by the count of each cluster in descending order and saved as a final CSV file. This file represents a comprehensive summary of the cluster analysis, providing a clear and organized view of the most prominent themes in both criticism and praising categories within the original dataset.
Final Output: In summary, the script not only clusters the text data but also enriches it with detailed analysis, making it easier to understand key patterns and sentiments expressed in the text. The final output includes both CSV and TXT files, offering different formats for reviewing and utilizing the results of this comprehensive text analysis process.

## Requirements:


```bash
git clone https://github.com/reab5555/Entity-Reputation-Profiler.git
cd Entity-Reputation-Profiler
pip install -r requirements.txt

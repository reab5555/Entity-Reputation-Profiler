
<p align="center">
  <img src="assets/profiler_icon.png" alt="Alt text for image1" width="150"/>
</p>

# Entity Reputation Profiler
The purpose of this project is to extract a large number of tweets from the social network X that contain some keyword, and to create a profile of the criticsms and praisings, as well as emotions and sentiments toward that keyword for a predefined time period. this may be used for analyzing newley products, public figures, and organizations for marketing, PI, forensic, intelligence, or research purposes.

## Description
The tool is designed to create a reputation profile for a specific keyword by analyzing large amount of tweets that contain the keyword from the social network X. The keyword can be a certain product that has just been released, a public figure, an organization, or a name of a country.
First, the algorithm is designed to fetch, analyze, and store Twitter data related to a specific keyword within a specified date range. Using API calls, it retrieves or search for specific tweets that contain the keyword within a date period, filters them based on various parameters or queries like the number of favorites and exclusion terms, and uses sentiment analysis (using OpenAI GPT) to categorize emotions and attitudes towards the keyword. The analyzed data, along with detailed tweet information, is then saved into a dataframe for further use or analysis.
Secondly, it uses natural language processing to preprocess and cluster the criticisms and praisings summaries from the fetched dataframe, then employs a GPT-based model to analyze the clustered text for deeper insights, facilitating an understanding of the prominent themes in the criticism and praising categories. Technically, the main innovation here is the use of large language models instead of previously common methods such as the Zero-Shot Classification. These models give us a level of accuracy that is unmatched by the 'old' models, as well as a natural language processing that understands small nuances in the texts, and identifies broad patterns and meanings.

## The Scripts
There are two separate scripts:
twitter_x_ext.py for extracting the tweets by keyword within a date period, as well as utilizing GPT for finding criticisms and praisings from the tweets, and twitter_x_cluster.py for reducing the criticisms and praisings into a meaningful list of insights by clustering and profiling major problems, issues, advantages, and other useful information for further improvements. The reason for splitting the scripts is because we want one to be independent of the other. For example, it takes a long time to export a large amount of tweets, and we don't want that if there is a certain problem or error, the proccess will be interrupted. Therefore, using the second script only when we have a Dataframe file ready with all the data of the tweets only then we will want to run the second script to cluster the complete set of data.

### Dimensions or Features
The following is a complete list of dimensions or features of the extracted data, fit into the output dataframe:    
keyword, tweet_id, screen_name, name, text, bookmarks, favorites, created_at, year, month, day, day_of_week, time, date, lang, views, quotes, replies, retweets, followers_count, friends_count, favourites_count, verified, criticism, praising, negative, positive, neutral, anticipation, happiness, sadness, anger, fear, disgust, surprise, contempt, guilt, shame, curiosity, pride, sympathy.   

We chose the categories for classification after calculating correlations between the different emotions to check that there are no emotions with a correlation that is too high, so as not to get results for too similar dimensions. Emotions with too similar correlations of 0.85 or higher were removed from the list. Furthermore, the list of emotions is arbitrary, and any other suitable emotion can be added to the list, provided of course that it does not have a high correlation with another emotion already on the list.   
   
In addition, we tested correlations between the feelings or sentiments and dimensions such as the amount of views, the amount of likes, the amount of followers, the amount of shares, etc., but we received correlations that are not strong at all. For example, negative sentiment has a significant correlation of ***0.100 to the amount of reactions for tweets.

### Fetching: twitter_x_ext.py
1. Data Collection Setup: The script initializes with API keys and URLs for Twitter and GPT APIs, sets search parameters such as the keyword, date range, and filters for the tweets. start and end dates, the search word (keyword), the keyword to exclude, the minimum favorites for a tweet, and the number of pages to be fetched must be set manually. API service must be registered beforehead trough Rapid API service, since it is the cheapest and fastest option for fetching the data. for receiving and API key please register at https://rapidapi.com/hub.
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

## Requirements:
* Make sure to create an account and register for an API key, and set it in config.py - https://rapidapi.com/hub.  
* Make sure that all the latest required packages are installed from requirements.txt.
* In twitter_x_ext.py: start and end dates (start_date_str, end_date_str), the search word (search_word), the word to exclude (not_containing_str), the minimum favorites for a tweet (min_faves), and the number of pages (num_pages) to be fetched must be set manually.

## Examples:
### Product Analysis - Example 1
Let's demonstrate the work of the tool through analyzing and creating a profile for a product like the iPhone 15 Pro Max. First, we will extract tweets containing the keyword iPhone 15 Pro Max. The API uses queries, which means the keyword should be written in this way: 'iPhone-15-Pro-Max'. After that, we will specify the time period from which we would like to retrieve the tweets, for example, a start date of 2023-09-01 and an end date of 2024-01-01. In addition we would like to retrieve tweets with a minimum of 10 Favorites (likes) to limit our search to more popular tweets. We also want to specify which word we want to exclude or don't want to appear in the tweets, for example we don't want the word 'Lightroom' to appear so that tweets talking about photo editing won't be extracted as it is not relevant for profiling criticisms and praisings - we want tweets that talk about the device itself. In this example we extracted a relatively small number of tweets for iPhone-15-Pro-Max (about 4400 tweets for the specified date period). Let's check the data we have extracted so far. We will load them into a graph referring to some of the features:

<p align="center">
  <img src="assets/iphone-15-pro-max_twitter_fetch - Negative vs Neutral vs Positive.png" alt="Alt text for image1" width="800"/>
</p>

In this example, we can see the graph X-Axis with the dates, and the Y-Axis with the mean probability numbers of the Sentiments Negative, Neutral, and Positive (their sum is 1). the mean Sentiments across all dates are 0.16 for Negative, 0.4 for Neutral, and 0.43 for Positive - this indicate that the tweets for this date period are mostly positive toward iPhone 15 Pro Max for the dates between September 2023 to December 2023. now, the green spline line represent Positive sentiment, the red Negative, and the dark-grey Neutral sentiment. notice the release date vertical line in 22/09/2023. we can see a slight increase in positve sentiment in the release date, and a slight decline the day after, and a peak in 26/12/2023. notice that tweets that talk about products will mostly be positive, so we need to examine the slope and the increase and decrease of each line per date. Overall, we see a stable positivity toward the iPhone 15 Pro Max acros this date period, and a slight decrease of negativity since the product release date with some increase in 02/12/2023 with a peak value at the 19/12/2023. In order to understand why there is a sharp decrease or increase, it is recommended to use search engines to understand what event occurred on these dates.

<p align="center">
  <img src="assets/iphone-15-pro-max_twitter_fetch - Emotions.png" alt="Alt text for image1" width="800"/>
</p>

In this graph, we see the plotting of four different emotions (anticipation, curiosity, anger, and happiness). emotions are rated from 0 to 100. A notable peak in 'anticipation' is observed around the date labeled as iPhone 15 Release Date, which coincides with what one would expect around a product launch. The 'happiness' line also shows a peak around this date, suggesting positive reception. In contrast, 'anger' shows relatively lower levels throughout, with some small peaks that do not coincide with the release date. 'Curiosity' exhibits peaks both before and after the release date, suggesting that interest spikes occurred at multiple points, possibly due to announcements or other related news events. Overall, the graph suggests that anticipation and happiness were the dominant emotions expressed in relation to the iPhone 15 Pro Max around its release, with anticipation being the strongest emotion on average. Curiosity had a moderate presence throughout, with peaks at various points, while anger was the least expressed emotion according to this analysis.

<p align="center">
  <img src="assets/iphone-15-pro-max_twitter_fetch - keys.png" alt="Alt text for image1" width="800"/>
</p>

This bar chart categorizes the tweets into clusters named by key terms, and it distinguishes between two types of sentiments: praise (in green) and criticism (in red), and combinations of both (brown). The horizontal axis represents the count of mentions for each cluster (how many tweets contain the cluster name). The "Great" cluster has the highest count with 442 mentions, which falls under the praising category. The "Camera" cluster is also frequently mentioned feature with 148 counts, also associated with praising sentiment, indicating that the camera is a well-regarded aspect. On the criticism side, the "Issue" cluster has the highest count with 89 mentions, suggesting that there are some concerns or problems frequently discussed. Clusters like "Overheating," "Color," and "Battery" are associated with criticism. 


<p align="center">
  <img src="assets/Screenshot 2024-01-17 194152.png" alt="Alt text for image1" width="850"/>
</p>


This examplary output report is a detailed profile or summary of the clusters and their criticisms related to the iPhone 15 Pro Max, categorized by specific aspects or features, each followed by a count of mentions.

### Example 2
We would like to examine the attitude towards Israel before and after the events of October 7th 2023. We extracted about 50,000 tweets containing the word 'Israel' in all possible languages for the date range from July to December 2023. Let's examine the following graph:

<p align="center">
  <img src="assets/israel_twitter_fetch - Graph Builder 2.png" alt="Alt text for image1" width="800"/>
</p>

The sentiments Negative, Neutral, and Positive are plotted over a period from June to December, with specific events marked on the timeline.   

Key observations from the graph:   
* The negative sentiment has the highest mean value (around 0.45) and also the highest IQR (0.75), indicating both a higher average presence and greater variability in negative sentiment over the period.    
* Positive sentiment has the lowest mean (approximately 0.18) and a small IQR (0.1), suggesting that positive sentiments are less variable and consistently lower.    
* Neutral sentiment has a mean of around 0.32 with an IQR of 0.4, showing moderate presence and variability.    
* Notable peaks in negative sentiment correspond with marked events, particularly around the "Airstrikes on Gaza" and "Israeli Invasion of Gaza", suggesting these events elicited strong negative reactions.    
* The "7th of October" marks a significant peak for negative sentiment from that point. The differences between the sentiments are significant, so there is a clear distinction between them. The positive decreases along with the neutral, while the negative increases and continues to increase as the invasion progresses.   
* The "Prisoners Exchange" event shows a peak in positive sentiment and a decrease in negative sentiment, suggesting a favorable reaction to this event.    
* The smoothed lines help to visualize the general sentiment trend over time, revealing the fluctuating public reaction to the events marked on the graph. The data suggests that the events had a significant impact on the sentiments expressed, with negative sentiment being more pronounced overall.    

<p align="center">
  <img src="assets/israel_twitter_fetch - Anger vs Sympathy.png" alt="Alt text for image1" width="800"/>
</p>

This graph is a time series analysis displaying two emotional sentiments, anger and sympathy toward 'Israel'.    

Key observations from the graph:    

* The highest peak for anger coincides with the "Airstrikes on Gaza", suggesting a strong negative emotional response to this event.    
* Sympathy also peaks at the "Airstrikes on Gaza", although it is significantly lower than anger, indicating that while there is a notable level of sympathy, the anger sentiment is more dominant.     
* The "Israeli Invasion of Gaza" marks an increase in both anger and sympathy, with anger being the higher of the two.    
* The "Prisoners Exchange" shows an increase in sympathy sentiment, while anger appears to decrease, suggesting a positive public response to this event.    
Overall, the graph depicts the fluctuating levels of anger and sympathy in response to the marked events, with anger generally showing higher intensity than sympathy throughout the observed period.

<p align="center">
  <img src="assets/israel_twitter_fetch - Shame vs Pride.png" alt="Alt text for image1" width="800"/>
</p>

The graph is a time series plot of two emotional sentiments, shame and pride, against a timeline that includes key events.    

Observations from the graph:    

* Peaks in the sentiment of shame toward 'Israel' are visible at several points, particularly spiking around the "Israeli Invasion of Gaza". This suggests that this event elicited a strong feeling of shame toward 'Israel' among the discourse captured in the data.   
* The sentiment of pride shows less fluctuation and remains lower in comparison to shame, as indicated by its lower mean value.    
* The "Airstrikes on Gaza" event shows a notable peak in shame with a corresponding increase in pride, but unmatched against shame.   

<p align="center">
  <img src="assets/israel_twitter_fetch - Retweets.png" alt="Alt text for image1" width="800"/>
</p>

The graph displays a time series of retweet counts, presumably from Twitter, over a period with specific events marked along the timeline. The blue line represents the number of retweets over time, with spikes indicating increased activity.    

Observations from the graph:    

* There are noticeable spikes in retweet activity corresponding with the "Airstrikes on Gaza" and the "Israeli Invasion of Gaza" events. This suggests these events generated a significant amount of attention and were widely discussed or shared on the platform.    
* The "Prisoners Exchange" event also aligns with a spike in retweet numbers, suggesting heightened public interest or approval, which prompted users to share the content more broadly.   
Overall, retweet activity fluctuates, with the most pronounced peaks corresponding to events that are likely of high public interest or concern, as indicated by the higher volume of retweets.
The graph is useful for understanding the relative scale of public engagement and the spread of information on social media in relation to specific events.

<p align="center">
  <img src="assets/israel_twitter_fetch_clustered - criticism keywords - by date - nouns.png" alt="Alt text for image1" width="800"/>
</p>
<p align="center">
  <img src="assets/israel_twitter_fetch_clustered - criticism keywords - negative - adjectives_verbs.png" alt="Alt text for image1" width="800"/>
</p>

The graphs provided display timelines with cluster names categorized under criticism, represented in two separate graphs, one for nouns and the other for adjectives and verbs in relation or toward 'Israel'. Each graph plots the occurrences of these words over a timeline, with specific dates marked along the bottom axis. The first image focuses on nouns such as "apartheid", "genocide", "terrorism", "occupation", and "refugee" for example. The occurrences of these words are indicated by the horizontal lines and the box plots suggest the duration of the discussion about these terms. The second image presents adjectives and verbs, including "killing", "illegal", "criticizing", and "propaganda" for example.   

Both graphs highlight the "7th of October" with a red vertical line, which signify a significant date in relation to the usage of these keywords.    

These graphs could be used to analyze patterns of discourse, identify the prevalence of certain criticism topics over time, and observe how specific events might influence the language used in public discussions or social media. The distribution of terms across the dates could provide insights into the focus and intensity of criticism related to the events mentioned.

<p align="center">
  <img src="assets/israel_twitter_fetch_clustered - praising keywords - sympathy - nouns.png" alt="Alt text for image1" width="800"/>
</p>

In this bars plots we can see different nouns in relation to 'Israel', and the level of sympathy toward each cluster name. here we can see that the cluster name 'hostage' have the highest sympathy level, in other words, the tweets that contain the word 'hostage' in relation to 'Israel' have the highest level of sympathy.

<p align="center">
  <img src="assets/israel_twitter_fetch - Positive by Language.png" alt="Alt text for image1" width="800"/>
</p>

The horizontal bar chart represents the mean positivity score of tweets across various languages, denoted by their two-letter language codes. The bars and their color indicate the level of positive sentiment in content for each language. A longer bar signifies a higher positivity mean, while a shorter bar indicates a lower positivity mean. The color of the bars likely represents the intensity of positivity.   

At the top of the chart, the "ko" and "hu" language code, which typically stands for Korean and Hungarian, has the longest bar, suggesting that content in this language had the highest average positivity score among the languages represented.    

This chart can be useful for understanding which language-speaking communities are expressing more positive sentiments in their content toward 'Israel', according to the data source analyzed.     


### Example 3
Now let's present an analysis of collected tweets containing the keyword 'נתניהו' in the Hebrew language. The collected tweets were all written in Hebrew, and they were collected from the beginning of September 2023 until the end of December 2023. The total number of tweets is approximately 27,800.

<p align="center">
  <img src="assets/netanyahu_twitter_data_with_sentiments_clustered - negative vs neutral vs positive.png" alt="Alt text for image1" width="800"/>
</p>
<p align="center">
  <img src="assets/netanyahu_twitter_data_with_sentiments_clustered - Contempt vs Sympathy vs Surprise.png" alt="Alt text for image1" width="800"/>
</p>

These are two graphs that plot sentiment analysis results over time related to specific events, drawn from Twitter data that mentions or is associated with 'נתניהו'. The first graph shows the sentiments of sympathy, contempt, and surprise, with sympathy shown in pink, contempt in purple, and surprise in yellow. The second graph plots negative, neutral, and positive sentiments over the same timeframe. The sentiments are represented in red, black, and green respectively.    

These graphs can provide insights into the public's emotional responses to Netanyahu's actions and related events. For instance, high peaks of negative sentiment and contempt may correlate with controversial events or statements, while peaks in positive sentiment or sympathy might align with events viewed favorably by the public. Peaks in surprise could indicate unexpected events or statements that caught the public's attention. notice the significant increase in contempt toward 'נתניהו' just few days after the Israeli Invasion of Gaza, and the slight increase in sympathy and with a decrease in contempt after the prisoners exchange.

<p align="center">
  <img src="assets/netanyahu_twitter_data_with_sentiments_clustered - keywords - by date - nouns.png" alt="Alt text for image1" width="800"/>
</p>
<p align="center">
  <img src="assets/netanyahu_twitter_data_with_sentiments_clustered - keywords - by date - adjectives_verbs.png" alt="Alt text for image1" width="800"/>
</p>

The first image shows a range of adjectives and verbs such as "questionable", "failing", "corrupt", and "terrorist". The second image focuses on nouns such as "decision", "disaster", "corruption", and "threat" (also positive attributes can be found). Both graphs highlight "7th of October" with a red vertical line. The concentration of the box plots in the area after October 7th depicts the average concentration of the cluster names in a much more dominant way during this period than before October 7th.



```bash
git clone https://github.com/reab5555/Entity-Reputation-Profiler.git
cd Entity-Reputation-Profiler
pip install -r requirements.txt

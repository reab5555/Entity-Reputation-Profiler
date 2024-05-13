
<p align="left">
  <img src="assets/profiler_icon.png" alt="Alt text for image1" width="150"/>
</p>

# Entity Reputation Profiler
This tool is designed to analyze the reputation and sentiment towards a specific entity (e.g., product, public figure, organization) by collecting and processing relevant tweets from the social network Twitter (X). The core functionality involves fetching tweets that mention the target entity within a specified date range, and then performing sentiment analysis on the remaining tweets.   
   
The sentiment analysis categorizes the tweets into positive (praises) and negative (criticisms) sentiments towards the target entity. Additionally, it identifies the emotions and attitudes expressed in the tweets.  
The tool then employs natural language processing techniques to preprocess and cluster the summaries of criticisms and praises extracted from the analyzed data. These clustered text segments are further analyzed using a language model (GPT) to gain deeper insights into the prominent themes and patterns within the criticism and praising categories.   
    
The ultimate goal is to provide a comprehensive reputation profile for the target entity, highlighting the sentiments, emotions, criticisms, and praises expressed in the social media conversations. This information can be valuable for various purposes, such as product improvements, marketing strategies, reputation management, or research and intelligence gathering.   
     
### Advantages
Firstly, the utilization of large language models instead of the previously common methods such as the Zero-Shot Classification (BERT) give us a level of classification accuracy that is unmatched by the 'old' models, as well as a natural language processing that understands small nuances in the texts, and identifies broad patterns and meanings. Secondly, it is worth to notice that if one directly ask ChatGPT about major problems about a newley released product for example - the results cannot be validated, nor we know it's output sources.   

A tool that extracts major advantages and disadvantages of a product for example from tweets for a predefined time period, as opposed to directly asking ChatGPT, offers several distinct benefits:   
* Real-Time User Feedback: Tweets often reflect real-time user experiences and opinions. This immediacy captures the current public sentiment about a product, which can be more up-to-date than a pre-trained model like ChatGPT.   
* Diversity of Opinions: Twitter hosts a wide range of users from different backgrounds, providing a diverse array of opinions. This diversity can offer a more comprehensive view of a product’s strengths and weaknesses compared to the potentially limited or generalized knowledge base of ChatGPT.   
* Specific Use-Case Scenarios: Users often tweet about specific scenarios in which they used the product. This specificity can give insights into how the product performs under various conditions, something that ChatGPT might not detail unless it has been trained on similar specific data.   
* Unprompted Reviews: Tweets about a product are usually unprompted and genuine, providing honest and unfiltered feedback. In contrast, ChatGPT's responses are based on its training data, which might not fully capture the nuances of spontaneous user opinions.   
* Trend Analysis: Analyzing tweets over time allows for the identification of changing trends in public opinion about a product. This dynamic perspective is something that a static database, like the one ChatGPT relies on, might not capture.   
* Identifying Influencer Opinions: Influencers and thought leaders often share their opinions on Twitter. Their views can significantly impact public perception, and analyzing their tweets can provide insights into influential opinions about a product.   
* Sentiment Analysis: Tools that analyze tweets can employ advanced sentiment analysis techniques to quantify public opinion, providing a more structured and measurable understanding of the advantages and disadvantages as perceived by users.   
* Competitive Analysis: By comparing tweets about similar products, one can gain insights into how a product stacks up against its competitors in real users views.   
* Problem Detection: Users often tweet about issues or problems they encounter with a product, providing early detection of potential flaws or areas for improvement.

### Disadvantages
* Quality and Reliability: Tweets can sometimes be misleading, incorrect, or based on incomplete information.
* Potential for Bias and Manipulation: Tweets can be subject to bias or manipulation, such as paid endorsements, targeted campaigns against a product, or tweets written by bots. This can distort the real picture of a product's strengths and weaknesses.
* Groupthink: Twitter can sometimes foster echo chambers, where only similar opinions are shared and amplified, leading to a biased view of a product’s reception.
    
<p align="center">
  <img src="assets/workflow.png" alt="Alt text for image1" width="600"/>
</p>
<p align="center">
  <img src="assets/workflow2.png" alt="Alt text for image1" width="600"/>
</p>
   
## Requirements:
* Make sure that all the latest required packages are installed from requirements.txt.
* In twitter_x_ext.py: start and end dates (start_date_str, end_date_str), the search word (search_word), the word to exclude (not_containing_str), the minimum favorites for a tweet (min_faves), and the number of pages (num_pages) to be fetched must be set manually.

## Examples:
### Example 1: 'iPhone 15 Pro Max'
<p align="center">
  <img src="assets/iphone-15-pro-max_twitter_fetch - Emotions.png" alt="Alt text for image1" width="800"/>
</p>
<p align="center">
  <img src="assets/Screenshot 2024-01-17 194152.png" alt="Alt text for image1" width="850"/>
</p>

<p align="center">
  <img src="assets/iphone-15-pro-max_twitter_fetch_clustered - problems_by_date.png" alt="Alt text for image1" width="850"/>
</p>
   
### Example 2: 'Israel'
We would like to examine the attitude towards Israel before and after the events of October 7th 2023. We extracted about 50,000 tweets containing the word 'Israel' in all possible languages for the date range from July to December 2023. Let's examine the following graph:

<p align="center">
  <img src="assets/israel_twitter_fetch - Graph Builder 2.png" alt="Alt text for image1" width="800"/>
</p>
   
<p align="center">
  <img src="assets/israel_twitter_fetch - Shame vs Pride.png" alt="Alt text for image1" width="800"/>
</p>
   
<p align="center">
  <img src="assets/israel_twitter_fetch - Retweets.png" alt="Alt text for image1" width="800"/>
</p>
   
<p align="center">
  <img src="assets/israel_twitter_fetch_clustered - criticism keywords - by date - nouns.png" alt="Alt text for image1" width="800"/>
</p>
<p align="center">
  <img src="assets/israel_twitter_fetch_clustered - criticism keywords - negative - adjectives_verbs.png" alt="Alt text for image1" width="800"/>
</p>
   
<p align="center">
  <img src="assets/israel_twitter_fetch_clustered - praising keywords - sympathy - nouns.png" alt="Alt text for image1" width="800"/>
</p>
   
<p align="center">
  <img src="assets/israel_twitter_fetch - Positive by Language.png" alt="Alt text for image1" width="800"/>
</p>
  
```bash
git clone https://github.com/reab5555/Entity-Reputation-Profiler.git
cd Entity-Reputation-Profiler
pip install -r requirements.txt

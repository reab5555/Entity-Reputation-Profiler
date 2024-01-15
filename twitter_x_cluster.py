import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer, ENGLISH_STOP_WORDS
from sklearn.cluster import KMeans
import re
import tkinter as tk
from tkinter import filedialog
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet as wn, stopwords
from nltk import pos_tag
import nltk
import requests
import time
from tqdm import tqdm
from config import chatgpt_api_url, chatgpt_headers

# Ensure nltk resources are downloaded
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')
nltk.download('wordnet')


# Specify the number of desired clusters:
n_clusters = 10
print('Number of Clusters:', n_clusters)


# Initialize tkinter and hide the root window
root = tk.Tk()
root.withdraw()

# File Selection and Naming
file_path = filedialog.askopenfilename(title="Select the CSV file", filetypes=[("CSV files", "*.csv")])
if not file_path:
    raise FileNotFoundError("No file selected.")

save_path = file_path.rsplit('.', 1)[0] + '_clustered.csv'


# Preprocessing function
def preprocess(text, lemmatizer, excluded_words):
    if not isinstance(text, str):
        return ''

    text = re.sub(r'http\S+', '', text).lower()  # Remove URLs and lowercase text
    text = re.sub(r'\W+', ' ', text)  # Remove non-words
    text = re.sub(r'\d+', '', text)  # Remove digits

    words = text.split()
    return ' '.join(
        [lemmatizer.lemmatize(word) for word in words if word.lower() not in excluded_words and len(word) > 3])


# Function to separate nouns, adjectives, and verbs
def separate_nouns_adj_verbs(text, lemmatizer):
    words = text.split()
    tagged_words = pos_tag(words)
    nouns = ' '.join(lemmatizer.lemmatize(word, pos='n') for word, tag in tagged_words if tag.startswith('NN'))
    adjectives_verbs = ' '.join(lemmatizer.lemmatize(word, pos='a') for word, tag in tagged_words if
                                tag.startswith('JJ') or tag.startswith('VB'))
    return nouns, adjectives_verbs


# Generate filename variations
filename_words = re.findall(r'\b\w+\b', file_path.split('/')[-1].split('.')[0].lower())
filename_variations = set(filename_words)
for word in filename_words:
    for syn in wn.synsets(word):
        for lemma in syn.lemmas():
            filename_variations.add(lemma.name().replace('_', ' ').lower())

# Read the CSV File
df = pd.read_csv(file_path)


# Apply preprocessing
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))
excluded_words = stop_words.union(filename_variations)

df['criticism_preprocessed'] = df['criticism'].apply(preprocess, args=(lemmatizer, excluded_words))
df['praising_preprocessed'] = df['praising'].apply(preprocess, args=(lemmatizer, excluded_words))


# Clustering and labeling
def cluster_and_label(column, n_clusters, lemmatizer):
    texts = df[column].tolist()
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(texts)

    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    kmeans.fit(X)
    labels = kmeans.labels_

    # Extract features for each cluster
    clustered_texts = [[] for _ in range(n_clusters)]
    for text, cluster_label in zip(texts, labels):
        clustered_texts[cluster_label].append(text)

    cluster_nouns = []
    cluster_adj_verbs = []
    for cluster in clustered_texts:
        cluster_nouns_combined = ' '.join([separate_nouns_adj_verbs(text, lemmatizer)[0] for text in cluster])
        cluster_adj_verbs_combined = ' '.join([separate_nouns_adj_verbs(text, lemmatizer)[1] for text in cluster])

        nouns_vectorizer = TfidfVectorizer(stop_words='english')
        adj_verbs_vectorizer = TfidfVectorizer(stop_words='english')

        # Check if there are nouns
        if cluster_nouns_combined.strip():
            try:
                nouns_tfidf = nouns_vectorizer.fit_transform([cluster_nouns_combined])
                top_noun = nouns_vectorizer.get_feature_names_out()[nouns_tfidf.toarray().argmax()]
                cluster_nouns.append(top_noun)
            except ValueError:  # Handle empty vocabulary case for nouns
                cluster_nouns.append("")

        else:
            cluster_nouns.append("")

        # Check if there are adjectives/verbs
        if cluster_adj_verbs_combined.strip():
            try:
                adj_verbs_tfidf = adj_verbs_vectorizer.fit_transform([cluster_adj_verbs_combined])
                top_adj_verb = adj_verbs_vectorizer.get_feature_names_out()[adj_verbs_tfidf.toarray().argmax()]
                cluster_adj_verbs.append(top_adj_verb)
            except ValueError:  # Handle empty vocabulary case for adjectives/verbs
                cluster_adj_verbs.append("")

        else:
            cluster_adj_verbs.append("")

    return labels, cluster_nouns, cluster_adj_verbs


# Cluster 'criticism' and 'praising' columns
criticism_labels, criticism_nouns, criticism_adj_verbs = cluster_and_label('criticism_preprocessed', n_clusters,
                                                                           lemmatizer)
praising_labels, praising_nouns, praising_adj_verbs = cluster_and_label('praising_preprocessed', n_clusters, lemmatizer)

# Create cluster name columns
df['criticism_cluster_nouns'] = [criticism_nouns[label] for label in criticism_labels]
df['criticism_cluster_adj_verbs'] = [criticism_adj_verbs[label] for label in criticism_labels]
df['praising_cluster_nouns'] = [praising_nouns[label] for label in praising_labels]
df['praising_cluster_adj_verbs'] = [praising_adj_verbs[label] for label in praising_labels]

# Save to CSV
df.to_csv(save_path, index=False)
print(f"Clustering completed. Results saved to: {save_path}")


# Define a function to remove dominant cluster names
def remove_dominant_cluster_names(df, columns):
    for column in columns:
        cluster_name_counts = df[column].value_counts()
        # Calculate 50 percent of the number of rows
        half_count = len(df) / 2
        # Get cluster names that should be removed
        dominant_cluster_names = cluster_name_counts[cluster_name_counts > half_count].index.tolist()
        # Replace dominant cluster names with an empty string
        df[column] = df[column].apply(lambda x: '' if x in dominant_cluster_names else x)

# Columns containing cluster names
cluster_columns = [
    'criticism_cluster_nouns',
    'criticism_cluster_adj_verbs',
    'praising_cluster_nouns',
    'praising_cluster_adj_verbs'
]

# Remove dominant cluster names from the specified columns
remove_dominant_cluster_names(df, cluster_columns)

# Get the keyword from the 'keyword' column (assuming it's in the first row)
keyword = df.loc[0, 'keyword']


# Function to analyze clusters using GPT:
def get_cluster_analysis(cluster_name, texts, keyword):
    keyword = keyword.capitalize()  # Capitalize the first letter of cluster_name
    cluster_name = cluster_name.capitalize()  # Capitalize the first letter of cluster_name
    # Construct the messages part of the payload with cluster_name, associated texts, and the keyword.
    payload = {
        "model": "gpt-3.5-turbo-16k",
        "messages": [
            {
                "role": "system",
                "content": f'For the word {cluster_name} - summarize and explain from the provided list of tweets summaries in what relation the word {cluster_name} is mentioned in relation and only toward or about {keyword}. summarize it as short as possible with one line, a limit of 50 words only and with two sentences maximum. furthermore, no need to mention all descriptions from the tweets summaries, only the top descriptions that best describe it so there is no need to repeat things that mean the same thing. the output must be written only in this format for example: {cluster_name}: relation summary or as in this example: Battery: significant battery errors, battery is draining fast. also, dont write or include a note or notes.',
            },
            {
                "role": "user",
                "content": f'Tweets summaries: {texts}'
            }
        ],
        "temperature": 1,
        "frequency_penalty": 1.5,
    }

    results = []
    max_retries = 2  # Maximum number of retries
    retry_count = 0  # Current retry attempt

    while retry_count <= max_retries:
        try:
            # Make the API call.
            response = requests.post(chatgpt_api_url, json=payload, headers=chatgpt_headers, timeout=120)
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
            print("Max retries exceeded. No more attempts will be made. this is possibly because of large amount of texts as an input. please try to increase the number of clusters.")
            return None  # Return None to indicate that the maximum retries were exceeded

    print(results)
    return results


# Function to calculate total unique clusters across specified columns
def total_unique_clusters(df, columns):
    unique_clusters = set()
    for column in columns:
        unique_clusters.update(df[column].unique())
    return unique_clusters

# Columns containing cluster names
cluster_columns = [
    'criticism_cluster_nouns',
    'praising_cluster_nouns',
    'criticism_cluster_adj_verbs',
    'praising_cluster_adj_verbs'
]

# Calculate the total number of unique clusters
total_clusters = total_unique_clusters(df, cluster_columns)


# Function to add cluster analysis results to the DataFrame with tqdm progress bar
def add_cluster_analysis_results(df, cluster_names_column, text_column, result_column, pbar):
    unique_cluster_names = df[cluster_names_column].unique()
    for cluster_name in unique_cluster_names:
        if cluster_name:  # Check if cluster_name is not empty
            cluster_texts = df[df[cluster_names_column] == cluster_name][text_column].tolist()

            # Call the modified get_cluster_analysis function with cluster_name, cluster_texts, and keyword
            analysis_result = get_cluster_analysis(cluster_name, cluster_texts, keyword)

            # If analysis_result is not None, add the result to the DataFrame
            if analysis_result is not None:
                df.loc[df[cluster_names_column] == cluster_name, result_column] = analysis_result
            else:
                print(f"Skipping cluster '{cluster_name}' due to exceeded retries.")

        pbar.update(1)


with tqdm(total=len(total_clusters), desc="Processing clusters") as pbar:
    add_cluster_analysis_results(df, 'criticism_cluster_nouns', 'criticism', 'criticism_cluster_nouns_exp', pbar)
    add_cluster_analysis_results(df, 'praising_cluster_nouns', 'praising', 'praising_cluster_nouns_exp', pbar)
    add_cluster_analysis_results(df, 'criticism_cluster_adj_verbs', 'criticism', 'criticism_cluster_adj_verbs_exp', pbar)
    add_cluster_analysis_results(df, 'praising_cluster_adj_verbs', 'praising', 'praising_cluster_adj_verbs_exp', pbar)


# Replace empty cells with NaN values
df = df.replace('', np.nan)
# Replace NaN values with an empty string or a specific placeholder before saving to CSV
df.fillna('', inplace=True)
# Drop the preprocessed columns since they are not relevant for the output
df = df.drop(['criticism_preprocessed', 'praising_preprocessed'], axis=1)

# Define the columns to extract cluster names from
exp_columns = ['criticism_cluster_nouns_exp', 'praising_cluster_nouns_exp',
               'criticism_cluster_adj_verbs_exp', 'praising_cluster_adj_verbs_exp']

# Replace 'nan' strings with an empty string in specified columns
for col in exp_columns:
    df[col] = df[col].apply(lambda x: '' if str(x).lower() == 'nan' else x)

# Save the updated DataFrame to CSV again
df.to_csv(save_path, index=False)
print(f"Cluster analysis results added to the DataFrame and saved to: {save_path}")

# Load the CSV file
df = pd.read_csv(save_path)

# Define the columns for criticism and praising
criticism_columns = ['criticism_cluster_nouns_exp', 'criticism_cluster_adj_verbs_exp']
praising_columns = ['praising_cluster_nouns_exp', 'praising_cluster_adj_verbs_exp']

# Extract cluster names for criticism and praising, including duplicates
criticism_cluster_names = []
praising_cluster_names = []

for col in criticism_columns:
    criticism_cluster_names.extend(df[col].dropna().tolist())

for col in praising_columns:
    praising_cluster_names.extend(df[col].dropna().tolist())

# Count the frequency of each cluster name in both categories
criticism_name_counts = pd.Series(criticism_cluster_names).value_counts()
praising_name_counts = pd.Series(praising_cluster_names).value_counts()

# Sort the cluster names by their frequency
sorted_criticism_names = criticism_name_counts.sort_values(ascending=False)
sorted_praising_names = praising_name_counts.sort_values(ascending=False)

# Create a TXT file and write the sorted lists
txt_file_path = save_path.rsplit('.', 1)[0] + '_clusters_summary.txt'
with open(txt_file_path, 'w', encoding='utf-8') as file:
    file.write(f'{keyword}:\n\n\n')
    file.write("Criticism:\n---------------------------------------------\n\n")
    for cluster_name, count in sorted_criticism_names.items():
        file.write(f"- {cluster_name}\nCount: {count}\n\n")

    file.write("\n\nPraising:\n---------------------------------------------\n\n")
    for cluster_name, count in sorted_praising_names.items():
        file.write(f"- {cluster_name}\nCount: {count}\n\n")

print(f"Cluster names list saved to: {txt_file_path}")


# Function to parse the TXT file and extract cluster data
def parse_txt_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Split the content into criticism and praising sections
    criticism_section, praising_section = content.split('Praising:\n---------------------------------------------\n\n', 1)

    # Function to extract cluster data from a section
    def extract_cluster_data(section, label):
        clusters = []
        # Find all cluster entries using regular expression
        cluster_entries = re.findall(r'- (.+?): (.+?)\nCount: (\d+)', section)
        for entry in cluster_entries:
            cluster_name, explanation, count = entry
            clusters.append({'Cluster Name': cluster_name, 'Explanation': explanation, 'Count': int(count), 'Type': label})
        return clusters

    # Extract clusters from both sections
    criticism_clusters = extract_cluster_data(criticism_section, 'Criticism')
    praising_clusters = extract_cluster_data(praising_section, 'Praising')

    # Combine both lists
    all_clusters = criticism_clusters + praising_clusters
    return all_clusters


# Parse the TXT file
cluster_data = parse_txt_file(txt_file_path)

# Create a DataFrame from the extracted data
df = pd.DataFrame(cluster_data)

# Sort the DataFrame by 'Count' in descending order
df = df.sort_values(by='Count', ascending=False)

# Save the DataFrame to a CSV file
csv_file_path = txt_file_path.rsplit('.', 1)[0] + '_clusters_exp.csv'
df.to_csv(csv_file_path, index=False)

print(f"Cluster data saved to: {csv_file_path}")
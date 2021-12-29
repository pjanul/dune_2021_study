# Dune (2021) Reception Analysis

Welcome to the project. Here are a few details to help familarize yourself with everything.

## Directory Structure

The project exists in the following folder structure:

```
├── dune_2021_study
    ├── readme.txt
    ├── project_main
        ├── scripts
            ├── clean_tweets.py
            ├── compute_tfidf.py
            ├── get_words.py
            ├── retrieve_tweets.py
        ├── data
            ├── tfidf_values
                ├── category_tfidf.json
                ├── sentiment_tfidf.json
                ├── combined_tfidf.json
            ├── word_counts
                ├── category_words.json
                ├── sentiment_words.json
                ├── combined_words.json
            ├── api_data.json
            ├── clean_annotated_tweets.csv
            ├── clean_tweets.csv
            ├── retrieval_windows.txt
```		

## Overview of Code

The code in this project can be be split into 3 categories: tweet collection/cleaning, TF-IDF calculation, and plotting. 
Below is an explanation/tutorial and a description of each script. 
When running the script in the command line, make sure to use the appropriate path to each file. 
The commands should run anywhere, but it is best if they are run in the "project_main" directory.



### Section 1: Tweet Collection and Cleaning:
#### Using `retrieve_tweets.py`
This script should be run in the command line as follows.
```
python3 retrieve_tweets.py -i <retrieval_window_file.txt> -o <output_file.json>
```
The retrieval window file should contain a list of dates. These dates form time intervals over which a maximum of 100 tweets are collected. 
If there are not 100 tweets over a given interval, all the tweets that can be collected will be. 
The results of the Twitter API calls will then be stored and written to the output JSON file.
The number of API calls is n-1, where n is the length of the retrieval list.
IMPORTANT: Anyone attempting to run this will require their own bearer token. 
For more information on aquiring a bearer token, see 'https://developer.twitter.com/en/docs/authentication/oauth-2-0/bearer-tokens'

#### Using `clean_tweets.py`
This script should be run in the command line as follows: 

```python3 clean_tweets.py -i <input_file.json> -o <output_file.csv>```

The input file here is the output produced by calling retrieve_tweets.py. The data is then processed into a CSV file containing 3 columns:
'tweet_id', 'created_at' (the date and time when the tweet was posted), and 'tweet' (the contents of the tweet). 
Additional columns for 'category', 'sentiment', and 'combined' are also created, but have no contents; they must be manually annotated.

### Section 2: TF-IDF Calculation:
#### Using `get_words.py`
This script should be run in the command line as follows:

```python3 get_words.py -i <input_file.csv> -o <output_file.json> -g <group_name>```

The input file is the result of clean_tweets.py. 
The tweets are then cleaned, and relevant words are stored along with their frequency in a JSON file 
(see report for more details as to how this is achieved). 
The -g flag indicates the group. This can be either 'category', 'sentiment', or 'combined', depending on what type of data we want.
Any other group name will produce an error message.
All three are collected for this project, as they will be plotted later.
		
#### Using `compute_tdidf.py`
This script should be run in the command line as follows:

```python3 compute_tfidf.py -i <input_file.json> -o <output_file.json> ```

The input file is the result of get_words.py, and should be run for all three groups. 
The top 10 highest TF-IDF scores per group are then calculated written to the output file.

## Commands Used to Run Code

The following commands were used to obtain and process the data. 
Some things to keep in mind when running these commands:
1. Anyone running this code will need to modify retrieve_tweets.py and use their own bearer token.
2. Default Twitter developer accounts can only retrieve tweets 7 days in the past. Unless you have Elevated Access, you will most likely need to update retrieval_windows.txt
to run the code. Otherwise, you will get an access error.
3. All commands appear are run in the ```project_main``` directory in the order in which they are called. 


```
	python3 ./scripts/retrieve_tweets.py -i ./data/retrieval_windows.txt -o api_data'.json 
	python3 ./scripts/clean_tweets.py -i ./data/output.json -o ./data/clean_tweets.csv
	python3 ./scripts/clean_tweets.py -i ./data/output.json -o ./data/clean_tweets.csv
```

```
	python3 ./scripts/get_words.py -i ./data/clean_annotated_tweets.csv -o ./data/word_counts/category_words.json -g category
	python3 ./scripts/get_words.py -i ./data/clean_annotated_tweets.csv -o ./data/word_counts/sentiment_words.json -g sentiment
	python3 ./scripts/get_words.py -i ./data/clean_annotated_tweets.csv -o ./data/word_counts/combined_words.json -g combined
```

```
	python3 ./scripts/compute_tfidf.py -i ./data/word_counts/category_words.json -o ./data/tfidf_values/category_tfidf.json
	python3 ./scripts/compute_tfidf.py -i ./data/word_counts/sentiment_words.json -o ./data/tfidf_values/sentiment_tfidf.json
	python3 ./scripts/compute_tfidf.py -i ./data/word_counts/combined_words.json -o ./data/tfidf_values/combined_tfidf.json
```

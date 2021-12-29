#!/usr/bin/env python3

import pandas as pd
import os, sys
import json
import datetime
import csv


# This function takes a single response and stores the relevant information in a list.
# The list has elements formatted as 'tweet ID + comma + time + comma + tweet content' 
def analyze_response(response):
    return_list = []
    response_data = response['data']
    #print(len(response_data)) # Useful to see how many tweets are in each section
    for tweet in response_data:
        tweet['text'] = tweet['text'].replace('\n', ' ')
        return_list.append([tweet['id'], tweet['created_at'], tweet['text']])
    return return_list 


# This function iterates through all responses and combines everything into a single list
# Once again, the list has elements formatted as 'tweet ID + tab + time + tab + tweet content' 
def get_tweet_data(all_responses):
    return_list = []
    for response in all_responses:
        
        return_list = return_list + analyze_response(response)
    return return_list
        
def send_to_df(tweet_list):
    df = pd.DataFrame(tweet_list, columns=['tweet_id', 'date', 'tweet'])
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values(by="date")
   
    return df

def main():
    # Open the messy API file and read it
    with open(sys.argv[2], "r", encoding="utf-8") as f_in:
        all_responses = json.loads(f_in.read())
    
    # Clean the data and store it in a list using the functions we defined above
    all_tweet_data = get_tweet_data(all_responses)
    
    df = send_to_df(all_tweet_data)
    df.drop_duplicates(subset ="tweet", keep = "first", inplace = True)
    
    # For each element in the list, write it as a line in a CSV file
    # Recall that each element has the format 'tweet ID + comma + time + comma + tweet content' 
    
    
    with open(sys.argv[4], "w", newline = '', encoding="utf-8") as f_out:

        writer = csv.writer(f_out)
        writer.writerow(['tweet_id', 'created_at', 'tweet', 'category', 'sentiment', 'combined'])
        df.to_csv(f_out, index=False,header=False)
        
    

    f_in.close()    
    f_out.close()

if __name__ == "__main__":
    main()

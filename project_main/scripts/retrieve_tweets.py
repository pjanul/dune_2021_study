#!/usr/bin/env python3

import pandas as pd
import requests
import os, sys
import json
from pathlib import Path
import time
from datetime import datetime



def connect_to_twitter(token):
        bearer_token = token
        return {"Authorization": "Bearer {}".format(bearer_token)}

# Make a request to the Twitter API and access tweets posted in the specified time interval
# We can only access 100 tweets at a time, so we need at least 10 intervals to get all the 
def make_request(headers, start_time, end_time):
    url = "https://api.twitter.com/2/tweets/search/recent"
    query_params = {
                  'query': 'dune movie lang:en -is:retweet',
                  'start_time': start_time,
                  'end_time': end_time,
                  'max_results': 100,
                  'tweet.fields': 'id,text,author_id,geo,created_at,lang', #'id,text,author_id,in_reply_to_user_id,geo,conversation_id,created_at,lang,public_metrics,referenced_tweets,reply_settings,source',
                  'next_token': {} 
                  # Potentially useful fields, but not required for this project
                  #'expansions': 'author_id,in_reply_to_user_id,geo.place_id',
                  #'user.fields': 'id,name,username,created_at,description,public_metrics,verified',
                  #'place.fields': 'full_name,id,country,country_code,geo,name,place_type',
                  } 
    return requests.request("GET", url, params=query_params,    headers=headers).json()


# Make one request for each time interval 
# CAUTION: Calling this function too frequently can exceed your rate limit
def get_all_requests(headers, time_interval_list):
    # Initialize a list to collect the API data.
    requests_list = []
    
    # Iterate through each time interval and make a request. Then, append to the API data list
    for i in range(len(time_interval_list)-1):
        start_time = time_interval_list[i]
        end_time = time_interval_list[i+1]
        requests_list.append(make_request(headers, start_time, end_time))
    return requests_list    


def main():
    
    # Two main things which may need to be altered manually:
    # 1) The bearer token: Replace this with your own token if necessary.
    # 2) The time intervals: Changing the time intervals can give us different data and different biases. 
    #                        Feel free to customize this (or update it to new intervals)if necessary
    
    # ====================================== Customize this if need be ================================================ #
    
    # Create the headers for the API request. 
    headers = connect_to_twitter("AAAAAAAAAAAAAAAAAAAAAJA2WwEAAAAAbUlKsSMoVshUYuq2HEkNhNP4jzs%3DjKhF6Ll6m6n19K5d4TZolri0uyxfcMLeFEUbjKznbzPjHwrTiQ")
    
    
    # Define appropriate time intervals. Each interval will collect exactly 100 tweets
    time_intervals = ['2021-12-04T00:00:00Z', '2021-12-04T06:00:00Z', '2021-12-04T12:00:00Z', '2021-12-04T18:00:00Z',
                  '2021-12-05T00:00:00Z', '2021-12-05T08:00:00Z', '2021-12-05T16:00:00Z',
                  '2021-12-06T00:00:00Z', '2021-12-06T08:00:00Z', '2021-12-06T18:00:00Z', 
                  '2021-12-07T00:00:00Z'] 

    # Only 2 intervals which decreases the number of requests we make; useful for testing purposes
    time_intervals_short = ['2021-12-04T00:00:00Z', '2021-12-05T06:00:00Z', '2021-12-06T12:00:00Z']
    
    # ================================================================================================================ #
    
    all_responses = get_all_requests(headers, time_intervals)
    

    # If the output path does not exist, create it. Then, open the file for writing
    output_file = sys.argv[2]
    output_dir = os.path.dirname(output_file)
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    f = open(output_file, "w")
    f.write(json.dumps(all_responses))
    f.close()
    
if __name__ == "__main__":
    main()

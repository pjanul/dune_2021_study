#!/usr/bin/env python3

import pandas as pd
import os, sys
import json
import csv
import math
import itertools 



# Compute the Total Frequency (TF) of a word, i.e. the total number of times a word appears in a given category
def tf(w, category, script):
    try:
        return script[category][w]
    except KeyError:
        return 0
    
# Compute the Inverse Domain Frequency (IDF) of a word, i.e. log [(total number of categories) /(number of categories that use the word w)]
def idf(w, script):
    num_categories = len(script)
    num_uses = 0 
    for category in script:
        if w in script[category]:
            num_uses += 1

    return math.log(num_categories/num_uses, 10)

# Compute TD-IDF (i.e. TF times IDF)
def tf_idf(w, category, script):
    return tf(w, category, script) * idf(w, script)


def get_tf_idf_dict(script):
    tf_idf_dict = {}
    for category in script:
        tf_idf_dict[f'{category}'] = {}
        # Compute TF-IDF values for all words across all categories
        for word in script[category]:
            tf_idf_dict[f'{category}'][f'{word}'] = tf_idf(word, category, script)

        # Sort this dictionary from highest TF-IDF value to lowest
        tf_idf_dict[f'{category}'] = {k: v for k, v in sorted(tf_idf_dict[f'{category}'].items(), key=lambda item: item[1], reverse=True)}
    
    return tf_idf_dict


def finalize_data(script, num_entries):
    # Invoke get_tf_idf_dict to get a dictionary of the TF-IDF values of ALL words in that dictionary
    tf_idf_dict = get_tf_idf_dict(script)
    final_dict = {}

    # Create a list containing the highest TF-IDF values, and truncate it so that only the first "n" highest TD-IDF values appear
    for category in tf_idf_dict:
        final_dict[f'{category}'] = list(tf_idf_dict[f'{category}'].items())[:num_entries]    

    #final_dict = dict(itertools.islice(tf_idf_dict.items(), num_entries)) 
    return final_dict

def main():
    with open(sys.argv[2], "r") as f_in:
        group_dict = json.loads(f_in.read())
    f_in.close()
    
    group_tfidf = finalize_data(group_dict, 10)
    
    with open(sys.argv[4], "w") as f_out:
        f_out.write(json.dumps(group_tfidf))
    f_out.close() 
    


if __name__ == "__main__":
    main()

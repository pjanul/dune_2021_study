#!/usr/bin/env python3
import pandas as pd
import os, sys
import json
import csv

stopwords = ["a", "about", "above", "across", "after", "again", "against", "all", "almost", "alone", "along", "already", "also", "although", "always", "among", "an", "and", "another", "any", "anybody", "anyone", "anything", "anywhere", "are", "area", "areas", "around", "as", "ask", "asked", "asking", "asks", "at", "away", "b", "back", "backed", "backing", "backs", "be", "became", "because", "become", "becomes", "been", "before", "began", "behind", "being", "beings", "best", "better", "between", "big", "both", "but", "by", "c", "came", "can", "cannot", "case", "cases", "certain", "certainly", "clear", "clearly", "come", "could", "d", "did", "differ", "different", "differently", "do", "does", "done", "down", "down", "downed", "downing", "downs", "during", "e", "each", "early", "either", "end", "ended", "ending", "ends", "enough", "even", "evenly", "ever", "every", "everybody", "everyone", "everything", "everywhere", "f", "face", "faces", "fact", "facts", "far", "felt", "few", "find", "finds", "first", "for", "four", "from", "full", "fully", "further", "furthered", "furthering", "furthers", "g", "gave", "general", "generally", "get", "gets", "give", "given", "gives", "go", "going", "good", "goods", "got", "great", "greater", "greatest", "group", "grouped", "grouping", "groups", "h", "had", "has", "have", "having", "he", "her", "here", "herself", "high", "high", "high", "higher", "highest", "him", "himself", "his", "how", "however", "i", "if", "important", "in", "interest", "interested", "interesting", "interests", "into", "is", "it", "its", "itself", "j", "just", "k", "keep", "keeps", "kind", "knew", "know", "known", "knows", "l", "large", "largely", "last", "later", "latest", "least", "less", "let", "lets", "like", "likely", "long", "longer", "longest", "m", "made", "make", "making", "man", "many", "may", "me", "member", "members", "men", "might", "more", "most", "mostly", "mr", "mrs", "much", "must", "my", "myself", "n", "necessary", "need", "needed", "needing", "needs", "never", "new", "new", "newer", "newest", "next", "no", "nobody", "non", "noone", "not", "nothing", "now", "nowhere", "number", "numbers", "o", "of", "off", "often", "old", "older", "oldest", "on", "once", "one", "only", "open", "opened", "opening", "opens", "or", "order", "ordered", "ordering", "orders", "other", "others", "our", "out", "over", "p", "part", "parted", "parting", "parts", "per", "perhaps", "place", "places", "point", "pointed", "pointing", "points", "possible", "present", "presented", "presenting", "presents", "problem", "problems", "put", "puts", "q", "quite", "r", "rather", "really", "right", "right", "room", "rooms", "s", "said", "same", "saw", "say", "says", "second", "seconds", "see", "seem", "seemed", "seeming", "seems", "sees", "several", "shall", "she", "should", "show", "showed", "showing", "shows", "side", "sides", "since", "small", "smaller", "smallest", "so", "some", "somebody", "someone", "something", "somewhere", "state", "states", "still", "still", "such", "sure", "t", "take", "taken", "than", "that", "the", "their", "them", "then", "there", "therefore", "these", "they", "thing", "things", "think", "thinks", "this", "those", "though", "thought", "thoughts", "three", "through", "thus", "to", "today", "together", "too", "took", "toward", "turn", "turned", "turning", "turns", "two", "u", "under", "until", "up", "upon", "us", "use", "used", "uses", "v", "very", "w", "want", "wanted", "wanting", "wants", "was", "way", "ways", "we", "well", "wells", "went", "were", "what", "when", "where", "whether", "which", "while", "who", "whole", "whose", "why", "will", "with", "within", "without", "work", "worked", "working", "works", "would", "x", "y", "year", "years", "yet", "you", "young", "younger", "youngest", "your", "yours", "z"]


# This function casts everything to lowercase and replaces punctuation with a space
def clean_data(tweet_df):
    
    tweet_df["tweet"] = tweet_df["tweet"].str.lower()
    
    # Delete all URLs
    tweet_df['tweet'] = tweet_df['tweet'].str.replace('http\S+|www.\S+', '', case=False, regex=True)
    
    # Delete any word containing the @ symbol to avoid account names appearing in the data
    tweet_df["tweet"] = tweet_df["tweet"].str.replace('@\w*', "", regex = True)
    
    # Get rid of anything that is not ascii 
    tweet_df = tweet_df.astype(str).apply(lambda x: x.str.encode('ascii', 'ignore').str.decode('ascii'))
    
    # Replace these characters with a space character
    invalid_chars="()[],-.?!:;#&"
    for char in invalid_chars:
        tweet_df["tweet"] = tweet_df["tweet"].str.replace(char, " ", regex = True)
        
    
    
    # Delete words containing only numbers
    tweet_df["tweet"] = tweet_df["tweet"].str.replace(r'\w*\d\w*',"", regex = True)
    
    return(tweet_df)

# This function returns a list whose elements are dataframes 
# Each dataframe contains all tweets for a given category
def create_category_dict(category_list, tweet_df, column_name):
    all_cats_dict = {}
    
    # Convert "dialog" column of dataframe into a dict containing all valid words
    for category in category_list:
        # Handle only the lines relevant to the current category
        current_df = tweet_df[tweet_df[column_name] == f'{category}']
        # Get all words into a dictionary where the key is the word and the value is the number of occurences
        all_cats_dict[f'{category}'] = current_df['tweet'].str.split(expand=True).stack().value_counts()
        # Remove all words that 1) occur < 5 times 2) contain non-alphabetical characters 3) are stopwords
        all_cats_dict[f'{category}'] = {k:int(v) for k,v in all_cats_dict[f'{category}'].items() if k.isalpha() and k not in stopwords}
    
    
    # Create a dictionary keeping track of how many times ALL categories use a given word
    word_count = {}
    for category, word_list in all_cats_dict.items():
        for word, count in word_list.items():
            word_count[word] = word_count.get(word, 0) + count

    # If this word occurs less than 5 times across ALL valid tweets, then remove it from all categories word counts
    for word, count in word_count.items():
        # Check word_count dict if the keys occurs > 5 times
        if count < 5: 
            # Iterate through all_cats_dict and remove all occurrences of that key
            for category, word_list in all_cats_dict.items():
                if word in word_list:
                    word_list.pop(word)

    

    return all_cats_dict

def define_groups():
    if sys.argv[6] == "category":
        return ["r", "c", "s", "b", "m", "e"]
    elif sys.argv[6] == "sentiment":
        return ["g", "n", "b"]
    elif sys.argv[6] == "combined":
        return ["rg", "cg", "sg", "bg", "mg", "eg", "rn", "cn", "sn", "bn", "mn", "en","rb", "cb", "sb", "bb", "mb", "eb"]
    else:
        print("Error: The grouping parameter must be either 'category', 'sentiment', or 'combined'")
        print("Exiting now. Please try again with correct grouping parameter")
        quit()


def main():

    groups = define_groups()

    # Read the input CSV file and only take the 2 relevant columns (category name and tweet contents)
    input_file = pd.read_csv(sys.argv[2])
    df = pd.DataFrame(input_file, columns = ["tweet", sys.argv[6]])
    df = clean_data(df)
    
    #categories = sys.argv[6]
    cat_dict = create_category_dict(groups, df, sys.argv[6])
    
    with open(sys.argv[4], "w") as f_out:
        f_out.write(json.dumps(cat_dict))
        
    f_out.close()
    
 
if __name__ == "__main__":
    main()
    
        

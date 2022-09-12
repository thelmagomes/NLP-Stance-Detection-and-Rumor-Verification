import os
import time
import glob
import json
import pandas as pd

# File paths
TRAINING_PATH = "C:\\CourseWork\\NLP_TextMining\\Project\\rumoureval2019\\rumoureval-2019-training-data\\twitter-english\\"
TRAINING_LABEL_PATH= "C:\\CourseWork\\NLP_TextMining\\Project\\rumoureval2019\\rumoureval-2019-training-data\\train-key.json"
TRAINING_TASK_OUTPUT_PATH = 'C:\\CourseWork\\NLP_TextMining\\Project\\training_task_c_tweets.csv'

# Functions
def extract_reply_tweets(PATH):
    c =0
    tweets = []
    # n = 0

    start = time.time()
    for i in glob.glob(PATH + "*\\*\\*\\*.json" ):
        with open(i, 'r') as f:
            data = json.load(f)
            tweets.append(data)
        # n += 1
    print('Time taken to extract: ' + str(time.time() - start))
    print ('Total Tweets extracted: ' + str(len(tweets)))

    return tweets

def extract_task_a_labels(PATH, OUTPUT_PATH):
    lfile = open(PATH, 'r')
    l = json.load(lfile)
    os.remove(OUTPUT_PATH) if os.path.exists(OUTPUT_PATH) else print(OUTPUT_PATH)

    labels = {}
    for k, v in l['subtaskaenglish'].items():
        if k.isnumeric() == False:
            continue
        labels [int(k)] =  v

    return (labels)

# Extract Reply Tweets and Task A labels
tweets = extract_reply_tweets(TRAINING_PATH)
labels = extract_task_a_labels(TRAINING_LABEL_PATH, TRAINING_TASK_OUTPUT_PATH)

# Normalize the json data to flatten the nested json.
tweets_nm = pd.json_normalize(tweets)

column_list = ['id', 'in_reply_to_status_id_str', 'text', 'user.verified', 'user.followers_count', 'retweet_count', 'favorite_count', 'entities.hashtags', 'entities.urls']
tweets_df = tweets_nm[column_list].copy()


# fetch parent tweet text
parent_text_dict = {}


list_of_parent_text = []
start1 = time.time()
for rowIndex, row in tweets_df.iterrows(): #iterate over rows
    # print ('in rowIndex: ' + str(rowIndex))
    for columnIndex, value in row.items():
            # print (tweet_id)
        if columnIndex == 'id':
            tweet_id = value
        if (columnIndex) == 'in_reply_to_status_id_str':
            if value == None:
                    # print('value is none here')
                    value = tweet_id
                    # Now update the parent_id of this tweet with its own id
                    tweets_df.at [rowIndex, columnIndex] = value

            # print ('in in_reply_to_status_id with value: ')
            # print(value)
            parent_tweet_id = value
            
            # print(ACTUAL_PATH + "\\*\\" + str(value) + "\\source-tweet\\" + str(value) + ".json")
            for i in glob.glob(os.path.join(TRAINING_PATH, '**/' + str(parent_tweet_id) + '.json'), recursive=True):
                # print(i)
                file = open(i, 'r')
                parent_data = json.load(file)
                parent_text = parent_data['text']
                list_of_parent_text.append(parent_text)
                print (parent_text)

# Add Label column to Reply tweets dataframe
tweets_df['label'] = tweets_df['id'].map(labels)
tweets_df['parent_tweet_text'] = pd.Series(list_of_parent_text)
# tweets_df['in_reply_to_status_id_str'].map(parent_text_dict)

# Remove rows of reply tweets that do not have SDQC label in train-key.json file
tweets_df = tweets_df.dropna(subset= ['label'])


# Create CSV file from dataframe
tweets_df.to_csv(TRAINING_TASK_OUTPUT_PATH, index=False, header=True)
print ("Total time" + str(time.time() - start1))


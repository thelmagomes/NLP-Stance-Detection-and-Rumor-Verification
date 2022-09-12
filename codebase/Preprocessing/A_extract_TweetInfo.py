import os
import time
import glob
import json
import pandas as pd

# File paths
#TRAINING
TRAINING_PATH = "C:\\CourseWork\\NLP_TextMining\\Project\\rumoureval2019\\rumoureval-2019-training-data\\twitter-english\\"
TRAINING_LABEL_PATH= "C:\\CourseWork\\NLP_TextMining\\Project\\rumoureval2019\\rumoureval-2019-training-data\\train-key.json"
TRAINING_TASK_A_OUTPUT_PATH = 'C:\\CourseWork\\NLP_TextMining\\Project\\training_task_a_tweets.csv'

#TEST
TEST_PATH = "C:\\CourseWork\\NLP_TextMining\\Project\\rumoureval2019\\rumoureval-2019-test-data\\twitter-en-test-data\\"
TEST_LABEL_PATH= "C:\\CourseWork\\NLP_TextMining\\Project\\rumoureval2019\\final-eval-key.json"
TEST_TASK_A_OUTPUT_PATH = 'C:\\CourseWork\\NLP_TextMining\\Project\\test_task_a_tweets.csv'


# Functions
def extract_reply_tweets(PATH):
    c =0
    tweets = []

    start = time.time()
    for i in glob.glob(PATH + "*\\*\\replies\\*.json" ):
        with open(i, 'r') as f:
            data = json.load(f)
            tweets.append(data)
       
    print('Time taken to extract: ' + str(time.time() - start))
    print ('Total Tweets extracted: ' + str(len(tweets)))

    return tweets

def extract_task_a_labels(PATH, OUTPUT_PATH, subtask_name):
    lfile = open(PATH, 'r')
    l = json.load(lfile)
    os.remove(OUTPUT_PATH) if os.path.exists(OUTPUT_PATH) else print(OUTPUT_PATH)

    labels = {}
    for k, v in l[subtask_name].items():
        if k.isnumeric() == False:
            continue
        labels [int(k)] =  v

    return (labels)

def extract_parent_text(tweets_df, PATH):
    list_of_parent_text = []
    # start1 = time.time()
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
                parent_tweet_id = value

                
                # print(ACTUAL_PATH + "\\*\\" + str(value) + "\\source-tweet\\" + str(value) + ".json")
                for i in glob.glob(os.path.join(PATH, '**/' + str(parent_tweet_id) + '.json'), recursive=True):
                    # print(i)
                    file = open(i, 'r')
                    parent_data = json.load(file)
                    parent_text = parent_data['text']
                    list_of_parent_text.append(parent_text)
                    print (parent_text)
    return list_of_parent_text

# Extract Reply Tweets and Task A labels

#TRAINING
# tweets = extract_reply_tweets(TRAINING_PATH)
# labels = extract_task_a_labels(TRAINING_LABEL_PATH, TEST_TASK_A_OUTPUT_PATH, 'subtaskaenglish')

#TEST
tweets = extract_reply_tweets(TEST_PATH)
labels = extract_task_a_labels(TEST_LABEL_PATH, TRAINING_TASK_A_OUTPUT_PATH, 'subtaskaenglish')

# Normalize the json data to flatten the nested json.
tweets_nm = pd.json_normalize(tweets)
column_list = ['id', 'in_reply_to_status_id_str', 'text', 'user.verified', 'user.followers_count', 'retweet_count', 'favorite_count', 'entities.hashtags', 'entities.urls']
# tweets_df = pd.DataFrame(tweets_nm, columns= column_list)
tweets_df = tweets_nm[column_list].copy()

# # fetch parent tweet text
# list_of_parent_text = extract_parent_text(tweets_df, TRAINING_PATH)
list_of_parent_text = extract_parent_text(tweets_df, TEST_PATH)

# Add Label column to Reply tweets dataframe
    # Labels commented when test data
tweets_df['label'] = tweets_df['id'].map(labels)
tweets_df['parent_tweet_text'] = pd.Series(list_of_parent_text)
# tweets_df['parent_tweet_text'] = tweets_df['in_reply_to_status_id_str'].map(parent_text_dict)

# Remove rows of reply tweets that do not have SDQC label in train-key.json file
    # Labels commented when test data
tweets_df = tweets_df.dropna(subset= ['label'])

# TEST - print first 15 tweets
# print(tweets_df.head(15))

# Create CSV file from dataframe
# tweets_df.to_csv(TRAINING_TASK_A_OUTPUT_PATH, index=False, header=True)
tweets_df.to_csv(TEST_TASK_A_OUTPUT_PATH, index=False, header=True)



import os
import time
import glob
import json
import pandas as pd

# File paths
TRAINING_PATH = "C:\\CourseWork\\NLP_TextMining\\Project\\rumoureval2019\\rumoureval-2019-training-data\\twitter-english\\"
TRAINING_LABEL_PATH= "C:\\CourseWork\\NLP_TextMining\\Project\\rumoureval2019\\rumoureval-2019-training-data\\train-key.json"
TRAINING_TASK_B_OUTPUT_PATH = 'C:\\CourseWork\\NLP_TextMining\\Project\\training_task_b_source_tweets.csv'

#TEST
TEST_PATH = "C:\\CourseWork\\NLP_TextMining\\Project\\rumoureval2019\\rumoureval-2019-test-data\\twitter-en-test-data\\"
TEST_LABEL_PATH= "C:\\CourseWork\\NLP_TextMining\\Project\\rumoureval2019\\final-eval-key.json"
TEST_TASK_B_OUTPUT_PATH = 'C:\\CourseWork\\NLP_TextMining\\Project\\test_task_b_tweets.csv'

# Functions
def extract_source_tweets(PATH):
    tweets = []

    start = time.time()
    for i in glob.glob(PATH + "*\\*\\source-tweet\\*.json" ):
        with open(i, 'r') as f:
            data = json.load(f)
            tweets.append(data)
    print('Time taken to extract: ' + str(time.time() - start))
    print ('Total Tweets extracted: ' + str(len(tweets)))

    return tweets

def extract_task_b_labels(PATH, OUTPUT_PATH):
    lfile = open(PATH, 'r')
    l = json.load(lfile)
    os.remove(OUTPUT_PATH) if os.path.exists(OUTPUT_PATH) else print(OUTPUT_PATH)

    labels = {}
    for k, v in l['subtaskbenglish'].items():
        if k.isnumeric() == False:
            continue
        labels [int(k)] =  v

    return (labels)

# Extract Reply Tweets and Task B labels
    # TRAINING
# tweets = extract_source_tweets(TRAINING_PATH)
# labels = extract_task_b_labels(TRAINING_LABEL_PATH, TRAINING_TASK_B_OUTPUT_PATH)

    # TEST
tweets = extract_source_tweets(TEST_PATH)
labels = extract_task_b_labels(TEST_LABEL_PATH, TEST_TASK_B_OUTPUT_PATH)


# Normalize the json data to flatten the nested json.
tweets_nm = pd.json_normalize(tweets)
column_list = ['id', 'in_reply_to_status_id_str', 'text', 'user.verified', 'user.followers_count', 'retweet_count', 'favorite_count', 'entities.hashtags', 'entities.urls']
# tweets_df = pd.DataFrame(tweets_nm, columns= column_list)
tweets_df = tweets_nm[column_list].copy()

# Add Label column to Reply tweets dataframe
tweets_df['label'] = tweets_df['id'].map(labels)

# Remove rows of reply tweets that do not have SDQC label in train-key.json file
tweets_df = tweets_df.dropna(subset= ['label'])



# Create CSV file from dataframe
# tweets_df.to_csv(TRAINING_TASK_B_OUTPUT_PATH, index=False, header=True)
tweets_df.to_csv(TEST_TASK_B_OUTPUT_PATH, index=False, header=True)

# NLP-Stance-Detection-and-Rumor-Verification

The main purpose of our project is to detect a particular stance for the tweets, verify whether it is a rumor and generate a stance text which supports our model output.

Below are the sub-tasks which will be implemented in phases:
- **SDQC Support Classification**: The reply tweets in the conversation thread of each source tweet
will undergo multi-class SDQC (Support, Deny, Query, Comment) classification.
- **Veracity Prediction**: Multi-class text classification will be implemented on source tweets for them to be determined as True, False or Unverified. Based on the output class, we will obtain a confidence
score ranging from 0 to 1 - where a score of 0 indicates an unverified rumor.
- **Stance Generation**: Our model will generate a stance text using the information we obtained from the above sub-tasks. The source tweet, its reply thread and label assigned to each reply as per
sub-task A will be used to generate the stance response using conditional distribution.

These notebooks were run on Google Colab. 

All datasets for each individual tasks are in datasets folder - while running the code please update the path of these csvs in the notebook accordingly.

Training Datasets:

Subtask A: training_task_a_tweets.csv
Subtask B: training_task_b_source_tweets.csv
Subtask C Seq2Seq: training_task_c_support
                training_task_c_query
                training_task_c_deny
                training_task_c_comments

Subtask C Transformers: training_task_c_tweets.csv

Testing Datasets:

Subtask A: test_task_a_tweets.csv, test_a.csv
Subtask B: test_task_b_tweets.csv


For Subtask C seq2seq model, we have 4 different datasets separated according to the SDQC classification. The path needs to be updated for each of these datasets. While testing, we need to update the source text according to the training data. Similarly, the reference text needs to be updated accordingly.

For subtask C Transformers model, Replace the filename of this format  '/content/outputs/simplet5-epoch-2-train-loss- * -val-loss- *' in the step where second layer model is loading.

For all the notebooks, please implement all the steps in order.
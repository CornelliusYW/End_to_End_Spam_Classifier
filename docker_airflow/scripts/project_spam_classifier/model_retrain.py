import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import pickle
import os


def retrain_model():
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, 'dataset/training_data.csv')
    df = pd.read_csv(file_path)

    vectorizer = CountVectorizer()
    naive_bayes_classifier = MultinomialNB()

    # Creating a pipeline for the whole process
    pipeline = Pipeline([
        ('vectorizer', vectorizer),
        ('classifier', naive_bayes_classifier)
    ])

    pipeline.fit(df['email'], df['spam'])

    relative_path = '../../../storage/spam_classifier_pipeline.pkl'

    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, relative_path)
    
    with open(file_path, 'wb') as file:
        pickle.dump(pipeline, file)

if __name__ == "__main__":
    retrain_model()



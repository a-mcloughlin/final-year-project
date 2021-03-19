import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.feature_selection import chi2
from sklearn.utils import resample
from sklearn.svm import LinearSVC
import pickle
from joblib import dump, load

# A python class to store the relevant data for a scikit learn machine learning model
class ml_model:
    def __init__(self, model, word_count_vect):  
        self.model = model
        self.word_count_vect = word_count_vect
        
# Build a Machine Learning Political Estimator Model from the dataset from the given country
def build_ml_model(country):
    if country == "ie":
        data = pd.read_csv(r'datasets/ml_training/ie_parties_full_set.csv')
    elif country == "uk":
        data = pd.read_csv(r'datasets/ml_training/uk_parties_full_set.csv')
    elif country == "us":
        data = pd.read_csv(r'datasets/ml_training/kaggle_US_dataset_modified.csv')
    else:
        data = pd.read_csv(r'datasets/ml_training/ie_uk_us_full_set.csv')
    
    data.columns = ['Tweet', 'Account', 'Score', 'Leaning']
    scaled_data = resample_data(data)

    test_model(scaled_data)

    word_count_vectoriser = CountVectorizer()
    data_train_wordcounts = word_count_vectoriser.fit_transform(scaled_data.Tweet.astype('U').values)

    tfidf_transformer = TfidfTransformer()
    data_train_tfidf = tfidf_transformer.fit_transform(data_train_wordcounts)
    logicalRegressionModel = LogisticRegression(random_state=0, max_iter=1000).fit(data_train_tfidf, scaled_data['Leaning'])
    
    return logicalRegressionModel, word_count_vectoriser

# Test the logical regression by splitting the data into trainng and testing data,
# and building the Machine Learning model to calculate accuracy on the base dataset
def test_model(model):
    x_train, x_test, y_train, y_test = train_test_split(model['Tweet'], model['Leaning'], random_state = 0, test_size=0.10)
    word_count_vect = CountVectorizer()
    data_train_wordcounts = word_count_vect.fit_transform(x_train.astype('U').values)

    tfidf_transformer = TfidfTransformer()
    data_train_tfidf = tfidf_transformer.fit_transform(data_train_wordcounts)
    logicalRegressionModel = LogisticRegression(random_state=0, max_iter=1000).fit(data_train_tfidf, y_train)
    
    prediction = logicalRegressionModel.predict(word_count_vect.transform(x_test.astype('U').values))
    print(np.mean(prediction == y_test))

# Randomly trim entries from the larger group within the dataset
# This will result in equal size classification groups within the training dataset
def resample_data(data):
    bigger_group = data.groupby('Leaning').Tweet.count().idxmax()
    smaller_group = data.groupby('Leaning').Tweet.count().idxmin()
    
    bigger_group = data[data.Leaning==bigger_group]
    smaller_group = data[data.Leaning==smaller_group]
    
    smaller_downsampled = resample(bigger_group,replace=True, n_samples=len(smaller_group),random_state=27)
    scaled_data = pd.concat([smaller_group, smaller_downsampled])
    
    return scaled_data

# Predict the class of a previously unseen text string
# This will classify any string as liberal or conservative
def predict_from_model(ml_model, word_count_vect, text_data):
    prediction = ml_model.predict(word_count_vect.transform([text_data]))
    return prediction

def retrieve_ml_model(country):
    country_ml_object = load( "datasets/ml_models/"+ country +".joblib" ) 
    model = country_ml_object.model
    word_count_vect = country_ml_object.word_count_vect
    return model, word_count_vect

# build the set of ml models and store them as joblib files for faster processing
def store_models():
    for country in ['ie', 'uk', 'us','global']:
        model, word_count_vect = build_ml_model(country)
        ml_object = ml_model(model, word_count_vect)
        dump(ml_object, "datasets/ml_models/"+country+".joblib")
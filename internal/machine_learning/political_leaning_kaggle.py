import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_selection import chi2
from sklearn.svm import LinearSVC
import csv

def build_ml_model():
    data = pd.read_csv('internal\machine_learning\datasets\kaggle_US_dataset.csv')
    data.columns = ['Party', 'Handle', 'Tweet']
    data['leaning_id'] = data['Party'].factorize()[0]
    leaning_id_df = data[['Party', 'leaning_id']].drop_duplicates().sort_values('leaning_id')
    leaning_to_id = dict(leaning_id_df.values)
    
    tfidf = TfidfVectorizer(sublinear_tf=True, min_df=5, norm='l2', encoding='utf-8', ngram_range=(1, 2), stop_words='english')

    features = tfidf.fit_transform(data.Tweet.astype('U').values)
    labels = data.leaning_id
    features.shape

    x_train, x_test, y_train, y_test = train_test_split(data['Tweet'], data['Party'], random_state = 0, test_size=0.33)
    word_count_vect = CountVectorizer()
    X_train_counts = word_count_vect.fit_transform(x_train.astype('U').values)

    tfidf_transformer = TfidfTransformer()
    X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
    tclf = LinearSVC().fit(X_train_tfidf, y_train)
    
    prediction = tclf.predict(word_count_vect.transform(x_test))
    #print(np.mean(prediction == y_test))
    
    return tclf, word_count_vect

def predict_from_model(model, word_count_vect, text_data):
    prediction = model.predict(word_count_vect.transform([text_data]))
    return prediction

def test():
    model, word_count_vect, x_test, y_test = build_ml_model()
    prediction = predict_from_model(model, word_count_vect, x_test, y_test)
    #prediction = predict_from_model(model, word_count_vect, "process of ending net neutrality for millions of Americans")
    
#test()
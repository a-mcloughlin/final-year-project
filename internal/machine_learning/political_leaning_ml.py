import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.feature_selection import chi2

def build_ml_model(country):
    if country == "ie":
        data = pd.read_csv(r'internal/machine_learning/datasets/ie_parties_04_02_2021.csv')
        print("Using Irish Dataset")
    elif country == "uk":
        data = pd.read_csv(r'internal/machine_learning/datasets/uk_parties_04_02_2021.csv')
        print("Using UK Dataset")
    elif country == "us":
        data = pd.read_csv(r'internal/machine_learning/datasets/kaggle_US_dataset_modified.csv')
        print("Using US Dataset")
    else:
        data = pd.read_csv(r'internal/machine_learning/datasets/ie_uk_us_04_02_2021.csv')
        print("Using IE, UK and US Datasets")
    
    data.columns = ['Tweet', 'Account', 'Score', 'Leaning']
    
    if country != "us":
        from sklearn.utils import resample
        import matplotlib.pyplot as plt
        # fig = plt.figure(figsize=(8,6))
        # data.groupby('Leaning').Tweet.count().plot.bar(ylim=0)
        # plt.show()
        
        conservative = data[data.Leaning=='conservative']
        liberal = data[data.Leaning=='liberal']
        lib_downsampled = resample(liberal,replace=True, n_samples=len(conservative),random_state=27)
        scaled_data = pd.concat([conservative, lib_downsampled])
        scaled_data.Leaning.value_counts()
        conservative = scaled_data[scaled_data.Leaning=='conservative']
        liberal = scaled_data[scaled_data.Leaning=='liberal']
    else:
        scaled_data = data
    
    
    scaled_data['leaning_id'] = scaled_data['Leaning'].factorize()[0]
    leaning_id_df = scaled_data[['Leaning', 'leaning_id']].drop_duplicates().sort_values('leaning_id')
    leaning_to_id = dict(leaning_id_df.values)
    
    from sklearn.svm import LinearSVC

    tfidf = TfidfVectorizer(sublinear_tf=True, min_df=5, norm='l2', encoding='utf-8', ngram_range=(1, 2), stop_words='english')

    features = tfidf.fit_transform(scaled_data.Tweet.astype('U').values)
    labels = scaled_data.leaning_id
    features.shape

    x_train, x_test, y_train, y_test = train_test_split(scaled_data['Tweet'], scaled_data['Leaning'], random_state = 0, test_size=0.33)
    word_count_vect = CountVectorizer()
    X_train_counts = word_count_vect.fit_transform(x_train.astype('U').values)

    tfidf_transformer = TfidfTransformer()
    X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
    tclf = LogisticRegression(random_state=0, max_iter=1000).fit(X_train_tfidf, y_train)
    
    prediction = tclf.predict(word_count_vect.transform(x_test.astype('U').values))
    print(np.mean(prediction == y_test))
    
    return tclf, word_count_vect

def predict_from_model(model, word_count_vect, text_data):
    prediction = model.predict(word_count_vect.transform([text_data]))
    return prediction

def test():
    model, word_count_vect = build_ml_model("us")
    prediction = predict_from_model(model, word_count_vect, "Trump is very bad")
    print(prediction)
 
# Describe the leaning of a political score
def describe_political_leaning(political_score):
    statement = ""
    if political_score < -0.15:
        statement = "More politically Left Leaning than Right Leaning"
    elif political_score > 0.15:
        statement = "More politically Right Leaning than Left Leaning"
    else:
        statement = "These tweets have no strong political leaning"
    return statement
    
#test()
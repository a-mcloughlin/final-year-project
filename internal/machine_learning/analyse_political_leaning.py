from internal.machine_learning.political_leaning_ml import build_ml_model as build_ml_model ,predict_from_model as predict_from_model, describe_political_leaning

def evaluate_politics(tweetset, country):
    
    political_prediction = 0
    ml_model, word_count_vect = build_ml_model(country)
    
    for tweet in tweetset:
        party = predict_from_model(ml_model, word_count_vect, tweet)
        if party == 'liberal':
            political_prediction -= 1
        else:
            political_prediction += 1
            
    political_prediction = political_prediction/len(tweetset)
    
    statement = describe_political_leaning(political_prediction)
    
    dataset_country = "Ireland, The UK and The USA"
    if country == 'ie':
        dataset_country = "Ireland"
    elif country == 'uk':
        dataset_country = "The United Kingdom"
    elif country == 'us':
        dataset_country = "The United States of America"
        
    political_leaning_degree =  (((political_prediction + 1) / 2)*180) + 270
    
    return dataset_country, statement, political_leaning_degree
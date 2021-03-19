from internal.political_leaning.political_leaning_ml import retrieve_ml_model,predict_from_model
import internal.word_processing.interpret_data as interpret_data
        
# From a set of tweets and a country code, predict the political leaning of the set of tweets
# Classify each tweet with a political leaning, and get the predominant leaning
# This variable is represented in the GUI using a guage.
# Store the overall political value so it can be shown as the strength of left/right leaning
def evaluate_politics(tweetset, country):
    
    political_prediction = 0
    ml_model, word_count_vect = retrieve_ml_model(country)
    
    for tweet in tweetset:
        party = predict_from_model(ml_model, word_count_vect, tweet)
        if party == 'liberal':
            political_prediction -= 1
        else:
            political_prediction += 1
            
    political_prediction = political_prediction/len(tweetset)
    print("Pol Pred: "+str(political_prediction))
    statement, summary = interpret_data.describe_political_leaning(political_prediction)
    
    if country == 'ie':
        dataset_country = "Ireland"
        print("Using Irish Dataset")
    elif country == 'uk':
        dataset_country = "The United Kingdom"
        print("Using UK Dataset")
    elif country == 'us':
        dataset_country = "The United States of America"
        print("Using US Dataset")
    else:
        dataset_country = "Ireland, The UK and The USA"
        print("Using IE, UK and US Datasets")
        
        
    political_leaning_degree =  (((political_prediction + 1) / 2)*180) + 270
    
    return dataset_country, statement, political_leaning_degree, summary
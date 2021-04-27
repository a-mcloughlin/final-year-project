# Twitter Analysis Application 

This application is a python tool which can be used to analyse the topic, sentiment and political stance of tweets. 
This python application has a simple Python Flask front-end, and allows users to analyse the tweets within a specific hashtag, or by a specific user. 

The main data points which are gathered from a set of tweets are the sentiment of the tweets, the most common words and phrases within the tweets and the political leaning of the tweets, left leaning to right leaning. This web app will allows users to compare the activity within two separate accounts or hashtags to see similarities and differences. Users can also analyse an individual account in greater depth than when analysing recent tweets buy that account. 

A video demonstration of this tool in action can be found at https://tinyurl.com/aideenmc-fyp-demo 

## Tools implemented

Sentiment analysis is preformed using VADER SentimentIntensityAnalyzer with NLTK.

Emotion Analysis is preformed using the NRC Emotion Lexicon.

Political Leaning analysis is preformed using scikit learn, with 4 different models trained with 4 different datasets of political tweets 
(Irish Politics, UK Politcs, US POlitics, Combination of previous 3 datasets).

## Using the Twitter Analysis Application 

To use this Twitter Analysis tool, you will need Twitter Develope API access, and a rapid API key (for use with Bot decetion tool Botometer).
These credemtials must be stored in a auth.yaml file in the home directory of the code to be accessed by the relevant files. 

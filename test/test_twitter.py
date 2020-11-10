
import unittest
import requests
import internal.twitter.requests as requests
import internal.twitter.auth as auth

test_wordlist = []
base_url = "https://api.twitter.com/2/tweets/search/recent?max_results=100"
until_tweet = "&until_id=12345"

class TestTwitter(unittest.TestCase):
    
    def test_get_tweets_for_tag(self):
        #print("twitter/requests.py get_tweets_for_tag TEST: SUCCESS")
        self.assertEqual(
            requests.get_tweets_for_tag("hash"), 
            base_url + "&query=hash"
        )
        
    def test_get_tweets_for_usr(self):
        self.assertEqual(
            requests.get_tweets_for_user("user"),  
            base_url + "&query=from:user"
        )
        
    def test_get_tweets_for_tag_maxid(self):
        result = self.assertEqual(
            requests.get_tweets_for_tag_maxid("hash", 12345), 
            base_url + "&query=hash" + until_tweet
        )
        
    def test_get_tweets_for_usr_maxid(self):
        self.assertEqual(
            requests.get_tweets_for_usr_maxid("user", 12345), 
            base_url + "&query=from:user" + until_tweet
        )
             
    def test_process_yaml_create_token(self):
        data = auth.process_yaml("test/mocked_auth.yaml")
        self.assertEqual(
            auth.create_token(data), 
            "mocked_token"
        )
        


def run_tests():
    unittest.main()


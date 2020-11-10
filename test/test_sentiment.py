
import unittest
import internal.sentiment.detect_emotions as detect_emotions

class mock_word:  
    def __init__(self, word):  
        self.word = word  
        self.count = 1 

class mock_emotion:
    def __init__(self, name, weight, count):  
        self.name = name  
        self.weight = weight 
        self.count = count
        
    def get_strength(self):
        return round(self.count/self.weight,5)

wordlist = [
    mock_word("According"),mock_word("to"),
    mock_word("all"),mock_word("known"),
    mock_word("laws"),mock_word("of"),
    mock_word("aviation"),mock_word("there"),
    mock_word("is"),mock_word("no"),
    mock_word("way"),mock_word("a"),
    mock_word("bee"),mock_word("should"),
    mock_word("be"),mock_word("able"),
    mock_word("to"),mock_word("fly"),
    mock_word("Its"),mock_word("wings"),
    mock_word("are"),mock_word("too"),
    mock_word("small"),mock_word("to"),
    mock_word("get"),mock_word("its"),
    mock_word("fat"),mock_word("little"),
    mock_word("body"),mock_word("off"),
    mock_word("the"),mock_word("ground"),
    mock_word("The"),mock_word("bee,"),
    mock_word("of"),mock_word("course,"),
    mock_word("flies"),mock_word("anyway"),
    mock_word("because"),mock_word("bees"),
    mock_word("don't"),mock_word("care"),
    mock_word("what"),mock_word("humans"),
    mock_word("think"),mock_word("is"),mock_word("impossible")
]

mock_emotionlist = [
    mock_emotion("joy",689,0),
    mock_emotion("negative",3322,3),
    mock_emotion("positive",2312,0),
    mock_emotion("sadness",1189,2),
    mock_emotion("surprise",534,0),
    mock_emotion("trust",1230,1),
    mock_emotion("anger",1245,1),
    mock_emotion("anticipation",839,0),
    mock_emotion("disgust",1058,1),
    mock_emotion("fear",1473,1)
]

mock_strongest_emotions = [
    mock_emotion("sadness",1189,2),
    mock_emotion("disgust",1058,1),
    mock_emotion("trust",1230,1),
] 

mock_positivity_negativity = [
    mock_emotion("negative",3322,3),
    mock_emotion("positive",2312,0),
]

class TestSentiment(unittest.TestCase):
    
    def test_get_positivity_and_negativity(self):
        positivity_negativity, sentiment = detect_emotions.get_positivity_and_negativity(mock_emotionlist)
        assert_emotionlists_are_equal(self, positivity_negativity, mock_positivity_negativity)
        self.assertEqual(sentiment, "much more Negative than Positive")
    
    def test_get_emotions_from_wordlist(self):
        detected_emotions = detect_emotions.get_emotions_from_wordlist(wordlist)
        assert_emotionlists_are_equal(self, detected_emotions, mock_emotionlist)

    def test_removelistelement(self):
        word1 = detect_emotions.emotion_data('one',0)
        word2 = detect_emotions.emotion_data('two',0)
        test_list = [word1, word2]
        
        self.assertEqual(
            detect_emotions.removelistelement(test_list, "one"), 
            [word2]
        )
            
    def test_get_strongest_emotions(self):
        strongest_emotions = detect_emotions.get_strongest_emotions(mock_emotionlist)
        assert_emotionlists_are_equal(self, strongest_emotions, mock_strongest_emotions)
            
def assert_emotionlists_are_equal(self, list1, list2):
   for index, emotion in enumerate(list1):
            self.assertEqual(emotion.name, list2[index].name)
            self.assertEqual(emotion.weight, list2[index].weight)
            self.assertEqual(emotion.count, list2[index].count)
            self.assertEqual(emotion.get_strength(), list2[index].get_strength()) 

def run_tests():
    unittest.main()


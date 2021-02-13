import botometer
from internal.twitter.auth import process_yaml

class authenticity_measures:
    def __init__(self, astroturf, fake_follower, spammer, financial, self_declared):
        self.astroturf = astroturf 
        self.fake_follower = fake_follower
        self.spammer = spammer
        self.financial = financial
        self.self_declared = self_declared
        
    def average(self):
        probFake = (self.astroturf + self.fake_follower + self.spammer + 
                    self.financial + self.self_declared)/5
        return probFake
        
    def probability(self, authmeasure):
        prob = int(authmeasure*100)
        return prob
    
    def probReal(self, authmeasure):
        probAuthentic = self.probability(1-authmeasure)
        return probAuthentic
        
        
def analyse_acc(auth_file, acctag):
    
    data = process_yaml(auth_file)
    
    rapidapi_key = data["rapid_api"]["rapidapi_key"]
    twitter_app_auth = data['twitter_app_auth']
    
    bom = botometer.Botometer(wait_on_ratelimit=True,rapidapi_key=rapidapi_key,**twitter_app_auth)

    result = bom.check_account(acctag)

    print("Screen Name: "+acctag)
    print("Result: "+str(result['raw_scores']['english']))
    
    
    authenticity = authenticity_measures(result['raw_scores']['english']['astroturf'],
                                                  result['raw_scores']['english']['fake_follower'],
                                                  result['raw_scores']['english']['spammer'],
                                                  result['raw_scores']['english']['financial'],
                                                  result['raw_scores']['english']['self_declared'])
    
    return authenticity
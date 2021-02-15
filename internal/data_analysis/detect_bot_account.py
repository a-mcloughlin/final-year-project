import botometer
from internal.twitter.auth import process_yaml

# Python object to store the Botometer data about a twitter account
class authenticity_measures:
    def __init__(self, astroturf, fake_follower, spammer, financial, self_declared):
        self.astroturf = astroturf 
        self.fake_follower = fake_follower
        self.spammer = spammer
        self.financial = financial
        self.self_declared = self_declared
        
    # The average probability of an account being a bot
    def average(self):
        probFake = (self.astroturf + self.fake_follower + self.spammer + 
                    self.financial + self.self_declared)/5
        return probFake
        
    # Turn the float probability into an int value
    def probability(self, authmeasure):
        prob = int(authmeasure*100)
        return prob
    
    # Taking the probability that an account is a given bot type, 
    # get the probability that the account is NOT that bot type
    def probReal(self, authmeasure):
        probAuthentic = self.probability(1-authmeasure)
        return probAuthentic
        
# Taking the location of a credential file, and the handle of a twitter account,
# Run Botometer on that accountand store the relevant data in an authenticity_measures object
def analyse_acc(auth_file, acctag):
    
    data = process_yaml(auth_file)
    rapidapi_key = data["rapid_api"]["rapidapi_key"]
    twitter_app_auth = data['twitter_app_auth']
    
    bom = botometer.Botometer(wait_on_ratelimit=True,rapidapi_key=rapidapi_key,**twitter_app_auth)

    result = bom.check_account(acctag)

    print("Result: "+str(result['raw_scores']['english']))
    
    authenticity = authenticity_measures(result['raw_scores']['english']['astroturf'],
                                                  result['raw_scores']['english']['fake_follower'],
                                                  result['raw_scores']['english']['spammer'],
                                                  result['raw_scores']['english']['financial'],
                                                  result['raw_scores']['english']['self_declared'])
    
    return authenticity
import tweepy
import time
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

#importing the Machine Learning Model(own created)
from ML_Module import predict,return_X

X = return_X()

def user_authentication(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET):
    auth = tweepy.OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY,ACCESS_SECRET)
    api = tweepy.API(auth)
    return api

def store_last_seen_id(last_seen_id,filename):
    with open(filename,'w') as f:
        f.write(str(last_seen_id))
    return

def get_last_seen_id(filename):
    with open(filename,'r') as f:
        last_seen_id = int(f.read().strip())
    return last_seen_id

def replying_to_mentions():
    print('Searching for Mentions...')
    #Credentials of the BOT
    CONSUMER_KEY = 'CzpUGIjqvqFDv2AB0nbtF8YpZ'
    CONSUMER_SECRET = 'xNbMGiuDlIcJ5Jszm2GfQ4arADzl63gM4FEdPaZHhPXTOyKgEt'
    ACCESS_KEY = '1164128526565380096-pzSZ0TmolmWaM930AlsSODsVKFUxol'
    ACCESS_SECRET = '5irToh1prYEkn0AgWiTmvMGmYDgvpmphXjlKFHUTbyrqI'

    #API for the ML BOT USER
    api = user_authentication(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET)

    FileName = 'last_mention_id.txt'
    last_seen_id = get_last_seen_id(FileName)
    mentions = api.mentions_timeline(last_seen_id,tweet_mode='extended')

    # Getting the desired attributes for the mentioned Users
    for mention in reversed(mentions):
        print('Replying to Mentions...')
        last_seen_id = mention.id
        store_last_seen_id(last_seen_id,FileName)
        X_test = []
        users=mention.entities['user_mentions']
        if(len(users)>1):
            for i in range(1,len(users)):
                screen_name = users[i]['screen_name']
                target=api.get_user(screen_name)
                lst = [target.followers_count,target.friends_count,target.listed_count,target.favourites_count,target.statuses_count,target.default_profile,target.default_profile_image]
                if 'bot' in target.screen_name:
                    lst.append(1)
                else:
                    lst.append(0)
                if 'bot' in target.name:
                    lst.append(1)
                else:
                    lst.append(0)
                X_test.append(lst)
            X_test = np.array(X_test,ndmin=2)

            #Applying feature scaling to Test set
            sc = StandardScaler()
            sc.fit(X)
            X_test = sc.transform(X_test)

            # Predicting Whether the provided user is a bot or not
            y_pred = predict(X_test)
            print(y_pred)
            author = mention.user.screen_name
            #Replying to the tweet
            str = '@' + author + '\nProcessing the given users data...\n'
            for i in range(1,len(users)):
                screen_name = users[i]['screen_name']
                if y_pred[i-1][0]*100 < 50.0:
                    str += '@' + screen_name + ': is a bot with {0:.2f}% chance\n'.format(y_pred[i-1][1]*100)
                else:
                    str += '@' + screen_name + ': is a not a bot with {0:.2f}% chance\n'.format(y_pred[i-1][0]*100)
            api.update_status(str,in_reply_to_status_id = mention.id)
        else:
            api.update_status('Please retweet with a valid mention!',in_reply_to_status_id = mention.id)

while(True):
    replying_to_mentions()
    time.sleep(10)

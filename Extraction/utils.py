import GetOldTweets3 as got



def get_by_key(key,since,until,filename,proxy,numtweet=100):
    try:
        tweetCriteria = got.manager.TweetCriteria().setQuerySearch(key).\
            setSince(since).\
            setUntil(until).\
            setMaxTweets(numtweet)
        if len(proxy)>0:
            tweets = got.manager.TweetManager.getTweets(tweetCriteria,proxy=str(proxy))
        else:
            tweets = got.manager.TweetManager.getTweets(tweetCriteria)

    except:
        return 0
    # tweets = got.manager.TweetManager.getTweets(tweetCriteria,proxy='127.0.0.1:44775')
    if(len(tweets)>0):
        with open(str.format('colected_data/{0}',filename), mode='w+') as f:
            f.write('\n'.join(list([twit.text.encode('utf-8') for twit in tweets])))
            return 1
            # print tweet.text

def get_by_name(name,filename,proxy,numtweet=10):
    try:
        tweetCriteria = got.manager.TweetCriteria().setUsername(name).setMaxTweets(numtweet)
        if len(proxy)>0:
            tweets = got.manager.TweetManager.getTweets(tweetCriteria,proxy=str(proxy))
        else:
            tweets = got.manager.TweetManager.getTweets(tweetCriteria)

    except:
        return [-1]
    # tweets = got.manager.TweetManager.getTweets(tweetCriteria,proxy='127.0.0.1:44775')
    if(len(tweets)>0):
       return tweets
            # print tweet.text


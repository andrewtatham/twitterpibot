



 





rateLimits = None
tweetsRemaining = None




def getRateLimits():
    if twitter is not None:
        rateLimits = twitter.get_application_rate_limit_status()
    tweetsRemaining = 100


def canTweet():
    return tweetsRemaining is not None and tweetsRemaining > 0






def PrintTrends():
    

    #availtrends = twitter.get_available_trends()
    #logging.info(availtrends)
    worldwide_WOEID = 1
    leeds_WOEID = 26042


    worldwide_trends = twitter.get_place_trends(id = worldwide_WOEID)
    #plogging.info.pprint(worldwide_trends)

    leeds_trends = twitter.get_place_trends(id = leeds_WOEID)
    #logging.info(leeds_trends)

    trends = []
    for trend in worldwide_trends[0]["trends"]:
        trendname = trend["name"]
        trends.append(trendname)
    for trend in leeds_trends[0]["trends"]:
        trendname = trend["name"]
        trends.append(trendname)
    print ("Trends...")
    for trend in trends:
        print("")
        print(trend)
        try:
            trendtweets = twitter.search(q = urllib.quote_plus(trend), result_type = "popular")
            for trendtweet in trendtweets["statuses"]:
                print("  " + trendtweet["text"].replace("\n", "   "))
        except Exception as e:   
            logging.exception(e.message, e.args)             
            pprint.pprint(e)

def SuggestedUsers():
    categories = twitter.get_user_suggestions()

    for category in categories:
        print("")
        print(category["name"])
        users = twitter.get_user_suggestions_by_slug(slug = category["slug"])
        #pprint.pprint(users)
        for user in users["users"]:
            #pprint.pprint(user)
            print("")
            print("  " + user["name"])
            print("  @" + user["screen_name"])
            print("  " + user["description"])

        
    




#############################################################




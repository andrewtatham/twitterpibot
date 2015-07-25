
from ScheduledTask import ScheduledTask
from apscheduler.triggers.interval import IntervalTrigger





class SuggestedUsersScheduledTask(ScheduledTask):
    def GetTrigger(args):
        return IntervalTrigger(hours=3)
         
        
    
    def onRun(args):


        print("SUGGESTED USERS")
        
        categories = args.context.twitter.get_user_suggestions()

        for category in categories:
            print("")
            print(category["name"])
            users = args.context.twitter.get_user_suggestions_by_slug(slug = category["slug"])
            #print(users)
            for user in users["users"]:
                #print(user)
                print("")
                print("  " + user["name"])
                print("  @" + user["screen_name"])
                print("  " + user["description"])

      






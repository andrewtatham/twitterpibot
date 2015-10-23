import hardware
import Identity



screen_name = ""
if hardware.isRaspberryPi:
    screen_name = "andrewtathampi"
elif hardware.isRaspberryPi2:
    screen_name = "andrewtathampi2"
elif hardware.iswindows:
    screen_name = "andrewtathampi2"

import TwitterHelper
id = TwitterHelper.Init(screen_name)

def GetResponses():
    from SongResponse import SongResponse
    from PhotoResponse import PhotoResponse
    from Magic8BallResponse import Magic8BallResponse
    from RetweetResponse import RetweetResponse
    from FatherTedResponse import FatherTedResponse
    from MyTwitter import MyTwitter
    from BotBlockerResponse import BotBlockerResponse
    from ThanksResponse import ThanksResponse
    from HelloResponse import HelloResponse
    from RestartResponse import RestartResponse
    from TimelapseResponse import TimelapseResponse
    from TalkLikeAPirateDayResponse import TalkLikeAPirateDayResponse

    responses = [    
        RestartResponse()
    ]

    if hardware.isRaspberryPi:
        responses.extend([
            SongResponse(),
            TalkLikeAPirateDayResponse(),
            ThanksResponse(),
            HelloResponse(),
            Magic8BallResponse()
        ])
        
    if hardware.ispicamattached or hardware.iswebcamattached:
        responses.extend([
            PhotoResponse(),
            TimelapseResponse()
        ])
        
    if hardware.iswindows:
        responses.append(BotBlockerResponse())
        
    if hardware.isRaspberryPi:
        responses.extend([
            FatherTedResponse(),           
            RetweetResponse()
        ])
    return responses

def GetScheduledJobs():

    from EdBallsDay import EdBallsDay
    from Wikipedia import Wikipedia
    from MonitorScheduledTask import MonitorScheduledTask
    from TrendsScheduledTask import TrendsScheduledTask
    from RateLimitsScheduledTask import RateLimitsScheduledTask
    from SuggestedUsersScheduledTask import SuggestedUsersScheduledTask
    from KatieHopkinsScheduledTask import KatieHopkinsScheduledTask
    from UserListsScheduledTask import UserListsScheduledTask
    from WeatherScheduledTask import WeatherScheduledTask
    from BotBlockerScheduledTask import BotBlockerScheduledTask
    from JokesScheduledTask import JokesScheduledTask
    from TimelapseScheduledTask import TimelapseScheduledTask
    from SunriseTimelapseScheduledTask import SunriseTimelapseScheduledTask
    from SunsetTimelapseScheduledTask import SunsetTimelapseScheduledTask
    from NightTimelapseScheduledTask import NightTimelapseScheduledTask
    from SunTimelapseScheduledTask import SunTimelapseScheduledTask
    from SavedSearchScheduledTask import SavedSearchScheduledTask
    from TalkLikeAPirateDayScheduledTask import TalkLikeAPirateDayScheduledTask
    from MidnightScheduledTask import MidnightScheduledTask
    from SongScheduledTask import SongScheduledTask    
    from PhotoScheduledTask import PhotoScheduledTask
    from HappyBirthdayScheduledTask import HappyBirthdayScheduledTask





    scheduledjobs = [
        MonitorScheduledTask(),        
        SuggestedUsersScheduledTask(),
        UserListsScheduledTask(),
        #RateLimitsScheduledTask(),
        SavedSearchScheduledTask(),
        MidnightScheduledTask(),
        BotBlockerScheduledTask()
    ]

    if hardware.isRaspberryPi:
        scheduledjobs.extend([
            TrendsScheduledTask(),
            Wikipedia(),
            EdBallsDay(),
            TalkLikeAPirateDayScheduledTask(),
            #KatieHopkinsScheduledTask(),
            WeatherScheduledTask(),
            JokesScheduledTask(), 
            SongScheduledTask(),
            HappyBirthdayScheduledTask()
        ])
    
    if hardware.iswebcamattached or hardware.ispicamattached:
        scheduledjobs.extend([
            #TimelapseScheduledTask(),
            SunriseTimelapseScheduledTask(),
            SunsetTimelapseScheduledTask(),
            NightTimelapseScheduledTask(),
            SunTimelapseScheduledTask()
        ])   
        if not hardware.iswindows :
            scheduledjobs.append(PhotoScheduledTask())
        
    return scheduledjobs

def GetTasks():
    from ProcessInboxTask import ProcessInboxTask
    from StreamTweetsTask import StreamTweetsTask
    from FadeTask import FadeTask
    tasks = [ProcessInboxTask(),
            StreamTweetsTask(TwitterHelper.GetStreamer(Identity.screen_name))]
    if hardware.ispiglowattached or hardware.isunicornhatattached:
        tasks.append(FadeTask())
    return tasks

from ScheduledTask import ScheduledTask
import random
from OutgoingTweet import OutgoingTweet
from apscheduler.triggers.cron import CronTrigger
from TwitterHelper import Send



class KatieHopkinsScheduledTask(ScheduledTask):
    def adjective(self):
        return random.choice(['fat',
                            'penniless',
                            'ginger',
                            'Muslim',
                            'hippy',
                            'freckled',
                            'sweaty',
                            'smelly',
                            'chubby',
                            'Scottish',
                            'balding',
                            'breastfeeding',
                            'incompetent',
                            'lazy',
                            'cry-baby',
                            'liberal',
                            'left-wing',
                            'uneducated',
                            'unemployed',
                            'pointless',
                            'wannabe',
                            'Buddhist',
                            'tree-hugging',
                            'old',
                            'ugly',
                            'spotty',
                            'dirty',
                            'clueless',
                            'lactose-intolerant',
                            'depressed',
                            'homeless'
                            ])

    def people(self):
        return random.choice(['children',
                            'toddlers',
                            'teenagers',
                            'mothers',
                            'lollipop ladies',
                            'cyclists',
                            'gardeners',
                            'celebrities',
                            'waitresses',
                            'bloggers',
                            'vicars',
                            'joggers',
                            'pensioners',
                            'tramps',
                            'traffic wardens',
                            'ballet dancers',
                            'musicians',
                            'plumbers',
                            'sculptors',
                            'red squirrels',
                            'women',
                            'bus drivers',
                            'bakers',
                            'scientists',
                            'twins',
                            'nurses',
                            'lesbians',
                            'locksmiths',
                            random.choice(['Brummies','Scousers','Geordies','Cockneys','circus-folk']),
                            'farmers',
                            'vegans'
                            ])
    def insult(self):
        return random.choice(['losers',
                        'failures',
                        'has-beens',
                        'sell-outs',
                        'sluts',
                        'virgins',
                        'terrorists',
                        'idiots',
                        'hypocrites',
                        'morons',
                        'wannabes'
                        ])

    def doing(self):
        return random.choice(['on benefits',
                                'called ' + random.choice(['India','China','Brooklyn','Jayden','Lavender','Sarah','John','Barkley','Tiffany','Lexus','Timothy','James']),
                                'wearing burqas',
                                'in loving relationships',
                                'who love their parents',
                                'with pierced ears',
                                'who live on Council Estates',
                                'with friendship bracelets',
                                'with no chins',
                                'with tattoos',
                                'who read ' + random.choice(['The Guardian','The Independent','books']),
                                'on the BBC',
                                'who believe in global warming',
                                'on my bus',
                                'with stutters',
                                'with glasses',
                                'who eat kale',
                                'who own cats',
                                'with ' + random.choice(['Ebola','measles','chicken pox','the flu','asthma']),
                                'in cardigans',
                                'from ' + random.choice(['Belgium','Albania','New Zealand','Tibet','Peru','Gibraltar','Portugal','the North','Scotland','Slough','Greece'])
                                ])

    def fate(self):
        return random.choice(['go back to ' + random.choice(['Belgium','Cornwall','Brazil','Wales','Switzerland','Norway','Finland','Hawaii','Jamaica','the 1970s','the Isle of Man']),
                                'jump off a bridge',
                                'be put in the stocks',
                                'be kept in the zoo',
                                'be taken to court',
                                'have their tonsils removed',
                                'get a haircut',
                                'have their children taken away',
                                'explain themselves to a judge',
                                'join the Navy',
                                'go on a diet',
                                'be ashamed of themselves',
                                'have a bath',
                                'stop wearing denim',
                                'tie their own shoelaces',
                                'be quiet',
                                'buy some new clothes',
                                'get a job',
                                'have their driving licenses revoked',
                                'go back to school',
                                'put some socks on',
                                'apologise',
                                'get a hobby',
                                'change their own nappies',
                                'apologise to my children',
                                'go to jail',
                                'have an abortion'
                                ])

    def fated(self):
        return random.choice(['went back to ' + random.choice(['Canada','Belgium','Cornwall','Brazil','Wales','Switzerland','Norway','Finland','Hawaii','Jamaica','the 1970s','the Isle of Man']),
                                'jumped into the sea',
                                'were arrested',
                                'fell in a moat',
                                'got salmonella',
                                'had their driving licenses revoked',
                                'had their phones taken away',
                                'choked on a grape',
                                'fell down some stairs',
                                'were fired',
                                'had their citizenship revoked',
                                'put some clothes on',
                                'stopped going on about it',
                                'stopped eating so much cheese',
                                'got a room',
                                'stopped whining',
                                'got a hobby',
                                'sat down and shut up',
                                'were put down',
                                'had a bath',
                                'went to the gym',
                                'stopped rubbing it in other people\'s faces',
                                'had an abortion'
                                ])

    def thing(self):
        return random.choice(['the NHS',
                                'herbal tea',
                                'green post-it notes',
                                'the Homeward Bound films',
                                'safely ejecting my USB sticks',
                                'vitamin B tablets',
                                'the Radio Times',
                                'Jehova\'s Witnesses',
                                'bouncy castles',
                                'the sound of laughter',
                                'ponies',
                                'balloon animals',
                                'twiglets',
                                'snowflakes',
                                'goldfish',
                                'badgers',
                                'ethnic food',
                                'David Attenborough',
                                'Geoff from Byker Grove',
                                'Princess Diana',
                                'The Beach Boys',
                                'velcro',
                                'cupboards',
                                'Prawn Cocktail crisps',
                                'waterfalls',
                                'glitter',
                                'cupcakes',
                                'pillows',
                                'children\'s bicycles',
                                'novelty t-shirts',
                                'street artists',
                                'candyfloss',
                                'ball pools',
                                'volleyball',
                                'gluten-free pancakes',
                                'low fat yoghurt',
                                'The Guardian',
                                'the environment'
                                ])
    def needto(self):
        return random.choice(['face reality',
                        'do us all a favour',
                        'stop wasting our time',
                        'get real',
                        'take some responsibility',
                        'admit their mistakes',
                        'get their shit together',
                        'do what we\'ve all been thinking',
                        'admit they\'re in the wrong'
                        ])

        

    def tweet(self):
        message = [
            random.choice(
                    ["I think that ",
                        "Guess what - ",
                        "Let's be realistic, "]) \
                + random.choice([self.adjective() + " "," "]) \
                + random.choice([self.people(), self.insult()]) \
                + " " \
                + self.doing() + " should " + self.fate() + ".",

            random.choice(["It's about time that ","It's high time that ","Isn't it time that "]) \
                + random.choice([self.adjective() + " "," "]) \
                + self.people() + " " + self.doing() + " " + self.fated() + ".",

            random.choice(["Don't blame me but ","Not my fault but ","Let's be honest: ","I'm sorry but ","We all know it's true - ","Face facts: ","News flash... "]) \
                + self.people() + " " + self.doing() \
                + " need to " + self.needto() + " and " + self.fate() + ".",

            random.choice(["Is it just me or are all "]) + self.people() + " " \
                    + random.choice(['also','worse than','just deluded','just wannabe','really just unemployed','actually just','actually']) + " " \
                    + random.choice([self.people(),self.insult()]) + "?",

   

            random.choice(["Face it ","Bad news ","Get real "]) \
                    + self.people() + " you're just " + self.adjective() + " " + self.insult() + ".",

            "I hate " + self.people() + " almost as much as I hate " + self.thing() + '.',

            "If there's one thing I hate more than " + self.people() + " it's " + self.thing() + '.'
            ]
        return random.choice(message)

    def GetTrigger(self):


        return CronTrigger(hour="22-23,00-06", minute = "15/30")

    def onRun(self):
        
        text = self.tweet() + " #KatieHopkinsTweet"
        
        Send(OutgoingTweet(text=text))

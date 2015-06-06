
from InboxItem import InboxItem



class InboxTextItem(InboxItem):

    def Reply(self):
        for word in self.words:
            
            wordLower = word.lower()
              
            if wordLower == "help":
                ReplyWithHelp(context)

            if wordLower == "photo":
                ReplyWithPhoto(context)
            if wordLower in pics:
                ReplyWithDean(context, wordLower)
            if wordLower in songs:
                ReplyWithSong(context, wordLower)
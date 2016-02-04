from twitterpibot.responses.Response import Response
from twitterpibot.songs.Songs import Songs


class SongResponse(Response):
    def __init__(self):
        self.songs = Songs()
        self.songnames = self.songs.all_keys()

    def condition(self, inbox_item):
        return super(SongResponse, self).reply_condition(inbox_item) \
               and self.contains(inbox_item.words, self.songnames)

    def contains(self, list_a, list_b):
        for item_a in list_a:
            for item_b in list_b:
                if item_a.lower() == item_b.lower():
                    return True
        return False

    def respond(self, inbox_item):
        for word in inbox_item.words:
            for songname in self.songnames:
                if word.lower() == songname.lower():
                    self.songs.sing_song(song_key=songname, inbox_item=inbox_item)

from twitterpibot.responses.Response import Response
import twitterpibot.songs.Songs


class SongResponse(Response):
    def __init__(self, identity):
        Response.__init__(self, identity)
        self.songs = twitterpibot.songs.Songs.Songs()
        self.songnames = self.songs.all_keys()

    def condition(self, inbox_item):
        return mentioned_reply_condition(inbox_item) \
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
                    song_key = songname
                    song = self.songs.get_song(song_key)
                    self.identity.twitter.sing_song(song=song, inbox_item=inbox_item)

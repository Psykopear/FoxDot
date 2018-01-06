import time

from FoxDot import loop
from FoxDot.lib.Players import Player

from .auth import Auth
from .freesound import FreesoundClient


class Library:
    def __init__(self):
        """
        Authorize to the freesound api so we can make calls
        """
        self.auth = Auth()
        self.sounds = None
        self.client = FreesoundClient()
        self.client.set_token(self.auth.config.access_token, "oauth")

    def search(self, query, page=1):
        """
        Returns iterator of freesound's Sound objects resulting from the query
        """
        fields = "id,name,previews,download,images"
        filter = "type:wav"
        self.sounds = self.client.text_search(query=query, fields=fields, filter=filter, page=page)
        for s in self.sounds:
            print(s.name)

    def hear(self, auto=True):
        """
        Run through last search's results files and hear a preview
        """
        player = Player()
        for sound in self.sounds:
            print("==> Playing %s preview..." % sound.name)
            sound.retrieve_preview('/tmp/freesound')
            player >> loop(sound.path, bpm=60)
            if auto:
                time.sleep(2)
            else:
                input("Press anything to go to the next file")
            player.reset()

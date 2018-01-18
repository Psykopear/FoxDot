import string
import time

from os import listdir

from .auth import Auth
from .freesound import FreesoundClient
from ...Buffers import loop, symbolToDir
from ...Players import Player


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
        self.sounds = self.client.text_search(
            query=query,
            fields=fields,
            filter=filter,
            page=page
        )
        for s in self.sounds:
            print(s.name)

    def add_to_foxdot(self, sound_index, directory_symbol, order=None):
        filenames = sorted([f for f in listdir(symbolToDir(directory_symbol))])
        order = order or len(filenames) + 1
        if order <= 1:
            next_name = filenames[0]
        elif order > len(filenames):
            prev_name = filenames[-1]
        else:
            prev_name = filenames[order - 1]
            next_name = filenames[order]

        new_filename = ''
        for index, world_letter in enumerate(prev_name):
            for letter in string.printable:
                if letter > world_letter and letter < next_name[index]:
                    new_filename = letter
                    break
            if len(new_filename) == 1:
                new_filename += string.printable[
                    string.printable.index(next_name[1]) - 1]
                break
            else:
                new_filename += world_letter

        new_filename = '{}{}.wav'.format(
            new_filename,
            self.sounds[sound_index].name.split(".wav")[0])

        self.sounds[sound_index].retrieve(
            symbolToDir(directory_symbol), new_filename)

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
                input("Press anything to go to the next file. ")
            player.reset()

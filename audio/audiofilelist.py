from filesystem.filelist import FileList
from audio.audiofile import AudioFile
import random

class AudioFileList(FileList):
    def shuffle(self):
        super().shuffle()
        self.sort(AudioFile.get_play_count)
        # too strict to just sort by play count. Let's shuffle things up a bit more
        size = self.size()
        half_size = size // 2
        twenty_percent = size // 5
        for i in range(twenty_percent):
            first = random.randint(0, half_size - 1)
            second = random.randint(half_size, size - 1)
            self.filelist[first], self.filelist[second] = self.filelist[second], self.filelist[first]


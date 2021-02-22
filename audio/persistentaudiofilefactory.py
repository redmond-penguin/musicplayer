from audio.audiofile import AudioFile
from audio.sidfile import SidFile
from audio.medfile import MedFile
from audio.wavfile import WavFile
from audio.oggfile import OggFile
from audio.mp3file import Mp3File

from audio.audiofilefactory import AudioFileFactory
import os

class PersistentAudioFileFactory(AudioFileFactory):
    def __init__(self, storage):
        super().__init__()
        self.storage = storage
    
    def create_file(self, path):
        f = super().create_file(path)
        try:
            play_count = self.storage[path]
        except KeyError:
            self.storage[str(path)] = 0
            play_count = 0
        f.set_play_count(play_count)
        f.attach(self)
        return f

    def update(self, subject):
        if not isinstance(subject, AudioFile):
            raise ValueError()
        path = subject.get_path()
        self.storage[str(path)] = subject.get_play_count()


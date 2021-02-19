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
        try:
            f = self.storage[path]
        except KeyError:
            f = super().create_file(path)
            self.storage[str(path)] = f
        f.attach(self)
        return f

    def update(self, subject):
        if not isinstance(subject, AudioFile):
            raise ValueError()
        path = subject.get_path()
        self.storage[str(path)] = subject


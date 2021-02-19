from audio.audiofile import AudioFile
from audio.sidfile import SidFile
from audio.medfile import MedFile
from audio.wavfile import WavFile
from audio.oggfile import OggFile
from audio.mp3file import Mp3File
from audio.flacfile import FlacFile

from filesystem.basefilefactory import BaseFileFactory
import os

class AudioFileFactory(BaseFileFactory):
    def __init__(self):
        self.allowed_extensions = (".sid", ".wma", ".med", ".wav", ".ogg", ".mp3", ".flac")
    
    def create_file(self, path):
        if not isinstance(path, str):
            raise TypeError("path must be a string")
        (path_name, path_extension) = os.path.splitext(path)
        path_extension = path_extension.lower()
        if path_extension == ".sid":
            return SidFile(path)
        elif path_extension == ".wma":
            return AudioFile(path)
        elif path_extension == ".med":
            return MedFile(path)
        elif path_extension == ".wav":
            return WavFile(path)
        elif path_extension == ".ogg":
            return OggFile(path)
        elif path_extension == ".mp3":
            return Mp3File(path)
        elif path_extension == ".flac":
            return FlacFile(path)
        else:
            raise ValueError("Unsupported extension: " + path_extension)
        
    def supports_filename(self, filename):
         (name, extension) = os.path.splitext(filename)
         return extension.lower() in self.allowed_extensions

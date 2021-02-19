from audio.audiofile import AudioFile

class WavFile(AudioFile):
    def play(self):
        self.perform_operation("mplayer")
        
    def play_async(self):
        return self.perform_operation_async("mplayer", ["-really-quiet"])

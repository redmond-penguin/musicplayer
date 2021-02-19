from audio.audiofile import AudioFile

class OggFile(AudioFile):
    def play(self):
        self.perform_operation("ogg123")

    def play_async(self):
        return self.perform_operation_async("ogg123", ["-q"])

    def convert_to_wav(self, output_file):
        self.perform_operation("oggdec", ["-o", output_file])

    def convert_from_wav(self, input_file):
        self.perform_operation("oggenc", [input_file, "-o"])

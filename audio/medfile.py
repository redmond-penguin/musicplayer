from audio.audiofile import AudioFile

class MedFile(AudioFile):
    def play(self):
        self.perform_operation("uade123")

    def play_async(self):
        return self.perform_operation_async("uade123", ["--stderr"])

    def convert_to_wav(self, output_file):
        self.perform_operation("uade123", ["--disable-timeouts", "-f", output_file])
        
    def convert_from_wav(self, input_file):
        raise NotImplementedError()

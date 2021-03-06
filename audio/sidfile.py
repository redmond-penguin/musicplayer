from audio.audiofile import AudioFile

class SidFile(AudioFile):
    def play(self):
        self.perform_operation("sidplay2")

    def play_async(self):
        return self.perform_operation_async("sidplay2", ["-q", "-t5:00"])

    def convert_to_wav(self, output_file):
        self.perform_operation("sidplay2", ["-w" + output_file])
        
    def convert_from_wav(self, input_file):
        raise NotImplementedError()

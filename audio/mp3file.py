from audio.audiofile import AudioFile

class Mp3File(AudioFile):
    def play(self):
        self.perform_operation("mpg123")

    def play_async(self):
        return self.perform_operation_async("mpg123", ["-q", "--rva-mix", "--no-control"])

    def convert_to_wav(self, output_file):
        self.perform_operation("mpg123", None, ["-w", output_file])

    def convert_from_wav(self, input_file, pipe_input=None):
      if pipe_input is None:
        self.perform_operation("lame", ["-q", "0", "-V", "0", input_file])
      else:
        self.perform_operation("lame", ["-q", "0", "-V", "0", "-"], None, False, pipe_input)

from audio.oggfile import OggFile

class FlacFile(OggFile):
    def convert_to_wav(self, output_file, output_to_pipe=False):
      if not output_to_pipe:
        self.perform_operation("flac", None, ["-d", "-o", output_file])
      else:
        return self.perform_operation("flac", None, ["-d", "-c"], True)


    def convert_from_wav(self, input_file):
        self.perform_operation("flac", [input_file])

    def play_async(self):
        return self.perform_operation_async("mplayer", ["-really-quiet"])

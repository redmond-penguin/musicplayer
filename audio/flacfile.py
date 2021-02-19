from audio.oggfile import OggFile

class FlacFile(OggFile):
    def convert_to_wav(self, output_file):
        self.perform_operation("flac", None, ["-d", "-o", output_file])

    def convert_from_wav(self, input_file):
        self.perform_operation("flac", [input_file])

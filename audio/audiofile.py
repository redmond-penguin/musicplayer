from filesystem.basefile import BaseFile

class AudioFile(BaseFile):
    def __init__(self, path):
        self.play_count = 0
        BaseFile.__init__(self, path)
    
    def play(self):
        self.perform_operation("play")

    def play_async(self):
        return self.perform_operation_async("vlc", ["-q", "-I", "dummy", "--play-and-exit"])

    def convert_to_wav(self, output_file):
        raise NotImplementedError()

    def convert_from_wav(self, input_file):
        raise NotImplementedError()

    def get_play_count(self):
        return self.play_count

    def set_play_count(self, count):
        if count != self.play_count: 
            self.play_count = count
            self.notify()

    def play_song(self):
        self.set_play_count(self.play_count + 1)
        return self.play_async()

from filesystem.basefile import BaseFile
import math

tiny_tag = True
try:
    from tinytag import TinyTag
except ModuleNotFoundError:
    tiny_tag = False
    pass
music_tag = True
try:
    import music_tag
except ModuleNotFoundError:
    music_tag = False
    pass

class AudioFile(BaseFile):
    def __init__(self, path):
        self.play_count = 0
        self.tag = None
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
        p = self.play_async()
        self.set_play_count(self.play_count + 1)
        return p

    def get_tag(self):
        if self.tag is None:
            if tiny_tag:
                try:
                    self.tag = TinyTag.get(self.get_path())
                except:
                    self.tag = None
        return self.tag

    def get_description(self):
        tag = self.get_tag()
        if tag is not None:
            if tag.title is not None:
                title = tag.title
            else:
                title = "<no title>"
            if tag.artist is not None:
                artist = tag.artist
            else:
                artist = "<no artist>"
            if tag.album is not None:
                album = tag.album
            else:
                album = "<no album>"
            if tag.duration is not None:
                duration = "{0:02n}:{1:02n}".format(tag.duration // 60, math.floor(tag.duration % 60))
            else:
                duration = "<unknown duration>"
            description = title + " - " + artist + " / " + album + " (" + duration + ")"
        else:
            description = self.get_path()
        return description

    def set_tag(self, tag):
      if tag is not None:
        if music_tag:
          print("tagging file...")
          f = music_tag.load_file(self.get_path())
          if tag.title is not None:
            f['tracktitle'] = tag.title
          if tag.track is not None:
            f['tracknumber'] = tag.track
          if tag.artist is not None:
            f['artist'] = tag.artist
          if tag.album is not None:
            f['album'] = tag.album
          if tag.albumartist is not None:
            f['album_artist'] = tag.albumartist
          f.save()
          print("Finished tagging file")
      return 1


    def get_bitrate(self):
        tag = self.get_tag()
        if tag is not None:
            return tag.bitrate
        else:
            return 0.0
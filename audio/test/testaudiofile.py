import unittest
from audio.audiofile import AudioFile

class TestAudioFile(unittest.TestCase):
    def setUp(self):
        self.file = AudioFile("testfile")

    def test_convert_to_wav(self):
        with self.assertRaises(NotImplementedError):
            self.file.convert_to_wav("test.wav")

    def test_convert_from_wav(self):
        with self.assertRaises(NotImplementedError):
            self.file.convert_from_wav("test.wav")
 
if __name__ == '__main__':
	unittest.main()
  

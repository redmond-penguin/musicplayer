import unittest
from audio.sidfile import SidFile
from audio.medfile import MedFile
from audio.wavfile import WavFile
from audio.oggfile import OggFile
from audio.mp3file import Mp3File
from audio.audiofilefactory import AudioFileFactory

class TestBaseFileFactory(unittest.TestCase):
    def setUp(self):
        self.filefactory = AudioFileFactory()

    def test_create_sidfile(self):
        f = self.filefactory.create_file("sjoe.sid")
        self.assertIs(type(f), SidFile)
        self.assertEqual(f.get_path(), "sjoe.sid")

    def test_create_sidfile_uppercase_extension(self):
        f = self.filefactory.create_file("sjoe.SID")
        self.assertIs(type(f), SidFile)
        self.assertEqual(f.get_path(), "sjoe.SID")
        
    def test_create_sidfile_mixedcase_extension(self):
        f = self.filefactory.create_file("sjoe.SiD")
        self.assertIs(type(f), SidFile)
        self.assertEqual(f.get_path(), "sjoe.SiD")
        
    def test_create_medfile(self):
        f = self.filefactory.create_file("sjoe.med")
        self.assertIs(type(f), MedFile)
        self.assertEqual(f.get_path(), "sjoe.med")

    def test_create_wavfile(self):
        f = self.filefactory.create_file("sjoe.wav")
        self.assertIs(type(f), WavFile)
        self.assertEqual(f.get_path(), "sjoe.wav")
        
    def test_create_oggfile(self):
        f = self.filefactory.create_file("sjoe.ogg")
        self.assertIs(type(f), OggFile)
        self.assertEqual(f.get_path(), "sjoe.ogg")

    def test_create_mp3file(self):
        f = self.filefactory.create_file("sjoe.mp3")
        self.assertIs(type(f), Mp3File)
        self.assertEqual(f.get_path(), "sjoe.mp3")
        
    def test_create_wrong_argument_type(self):
        with self.assertRaises(TypeError):
            file2 = self.filefactory.create_file(self.filefactory)
        with self.assertRaises(TypeError):
            file2 = self.filefactory.create_file(None)
            
    def test_create_wrong_argument_value(self):
        with self.assertRaises(ValueError):
            file2 = self.filefactory.create_file("sjoe.doc")

    def test_supports_filename(self):
        self.assertTrue(self.filefactory.supports_filename("sjoe.mp3"))
        self.assertTrue(self.filefactory.supports_filename("sjoe.ogg"))
        self.assertTrue(self.filefactory.supports_filename("sjoe.wav"))
        self.assertTrue(self.filefactory.supports_filename("sjoe.wma"))
        self.assertTrue(self.filefactory.supports_filename("sjoe.sid"))
        self.assertTrue(self.filefactory.supports_filename("sjoe.med"))
        self.assertTrue(self.filefactory.supports_filename("sjoe.wAv"))
        self.assertTrue(self.filefactory.supports_filename("sjoe.WAV"))
        self.assertFalse(self.filefactory.supports_filename("sjoe.doc"))
        self.assertTrue(self.filefactory.supports_filename("/tmp/sjoe.wav"))
 
if __name__ == '__main__':
	unittest.main()
  

import unittest
from filesystem.basefile import BaseFile
from filesystem.basefilefactory import BaseFileFactory

class TestBaseFileFactory(unittest.TestCase):

	def setUp(self):
	        self.filefactory = BaseFileFactory()
	
	def test_create(self):
		f = self.filefactory.create_file("sjoe")
		self.assertIsInstance(f, BaseFile)
		self.assertIs(type(f), BaseFile)
		self.assertEqual(f.get_path(), "sjoe")

	def test_create_wrong_argument_type(self):
		with self.assertRaises(TypeError):
			file2 = self.filefactory.create_file(None)
 
if __name__ == '__main__':
	unittest.main()
  

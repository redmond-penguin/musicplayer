import unittest
from filesystem.filelist import FileList
from filesystem.basefilefactory import BaseFileFactory
from filesystem.basefile import BaseFile
import os

class TestFileList(unittest.TestCase):
    def setUp(self):
        self.filelist = FileList(None, BaseFileFactory())
        os.mknod("/tmp/testfile")
        os.mknod("/tmp/testfile2")
        os.mkdir("/tmp/testdir")
        os.mknod("/tmp/testdir/testfile3")
        if not os.path.isfile("/tmp/testfile"):
            raise Exception("Cannot create /tmp/testfile")
        if not os.path.isfile("/tmp/testfile2"):
            raise Exception("Cannot create /tmp/testfile2")
        if not os.path.isdir("/tmp/testdir"):
            raise Exception("Cannot create /tmp/testdir")
        if not os.path.isfile("/tmp/testdir/testfile3"):
            raise Exception("Cannot create /tmp/testdir/testfile3")
        
    def tearDown(self):
        if os.path.isfile("/tmp/testfile"):
            os.remove("/tmp/testfile")
        if os.path.isfile("/tmp/testfile2"):
            os.remove("/tmp/testfile2")
        if os.path.isfile("/tmp/testdir/testfile3"):
            os.remove("/tmp/testdir/testfile3")
        if os.path.isdir("/tmp/testdir"):
            os.rmdir("/tmp/testdir")
        
    def test_add_file(self):
        self.assertEqual(self.filelist.size(), 0)
        self.filelist.add_file("/tmp/testfile")
        self.assertEqual(self.filelist.size(), 1)
        self.filelist.add_file("/tmp/testfile2")
        self.assertEqual(self.filelist.size(), 2)
        self.assertEqual(self.filelist.get_file(0).get_path(), "/tmp/testfile")
        self.assertEqual(self.filelist.get_file(1).get_path(), "/tmp/testfile2")

    def test_add_file_wrong_argument(self):
        with self.assertRaises(TypeError):
            self.filelist.add_file(BaseFile())
      
    def test_get_file(self):
        self.filelist.add_file("/tmp/testfile")
        self.filelist.add_file("/tmp/testfile2")
        f = self.filelist.get_file(0)
        f2 = self.filelist.get_file(1)
        self.assertIsInstance(f, BaseFile)
        self.assertIsInstance(f2, BaseFile)
        self.assertEqual(f.get_path(), "/tmp/testfile")
        self.assertEqual(f2.get_path(), "/tmp/testfile2")

    def test_get_file_wrong_index(self):
        with self.assertRaises(IndexError):
            f = self.filelist.get_file(-1)
        with self.assertRaises(IndexError):
            f = self.filelist.get_file(0)
        with self.assertRaises(IndexError):
            f = self.filelist.get_file(1)
        with self.assertRaises(TypeError):
            f = self.filelist.get_file("/tmp/testfile")

    def test_add_path_to_list(self):
        self.filelist.add_path_to_list("/tmp/testdir")
        self.assertEqual(self.filelist.size(), 1)
        f = self.filelist.get_file(0)
        self.assertEqual(f.get_path(), "/tmp/testdir/testfile3")
        
if __name__ == '__main__':
	unittest.main()
  

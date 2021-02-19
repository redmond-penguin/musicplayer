import unittest
from filesystem.basefile import BaseFile
import os

class TestBaseFile(unittest.TestCase):
    def setUp(self):
        os.mknod("/tmp/testfile")
        if not os.path.isfile("/tmp/testfile"):
            raise Exception("Cannot create /tmp/testfile")
        self.file = BaseFile("/tmp/testfile")
        self.updater = None

    def update(self, caller):
        self.updater = caller
        
    def tearDown(self):
        if os.path.isfile("/tmp/testfile"):
            os.remove("/tmp/testfile")
        
    def test_get_path(self):
        self.assertEqual(self.file.get_path(), "/tmp/testfile")

    def test_create(self):
        file2 = BaseFile("testname")
        self.assertIsInstance(file2, BaseFile)
        self.assertEqual(file2.get_path(), "testname")

    def test_create_wrong_argument_to_constructor(self):
        with self.assertRaises(TypeError):
            file2 = BaseFile(self.file)
        with self.assertRaises(TypeError):
            file2 = BaseFile(None)
        with self.assertRaises(TypeError):
            file2 = BaseFile(15)

    def test_perform_operation(self):
        return_value = self.file.perform_operation("/bin/echo")
        self.assertEqual(return_value, 0)

    def test_perform_operation_before_arg(self):
        return_value = self.file.perform_operation("/bin/echo", ["before"])
        self.assertEqual(return_value, 0)

    def test_perform_operation_after_arg(self):
        return_value = self.file.perform_operation("/bin/echo", None, ["after"])
        self.assertEqual(return_value, 0)

    def test_perform_operation_before_and_after_arg(self):
        return_value = self.file.perform_operation("/bin/echo", ["before"], ["after"])
        self.assertEqual(return_value, 0)

    def test_perform_operation_wrong_arg(self):
        return_value = self.file.perform_operation("/bin/sed")
        self.assertEqual(return_value, 4)

    def test_perform_operation_unknown_command(self):
        with self.assertRaises(OSError):
            return_value = self.file.perform_operation("dummytest")
        
    def test_delete_file(self):
        self.file.delete()
        self.assertFalse(os.path.isfile(self.file.get_path()))
        
    def test_delete_nonexistent_file(self):
        file2 = BaseFile("dummytest")
        with self.assertRaises(OSError) as cm:
            file2.delete()
        self.assertEqual(cm.exception.filename, "dummytest")

    def test_attach(self):
        self.file.attach(self)
        self.assertEqual(len(self.file._observers), 1)
        self.assertEqual(self.file._observers[0], self)
        file2 = BaseFile("dummytest")
        self.file.attach(file2)
        self.assertEqual(len(self.file._observers), 2)
        self.assertEqual(self.file._observers[1], file2)

    def test_detach(self):
        self.file.attach(self)
        self.file.detach(self)
        self.assertEqual(len(self.file._observers), 0)

    def test_notify(self):
        self.file.notify()
        self.assertIsNone(self.updater)
        self.file.attach(self)
        self.file.notify()
        self.assertEqual(self.updater, self.file)
        self.file.detach(self)
        self.updater = None
        self.file.notify()
        self.assertIsNone(self.updater)
 
if __name__ == '__main__':
	unittest.main()
  

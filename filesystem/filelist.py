import random
import os
import sys
from filesystem.basefilefactory import BaseFileFactory
from filesystem.basefile import BaseFile

class FileList(object):
    """Represents a list of BaseFile objects."""
    def __init__(self, path_list = None, factory = None):
        """Initialize a FileList instance.
        
        Arguments:
        path_list -- A list of paths to recursively search for files.
                     All files that the factory knows how to handle will be added.
        factory   -- A factory to create the BaseFile objects based on their paths.
        """
        self.filelist = []
        self.index = 0
        if not path_list is None:
            for path in path_list:
                self.add_path_to_list(path)
        if factory is None:
            self.factory = BaseFileFactory()
        else:
            self.factory = factory

    def __iter__(self):
            return self     

    def __next__(self):
        if self.index == self.size():
            self.index = 0
            raise StopIteration
        self.index = self.index + 1
        return self.filelist[self.index - 1]

    def add_path_to_list(self, path):
        """Recursively add the files in a path to the file list.
 
        Arguments:
 
        path_list -- A paths to recursively search for files.
                     All files that the factory knows how to handle will be added.
        """
        files_and_dirs = os.walk(str(path))
        for root, dirs, files in files_and_dirs:
            files_to_add = [ self.factory.create_file(os.path.realpath(os.path.join(root, name))) for name in files if self.factory.supports_filename(name) ]
            self.filelist.extend(files_to_add)
        self.filelist.sort(key=BaseFile.get_path)

    def add_file(self, file_path):
        """Add a single BaseFile instance to the list.
        
        Arguments:
        file_path -- The path of the file to be added. If the factory
                     cannot create a BaseFile based on this path, a ValueError exception
                     is raised.
        """
        f = self.factory.create_file(file_path)
        self.filelist.append(f)
                
    def shuffle(self):
        """Rearrange the files in the list in a random fashion."""
        random.shuffle(self.filelist)

    def size(self):
        """Return the number of files in the file list."""
        return len(self.filelist)
        
    def perform_operation(self, operation_path, args_before=None, args_after=None, seconds_to_wait=0, mode=os.P_WAIT):
        """Execute a system command on all files in the list, one by one.
        See BaseFile.perform_operation for details on the arguments.
        """
        for f in self.filelist:
            f.perform_operation(operation_path, args_before, args_after, seconds_to_wait, mode)

    def get_file(self, index):
        """Return the BaseFile instance at a certain position in the list.
        
        Arguments:
        index -- The index of the file in the list. Must be at least 0 and at most size() - 1.
        """
        return self.filelist[index]
        
    def perform_method(self, meth):
        """Call a method on each BaseFile instance in the list, one by one."""
        for f in self.filelist:
            meth(f)

    def sort(self, k, r=False):
        self.filelist.sort(key=k, reverse=r)

import os
import subprocess

output=open(os.devnull, 'w')
inp=open(os.devnull, 'r')

class BaseFile:
    """The base file class. Represents a physical file which is supposed to exist."""
    def __init__(self, path):
        """Initialize a new BaseFile instance.

        Arguments:
        path -- The path of the file which will be kept in the member filepath.
        """
        if not isinstance(path, str):
            raise TypeError("path must be a string")
        self.filepath = path
        self._observers = []

    def get_path(self):
        """Return the member 'filepath'.

        'filepath' is a string that indicates the physical location of the file in the filesystem.
        """
        return self.filepath
	
    def get_extension(self):
        (path_name, path_extension) = os.path.splitext(self.filepath)
        return path_extension.lower()[1:]

    def perform_operation(self, operation_path, args_before=None, args_after=None, output_to_pipe=False, pipe_input=None):
        """Execute a system command with at least filepath as a parameter.

        Arguments:
        operation_path  -- The path and name of the command to be executed.
        args_before     -- The arguments to appear before the file path in the command
        args_after      -- The arguments to appear after the file path in the command
        """
        if args_before is None:
            args_before = []
        if args_after is None:
            args_after = []
        path = self.get_path()
        args = [operation_path] + args_before + [path] + args_after
        if not output_to_pipe:
          return subprocess.call(args, stdin=pipe_input)
        else:
          return subprocess.Popen(args, stdout=subprocess.PIPE).stdout

    def perform_operation_async(self, operation_path, args_before=None, args_after=None):
        """Execute a system command with at least filepath as a parameter.

        Arguments:
        operation_path  -- The path and name of the command to be executed.
        args_before     -- The arguments to appear before the file path in the command
        args_after      -- The arguments to appear after the file path in the command
        """
        if args_before is None:
            args_before = []
        if args_after is None:
            args_after = []
        path = self.get_path()
        global output
        global inp
        return subprocess.Popen([operation_path] + args_before + [path] + args_after, stderr=output, stdin=inp)

    def delete(self):
        """Delete the physical file indicated by file_path."""
        os.remove(self.get_path())

    def attach(self, observer):
        if not observer in self._observers:
            self._observers.append(observer)

    def detach(self, observer):
        try:
            self._observers.remove(observer)
        except ValueError:
            pass

    def notify(self, modifier=None):
        for observer in self._observers:
            if modifier != observer:
                observer.update(self)


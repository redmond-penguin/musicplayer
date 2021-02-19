from filesystem.basefile import BaseFile

class BaseFileFactory:
    def create_file(self, path):
        return BaseFile(path)

    def supports_filename(self, filename):
        return True

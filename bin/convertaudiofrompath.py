#!/usr/bin/env python3
import sys
import os
import argparse
scriptpath = os.path.abspath(os.path.dirname(__file__))
includepath = os.path.dirname(scriptpath)
sys.path.insert(0, includepath)
from audio.audiofilefactory import AudioFileFactory
from audio.audioconversionservice import AudioConversionService
from filesystem.filelist import FileList

parser = argparse.ArgumentParser(description="Convert music files", epilog="File types are auto-derived from the filename extensions.")
parser.add_argument("source_path", help="The source path")
parser.add_argument("destination_path", help="The destination path")
args = parser.parse_args()
source_path = args.source_path
destination_path = args.destination_path
factory = AudioFileFactory()
list = FileList(None, factory)
list.add_path_to_list(source_path)
for f in list:
  source_file_path = f.get_path()
  destination_file_path = os.path.join(destination_path, os.path.basename(source_file_path) + ".mp3")
  destination_file = factory.create_file(destination_file_path)
  AudioConversionService().convert_audio_file(f, destination_file)


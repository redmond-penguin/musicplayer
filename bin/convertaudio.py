#!/usr/bin/env python3
import sys
import os
import argparse
scriptpath = os.path.abspath(os.path.dirname(__file__))
includepath = os.path.dirname(scriptpath)
sys.path.insert(0, includepath)
from audio.audiofilefactory import AudioFileFactory
from audio.audioconversionservice import AudioConversionService

parser = argparse.ArgumentParser(description="Convert music files", epilog="File types are auto-derived from the filename extensions.")
parser.add_argument("source_file", help="The source file")
parser.add_argument("destination_file", help="The destination file")
args = parser.parse_args()
factory = AudioFileFactory()
source_file = factory.create_file(args.source_file)
destination_file = factory.create_file(args.destination_file)
AudioConversionService().convert_audio_file(source_file, destination_file)


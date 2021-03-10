#!/usr/bin/env python3
import os
import sys
import argparse
import time
import curses
import datetime
import math
import signal
import shelve
scriptpath = os.path.abspath(os.path.dirname(__file__))
includepath = os.path.dirname(scriptpath)
sys.path.insert(0, includepath)
from audio.audiofilelist import AudioFileList
from audio.persistentaudiofilefactory import PersistentAudioFileFactory
from audio.audiofile import AudioFile

def init_window():
    stdscr = curses.initscr()
    stdscr.nodelay(1)
    return stdscr

def paint_screen(stdscr, song_number):
    (y, x) = stdscr.getmaxyx()
    middle_line = y // 2
    previous_song = song_number - 1
    for line in range(middle_line - 2, -1, -1):
        stdscr.hline(line, 0, ' ', x)
        if previous_song >= 0:
            stdscr.addnstr(line, 6, list.get_file(previous_song).get_description(), x - 6)
            stdscr.addstr(line, 0, str(list.get_file(previous_song).get_play_count()))
            previous_song = previous_song - 1
    stdscr.hline(middle_line - 1, 0, '-', x)
    extension = "File type: " + f.get_extension()
    extension_length = len(extension)
    if extension_length < x:
        stdscr.addstr(middle_line - 1, x - extension_length, extension)
    stdscr.hline(middle_line, 0, ' ', x)
    stdscr.addnstr(middle_line, 6, f.get_description(), x - 6)
    stdscr.hline(middle_line + 1, 0, '-', x)
    bitrate = "Bitrate: " + str(int(f.get_bitrate()))
    bitrate_length = len(bitrate)
    if bitrate_length < x:
        stdscr.addstr(middle_line + 1, x - bitrate_length, bitrate)
    next_song = song_number + 1
    for line in range(middle_line + 2, y - 1):
        stdscr.hline(line, 0, ' ', x)
        if next_song < list_size:
            stdscr.addnstr(line, 6, list.get_file(next_song).get_description(), x - 6)
            stdscr.addstr(line, 0, str(list.get_file(next_song).get_play_count()))
            next_song = next_song + 1
    stdscr.refresh()
    return middle_line

storage = shelve.open(os.path.expanduser("~/.musicplayer_play_counts"))
list = AudioFileList(None, PersistentAudioFileFactory(storage))

parser = argparse.ArgumentParser(description="Play music files")
parser.add_argument("--noshuffle", dest="shuffle", default=True, action='store_false',
                    help="Don't shuffle the files before playing")
parser.add_argument("--repeat", dest="repeat", default=False, action='store_true',
                    help="Repeat the playlist after playing all songs. If in shuffle mode, list is reshuffled before repeating.")
parser.add_argument("path", nargs="*", default=["."], help="A file or a path to recursively scan for music files")
args = parser.parse_args()
for path in args.path:
    if os.path.isdir(path):
        list.add_path_to_list(path)
    elif os.path.isfile(path):
        list.add_file(path)
    else:
        print("Parameter " + path +  " doesn't seem to indicate a path")
        parser.print_help()

stdscr = init_window()
curses.noecho()
curses.cbreak()

line=-1
while True:
    if args.shuffle:
        list.shuffle()
    song_number=0
    list_size=list.size()
    while song_number < list_size:
        f = list.get_file(song_number)
        p = None
        pause = False
        try:
            p = f.play_song()
            start_time = datetime.datetime.today()
            previous_seconds_duration = 0
            middle_line = paint_screen(stdscr, song_number)
            stdscr.addstr(middle_line, 0, "00:00")
            stdscr.refresh()
            while p.poll() == None:
                if not pause:
                    current_time = datetime.datetime.today()
                    duration = current_time - start_time
                    seconds_duration = duration.total_seconds()
                    if seconds_duration > previous_seconds_duration:
                        formatted_duration = "{0:02n}:{1:02n}".format(seconds_duration // 60, math.floor(seconds_duration % 60))
                        stdscr.addstr(middle_line, 0, formatted_duration)
                        stdscr.refresh()
                        previous_seconds_duration = seconds_duration
                c = stdscr.getch()
                if c == ord('n'):
                    p.terminate()
                    continue
                if c == ord('r'):
                    p.terminate()
                    song_number = song_number - 1
                    continue
                if c == ord('p'):
                    if song_number > 0:
                        p.terminate()
                        song_number = song_number - 2
                        continue
                if c == ord(' '):
                    if pause:
                        p.send_signal(signal.SIGCONT)
                        pause = False
                        start_time_increase = datetime.datetime.today() - pause_start_time
                        start_time = start_time + start_time_increase
                        continue
                    else:
                        p.send_signal(signal.SIGSTOP)
                        pause = True
                        pause_start_time = datetime.datetime.today()
                        continue
                if c == curses.KEY_RESIZE:
                    stdscr = init_window()
                    middle_line = paint_screen(stdscr, song_number)
                if c == ord('x'):
                    song_number = list_size
                    p.terminate()
                    break
                time.sleep(0.25)
            song_number = song_number + 1
        except KeyboardInterrupt:
            #if p != None:
            #    p.terminate()
            try:
                song_number = song_number + 1
                time.sleep(0.5)
            except KeyboardInterrupt:
                args.repeat=False
                break
        except:
            curses.nocbreak()
            stdscr.keypad(0)
            curses.echo()
            curses.endwin()
            if p != None:
                p.terminate()
            storage.close()
            raise
    if not args.repeat:
        break
curses.nocbreak()
stdscr.keypad(0)
curses.echo()
curses.endwin()
storage.close()

# musicplayer
Linux console music player that recursively searches a directory for music files and then plays them randomly but with a preference for less often played tracks.

Just some experiments with Python, but it might be of use to someone.

## Requirements
* Python >= 3 with curses module (Linux)
* mpg123 for mp3 support
* ogg123 for ogg and flac support
* vlc for wma support

## Usage
    usage: musicplayer.py [-h] [--noshuffle] [--repeat] [path [path ...]]
    
    Play music files
    
    positional arguments:
      path         A file or a path to recursively scan for music files. If 
                   no path is provided, the currect directory is used.

    optional arguments:
      -h, --help   show this help message and exit
      --noshuffle  Don't shuffle the files before playing
      --repeat     Repeat the playlist after playing all songs. If in shuffle
                   mode, list is reshuffled before repeating.

**Warning**: the program uses a file ~/.musicplayer to keep track of song play counts. To change this file name or location, edit musicplayer.py.

## Keys
During playing, the following keys can be used:
* N - Next song
* P - Previous song
* Space - Pause playing
* X - Exit program

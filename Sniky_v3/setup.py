import sys
from cx_Freeze import setup, Executable

# Inclure les fichiers supplémentaires
include_files = [
    'backgrounds/',
    'sprites/',
    'musique_menu.mp3',
    'musique_niveau1.mp3',
    'musique_niveau2.mp3',
    'musique_niveau3.mp3',
    'musique_niveau4.mp3',
    'musique_niveau5.mp3',
    'musique_niveau6.mp3',
    'musique_niveau7.mp3',
    'musique_niveau8.mp3',
    'musique_niveau9.mp3',
    'musique_niveau10.mp3'
]

# Dépendances à inclure
build_exe_options = {
    "packages": ["pygame", "random", "time", "os"],
    "include_files": include_files
}

# Base du programme (console/GUI)
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="Sniky the Game",
    version="1.0",
    description="Sniky, the Game",
    options={"build_exe": build_exe_options},
    executables=[Executable("main.py", base=base)]
)

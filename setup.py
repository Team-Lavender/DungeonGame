import cx_Freeze
import sys
import os


base_setup = 'Win32GUI' if sys.platform == 'win32' else None
executables = [cx_Freeze.Executable("main.pyw", base = base_setup, icon='dungeongameicon.ico', targetName='CavernousDepths.exe')]

buildOptions = dict(packages = ["pygame", "configparser", "random"], include_files = [os.path.abspath("assets/'"),os.path.abspath("game_saves/"),os.path.abspath("dungeongameicon.png"),os.path.abspath("mapframe.txt"),os.path.abspath('mapframe2.txt'),os.path.abspath("mapframe3.txt") ,os.path.abspath("mapframe_tutorial.txt")])

cx_Freeze.setup(
         name = "DungeonGame",
         version = "0.1",
         options = dict(build_exe = buildOptions),
         executables = executables)
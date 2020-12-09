import cx_Freeze
import sys
base_setup = 'Win32GUI' if sys.platform == 'win32' else None
executables = [cx_Freeze.Executable("main.pyw", base = base_setup, icon='dungeongameicon.ico')]

buildOptions = dict(packages = ["pygame", "configparser", "random"], include_files = ['assets/', 'game_saves/', 'mapframe.txt', 'mapframe2.txt', 'mapframe3.txt', 'mapframe_tutorial.txt'])

cx_Freeze.setup(
         name = "DungeonGame",
         version = "0.1",
         options = dict(build_exe = buildOptions),
         executables = executables)
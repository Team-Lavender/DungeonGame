import cx_Freeze

executables = [cx_Freeze.Executable("main.py")]

buildOptions = dict(packages = ["pygame", "configparser", "random"], include_files = ['assets/', 'game_saves/', 'mapframe.txt', 'mapframe2.txt', 'mapframe3.txt'])

cx_Freeze.setup(
         name = "DungeonGame",
         version = "0.1",
         options = dict(build_exe = buildOptions),
         executables = executables)
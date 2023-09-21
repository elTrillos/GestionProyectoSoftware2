import PyInstaller.__main__
import sys

# Determine if running on Windows
is_windows = sys.platform.startswith('win')

# Define the data files to include
data_files = [("assets/*", "assets")]

# Convert the data files into the format for `--add-data`
add_data = ["--add-data={};{}".format(src, dst) if is_windows else "--add-data={}:{}".format(src, dst) for src, dst in data_files]

# Your existing options
cmd = [
    "main.py",  # your main file with ui.run()
    "--name",
    "LUDO",
    "--onefile",
    "--windowed",
    "--specpath",
    "specs",
] + add_data  # Include the `--add-data` options here

PyInstaller.__main__.run(cmd)

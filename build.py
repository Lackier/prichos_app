import os
from PyInstaller.__main__ import run as pyinstaller_run
import subprocess

# Specify the required dependencies
dependencies = ["tkcalendar", "pyinstaller"]

# Install dependencies
for dependency in dependencies:
    result = subprocess.run(["pip", "install", dependency])
    if result.returncode != 0:
        print(f"Failed to install dependency: {dependency}")
        exit(1)

main_script = "main.py"
output_dir = os.path.dirname(os.path.abspath(main_script))
exe_name = "PrichosApp.exe"  # Specify the desired name for the executable

# Run PyInstaller to create the executable
pyinstaller_args = [
    "--onefile",            # Create one executable file
    "--name", exe_name,     # Set the name of the executable file
    main_script             # Main script to build
]

try:
    pyinstaller_run(pyinstaller_args)
    print("__________________________________")
    print("Executable created successfully!!!")
except Exception as e:
    print("Failed to create executable:", e)
    exit(1)

input("Press Enter to exit...")

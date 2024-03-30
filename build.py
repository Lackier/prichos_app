import os
from PyInstaller.__main__ import run as pyinstaller_run
import subprocess

# Specify the required dependencies
dependencies = ["tkcalendar", "pyinstaller", "ttkbootstrap"]

for dependency in dependencies:
    result = subprocess.run(["pip", "install", dependency])
    if result.returncode != 0:
        print(f"Failed to install dependency: {dependency}")
        exit(1)

main_script = "main.py"
output_dir = os.path.dirname(os.path.abspath(main_script))
exe_name = "PrichosApp.exe"

language_modules = ["text_en.py", "text_es.py", "text_ru.py"]
add_data_args = [f"--add-data={module};." for module in language_modules]
pyinstaller_args = [
    "--onefile",
    "--name", exe_name,
    *add_data_args,
    main_script
]

try:
    pyinstaller_run(pyinstaller_args)
    print("__________________________________")
    print("Executable created successfully!!!")
except Exception as e:
    print("Failed to create executable:", e)
    exit(1)

input("Press Enter to exit...")

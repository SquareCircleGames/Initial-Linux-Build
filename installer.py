


import subprocess
import os
import zipfile
import time
import shutil # Almost fotgot this

GAME_URL = "https://github.com/SquareCircleGames/Initial-Linux-Build/releases/download/v1.06/Linux_Build.zip"

ZIP_NAME = "Linux-Build.zip"
EXTRACT_DIR = "ImmortalCombatSCG"
LAUNCHER_NAME = "Immortal_Combat.x86_64"

def main():
    print("--- Immortal Combat Linux Installer ---\n")
    print("You have ten (10) seconds to cancel the install with (CTRL + \\)")
    time.sleep(10)
    
    # Download
    print("Downloading game files...")
    subprocess.run(["curl", "-L", GAME_URL, "-o", ZIP_NAME], check=True)

    # Extract
    print(f"Unpacking files into ./{EXTRACT_DIR}...")
    if not os.path.exists(EXTRACT_DIR):
        os.makedirs(EXTRACT_DIR)
        
    with zipfile.ZipFile(ZIP_NAME, 'r') as zip_ref:
        zip_ref.extractall(EXTRACT_DIR)

    # This should fix that nested folder problem
    contents = os.listdir(EXTRACT_DIR)
    if len(contents) == 1 and os.path.isdir(os.path.join(EXTRACT_DIR, contents[0])):
        inner_folder = os.path.join(EXTRACT_DIR, contents[0])
        print(f"Moving files out of subfolder: {contents[0]}...")
        for item in os.listdir(inner_folder):
            shutil.move(os.path.join(inner_folder, item), os.path.join(EXTRACT_DIR, item))
        os.rmdir(inner_folder)

     # Permissions
    launcher_path = None
    for root, dirs, files in os.walk(EXTRACT_DIR):
        if LAUNCHER_NAME in files:
            launcher_path = os.path.join(root, LAUNCHER_NAME)
            break

    if launcher_path:
        print(f"Applying Linux execution permissions to: {launcher_path}")
        
        os.chmod(launcher_path, 0o755)
        print(f"\nSUCCESS! To play, run: ./{launcher_path}")
    else:
        print(f"\nWARNING: Could not find {LAUNCHER_NAME} inside the ZIP.")
        print("You may need to set permissions manually or check the filename.")

    # Cleanup
    if os.path.exists(ZIP_NAME):
        os.remove(ZIP_NAME)

main()



import os
import sys
import shutil
import subprocess
import nuitka.__main__ as nuitka_main

source_file = "main.py"
output_dir = "dist"

def ensure_dependencies():
    if not shutil.which("python3"):
        print("Python3 is not installed. Please install it first.")
        sys.exit(1)
    if not shutil.which("pip"):
        print("pip is not installed. Installing pip...")
        subprocess.run(["sudo", "apt", "update", "-qq"])
        subprocess.run(["sudo", "apt", "install", "-y", "-qq", "python3-pip"])
    try:
        subprocess.run(["python3", "-m", "nuitka", "--version"], check=True, stdout=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        print("Nuitka is not installed. Installing Nuitka...")
        subprocess.run(["pip", "install", "--quiet", "--user", "nuitka"])
    if not shutil.which("patchelf"):
        print("Installing or updating patchelf to the latest version...")
        subprocess.run(["sudo", "apt", "remove", "-y", "patchelf"])
        subprocess.run(["wget", "https://github.com/NixOS/patchelf/releases/download/0.17.0/patchelf-0.17.0.tar.gz"])
        subprocess.run(["tar", "-xzf", "patchelf-0.17.0.tar.gz"])
        os.chdir("patchelf-0.17.0")
        subprocess.run(["./configure"])
        subprocess.run(["make"])
        subprocess.run(["sudo", "make", "install"])
        os.chdir("..")
        shutil.rmtree("patchelf-0.17.0")
        os.remove("patchelf-0.17.0.tar.gz")
    if not shutil.which("ccache"):
        print("ccache is not installed. Installing ccache...")
        subprocess.run(["sudo", "apt", "update", "-qq"])
        subprocess.run(["sudo", "apt", "install", "-y", "-qq", "ccache"])

def patch_gofile():
    path="/usr/local/python/3.12.1/lib/python3.12/site-packages/gofilepy/gofile.py"
    if not os.path.isfile(path):
        print(f"File not found: {path}")
        raise FileNotFoundError(f"File not found: {path}")
    try:
        with open(path, "r") as file:
            lines = file.readlines()
        with open(path, "w") as file:
            for line in lines:
                if "raise NotImplemented" in line:
                    line = line.replace(
                        "raise NotImplemented",
                        'raise NotImplementedError("This feature is not implemented yet.")'
                    )
                file.write(line)
        print(f"Patch applied successfully to {path}")
    except Exception as e:
        print(f"Error patching file: {e}")
        raise e

def compile_to_binary():
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    sys.argv = [
        "nuitka",
        "--standalone",
        "--onefile",
        "--enable-plugin=tk-inter",
        "--follow-imports",
        "--assume-yes-for-downloads",
        f"--output-dir={output_dir}",
        source_file
    ]
    try:
        nuitka_main.main()
    except Exception as e:
        print(f"Compilation failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    ensure_dependencies()
    compile_to_binary()
    print("Compilation completed. The output is in the 'dist' directory.")

import os
import sys
import site
import glob
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
    site_packages_dirs = site.getsitepackages()
    gofile_path = None
    for dir in site_packages_dirs:
        match = glob.glob(os.path.join(dir, "gofilepy", "gofile.py"))
        if match:
            gofile_path = match[0]
            break
    if not gofile_path or not os.path.isfile(gofile_path):
        raise FileNotFoundError("Could not locate gofilepy/gofile.py in site-packages")
    print(f"Found gofile.py at: {gofile_path}")
    with open(gofile_path, "r") as file:
        lines = file.readlines()
    with open(gofile_path, "w") as file:
        for line in lines:
            if "raise NotImplemented" in line:
                line = line.replace(
                    "raise NotImplemented",
                    'raise NotImplementedError("This feature is not implemented yet.")'
                )
            file.write(line)
    print("Patch applied successfully.")

def compile_to_binary():
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    sys.argv = [
        "nuitka",
        "--standalone",
        "--onefile",
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
    patch_gofile()
    compile_to_binary()
    print("Compilation completed. The output is in the 'dist' directory.")

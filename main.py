from torrent import get_metadata, download_torrent
from output import print_full_metadata, print_primary_metadata
from validation import is_valid_magnet
from upload import upload_directory_to_gofile
import sys
import os

unattended = input("🔹 Do you want to enable unattended mode? (y/N): ").lower() == "y"
promptFullMetadata = "y" if unattended else input("🔹 Do you want the full metadata? (y/N): ")

magnetLink = input("🔹 Enter the magnet link: ")
if not is_valid_magnet(magnetLink):
    print("🔹 Invalid magnet link...")
    print("🔹 Exiting...")
    sys.exit()

print("🔹 Getting metadata...")
torrentMetadata = get_metadata(magnetLink)
isExists = torrentMetadata is not None
if promptFullMetadata.lower() == "y" and not unattended:
    if isExists:
        print_full_metadata(torrentMetadata)
    else:
        print("🔹 Cannot get metadata...")
        print("🔹 Exiting...")
        sys.exit()
else:
    if isExists:
        print_primary_metadata(torrentMetadata)
    else:
        print("🔹 Cannot get metadata...")
        print("🔹 Exiting...")
        sys.exit()

if unattended:
    print("🔹 Downloading torrent...")
    if isExists:
        pass
    else:
        print("🔹 Cannot download torrent, metadata not found...")
else:
    input("🔹 Press Enter to download the torrent...")
    if isExists:
        pass
    else:
        print("🔹 Cannot download torrent, metadata not found...")

temp_folder = "temp"
if os.path.exists(temp_folder) and os.path.isdir(temp_folder):
    print("🔹 Uploading files from the 'temp' folder...")
    uploaded_files = upload_directory_to_gofile(temp_folder, output_file="links.txt")
    if uploaded_files:
        with open('links.txt', 'r') as link_file:
            saved_results = link_file.read()
            print(saved_results)
        print(f"🔹 Upload completed. Links saved to links.txt.")
    else:
        print("🔹 No files were uploaded.")
else:
    print("🔹 'temp' folder does not exist or is not a directory.")


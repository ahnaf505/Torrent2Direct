from torrent import get_metadata
from output import print_full_metadata, print_primary_metadata
from validation import is_valid_magnet
import sys

magnetLink = input("🔹 Enter the magnet link: ")
if not is_valid_magnet(magnetLink):
    print("🔹 Invalid magnet link...")
    print("🔹 Exiting...")
    sys.exit()

print("🔹 Getting metadata...")
promptFullMetadata = input("do you want the full metadata? (y/N): ")
torrentMetadata = get_metadata(magnetLink)
isExists = torrentMetadata is not None
if promptFullMetadata.lower() == "y":
    if isExists != None:
        print_full_metadata(torrentMetadata)
    else:
        print("🔹 Cannot get metadata...")
        print("🔹 Exiting...")
        sys.exit()
else:
    if isExists != None:
        print_primary_metadata(torrentMetadata)
    else:
        print("🔹 Cannot get metadata...")
        print("🔹 Exiting...")
        sys.exit()


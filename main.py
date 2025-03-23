from torrent import get_metadata, print_full_metadata, print_primary_metadata
from validation import is_valid_magnet
import sys

magnetLink = input("🔹 Enter the magnet link: ")
if not is_valid_magnet(magnetLink):
    print("🔹 Invalid magnet link...")
    print("🔹 Exiting...")
    sys.exit()

print("🔹 Getting metadata...")
torrentMetadata = get_metadata(magnetLink)
isExists = torrentMetadata is not None
if isExists != None:
    print_primary_metadata(torrentMetadata)
else:
    print("🔹 Cannot get metadata...")
    print("🔹 Exiting...")
    sys.exit()



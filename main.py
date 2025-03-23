from torrent import get_metadata, print_full_metadata, print_primary_metadata
import sys

magnetLink = input("Enter the magnet link: ")
torrentMetadata = get_metadata(magnetLink)
isExists = torrentMetadata is not None
if isExists != None:
    print_primary_metadata(torrentMetadata)
else:
    print("Cannot get metadata...")
    print("Exiting...")
    sys.exit()

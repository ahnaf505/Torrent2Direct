def print_full_metadata(torrent_info):
    """Print all available metadata from a torrent."""
    print("\n🔹 **Torrent General Info**")
    print("🔹 Torrent Name:", torrent_info.name())
    print("🔹 Total Size:", torrent_info.total_size(), "bytes")
    print("🔹 Number of Files:", torrent_info.num_files())
    print("🔹 Info Hash:", torrent_info.info_hash())
    
    print("\n🔹 **Files in Torrent**")
    files = torrent_info.files()
    for index, file in enumerate(files):
        print(f"🔹 {index+1}. {file.path} ({file.size} bytes)")
    print("\n🔹 **Piece Information**")
    
    print("🔹 Piece Length:", torrent_info.piece_length(), "bytes")
    print("🔹 Number of Pieces:", torrent_info.num_pieces())
    print("🔹 Total Pieces Size:", torrent_info.num_pieces() * torrent_info.piece_length(), "bytes")

    print("\n🔹 **Other Metadata**")
    print("🔹 Private Torrent:", torrent_info.priv())
    print("🔹 Creation Date:", torrent_info.creation_date())
    print("🔹 Comment:", torrent_info.comment())
    print("🔹 Creator:", torrent_info.creator())

def print_primary_metadata(torrent_info):
    """Print only the primary metadata from a torrent."""
    print("\n🔹 **Torrent General Info**")
    print("🔹 Torrent Name:", torrent_info.name())
    print("🔹 Total Size:", torrent_info.total_size(), "bytes")
    print("🔹 Info Hash:", torrent_info.info_hash())


import libtorrent as lt
import time

def get_metadata(magnet_link, timeout=30):
    ses = lt.session()
    params = {
        'save_path': '.',
        'storage_mode': lt.storage_mode_t(2)
    }
    handle = lt.add_magnet_uri(ses, magnet_link, params)
    start_time = time.time()
    
    while not handle.has_metadata():
        time.sleep(1)
        if time.time() - start_time > timeout:
            return None

    torrent_info = handle.get_torrent_info()
    return torrent_info

def download_torrent(torrent_info, save_path='./temp/'):
    ses = lt.session()
    ses.set_upload_rate_limit(0)  # Disable uploading
    params = {
        'save_path': save_path,
        'storage_mode': lt.storage_mode_t(2),
        'ti': torrent_info
    }
    handle = ses.add_torrent(params)

    while not handle.is_seed():
        s = handle.status()
        print(f"Progress: {s.progress * 100:.2f}%")  # Print only progress
        time.sleep(1)

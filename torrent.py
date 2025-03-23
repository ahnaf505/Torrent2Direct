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

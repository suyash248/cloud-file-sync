from threading import Thread
import os
from core.download import Downloader
from lib.watcher import watch
from etc.conf import settings

def create_local_sync_dir():
    import os
    if not os.path.exists(settings.LOCAL_SYNC_LOCATION):
        print "[SYNC_LOC] Going to create local sync directory %s" %settings.LOCAL_SYNC_LOCATION
        os.makedirs(settings.LOCAL_SYNC_LOCATION)

def sync():
    create_local_sync_dir()
    download_sync_thread = Thread(target=Downloader.download_and_sync)
    download_sync_thread.start()
    download_sync_thread.join()

    watcher_sync_thread = Thread(target=watch)
    watcher_sync_thread.start()
    watcher_sync_thread.join()

if __name__ == '__main__':
    sync()
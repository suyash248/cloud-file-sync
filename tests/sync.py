from threading import Thread
from core.download import Downloader
from lib.watcher import watch

def sync():
    download_sync_thread = Thread(target=Downloader.download_and_sync)
    download_sync_thread.start()
    download_sync_thread.join()

    watcher_sync_thread = Thread(target=watch)
    watcher_sync_thread.start()
    watcher_sync_thread.join()

if __name__ == '__main__':
    sync()
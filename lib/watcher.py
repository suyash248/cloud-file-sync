import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from etc.conf import settings
from core.upload import Uploader
from core.delete import delete_file

class Watcher:
    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, settings.LOCAL_SYNC_LOCATION, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(settings.UPLOAD_AND_SYNC_DURATION)
        except:
            self.observer.stop()
            print "[ERROR] Watcher... stopped watching for further changes"

        self.observer.join()


class Handler(FileSystemEventHandler):
    @staticmethod
    def on_any_event(event):
        #print "[DEBUG] Received %s event - %s, is_dir - %s" % (event.event_type, event.src_path, event.is_directory)
        if event.is_directory:
            return None

        if event.event_type == 'deleted' or event.event_type == 'moved':
            delete_file(event.src_path)
        else:
            Uploader().lazy_upload_recursively()

def watch():
    print "[INFO] Watcher... started watching changes in directory {watch_dir} every {watch_duration} second(s)" \
        .format(watch_dir=settings.LOCAL_SYNC_LOCATION, watch_duration=settings.UPLOAD_AND_SYNC_DURATION)
    w = Watcher()
    w.run()

if __name__ == '__main__':
    watch()
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from database import Conn
# credits
# https://michaelcho.me/article/using-pythons-watchdog-to-monitor-changes-to-a-directory

class Watcher:
    DIRECTORY_TO_WATCH = "/home/petry/sambashare"

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print( "Error")

        self.observer.join()

class Handler(FileSystemEventHandler):
        
    @staticmethod
    def on_any_event(event):
        db = Conn()
        if event.is_directory:
            return None

        elif event.event_type == 'created':
            # Take any action here when a file is first created.
            print( "created - %s." % event.src_path)
            db.save(event.src_path)

        elif event.event_type == 'moved':
            # Taken any action here when a file is modified.
            print ("moved - %s to %s" % (event.src_path, event.dest_path))
            db.update(event.src_path, event.dest_path)

        elif event.event_type == 'deleted':
            # Taken any action here when a file is modified.
            print ("deleted - %s." % event.src_path)
            db.delete(event.src_path)

        elif event.event_type == 'renamed':
            # Taken any action here when a file is modified.
            print ("deleted - %s." % event.src_path)
            db.update(event.src_path, event.dest_path)

        # else:
        #     print("received not handled event type: %s" % event.event_type )

if __name__ == '__main__':
    w = Watcher()
    w.run()

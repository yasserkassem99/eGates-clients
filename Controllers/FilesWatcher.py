import sys
import time
import os
from watchdog.observers import Observer
from watchdog.events import RegexMatchingEventHandler

class PdfEventHandler(RegexMatchingEventHandler):
    PDF_REGEX = [r"^.+\.(([pP][dD][fF]))$"]

    def __init__(self):
        super().__init__(self.PDF_REGEX)

    def on_created(self, event):
        self.process(event)
        
    def on_deleted(self, event):
        print('pdf file deleted')

    def process(self, event):
        filename, ext = os.path.splitext(event.src_path)
        filename = f"{filename}.pdf"
        print(filename,'created')
        os.system(f"lpr -P Canon_MF633C_635C {filename}")




class FilesWatcher:
    def __init__(self, src_path):
        self.__src_path = src_path
        self.__event_handler = PdfEventHandler()
        self.__event_observer = Observer()
        self.run()
    def run(self):
        self.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()

    def start(self):
        self.__schedule()
        self.__event_observer.start()

    def stop(self):
        self.__event_observer.stop()
        self.__event_observer.join()

    def __schedule(self):
        self.__event_observer.schedule(
            self.__event_handler,
            self.__src_path,
            recursive=True
        )
        
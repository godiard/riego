# jobs management
import schedule
import time

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from irrigation import IrrigationManager, CONFIG_FILE_NAME

irrigation_manager = IrrigationManager(enable_schedule=True)

event_handler = FileSystemEventHandler()
event_handler.on_modified = irrigation_manager.update_config

observer = Observer()
observer.schedule(event_handler, CONFIG_FILE_NAME, recursive=False)
observer.start()
try:
    while True:
        schedule.run_pending()
        time.sleep(30)  # wait 30 seconds
except KeyboardInterrupt:
    observer.stop()
observer.join()

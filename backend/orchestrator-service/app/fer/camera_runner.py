import threading
from app.fer.detector import start_camera_loop

_camera_thread = None
_stop_event = threading.Event()

def start_fer():
    global _camera_thread
    _stop_event.clear()
    if _camera_thread is None or not _camera_thread.is_alive():
        _camera_thread = threading.Thread(
            target=start_camera_loop,
            args=(_stop_event,),
            daemon=True
        )
        _camera_thread.start()

def stop_fer():
    _stop_event.set()

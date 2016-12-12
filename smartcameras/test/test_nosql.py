import threading
import time
from smartcameras.nosqlconsumer import TableConsumer
from smartcameras.speedcamera import SpeedCamera

def test_simple():
    table = TableConsumer()
    threadConsumer = threading.Thread(target=table.activate)
    threadConsumer.daemon = True
    threadConsumer.start()

    camera = SpeedCamera("Blandford Square", "Newcastle")
    threadProducer = threading.Thread(target=camera.activate, args=(50, 5))
    threadProducer.daemon = True
    threadProducer.start()

    time.sleep(5)

    camera.deactivate()
    threadProducer.join()

    table.terminate()
    threadConsumer.join()

import threading
import time
import pytest
from smartcameras.storagehandler import CameraRegister
from smartcameras.speedcamera import SpeedCamera

def test_camera_register():
    cameraRegister = CameraRegister()
    threadConsumer = threading.Thread(target=cameraRegister.activate)
    threadConsumer.daemon = True
    threadConsumer.start()

    cameraRegister.flushTable()

    camera = SpeedCamera("Dragao", "Porto")
    threadProducer = threading.Thread(target=camera.activate, args=(50, 5))
    threadProducer.daemon = True
    threadProducer.start()

    time.sleep(5)

    camera.deactivate()
    threadProducer.join()

    cameraRegister.terminate()
    threadConsumer.join()

    entities = cameraRegister.retrieveAllEntities()
    assert len(entities) > 0    

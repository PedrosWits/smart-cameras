import threading
import time
import pytest
from smartcameras.storagehandler import CameraRegister, PoliceMonitor
from smartcameras.speedcamera import SpeedCamera

def test_camera_register():
    cameraRegister = CameraRegister()
    threadConsumer = threading.Thread(target=cameraRegister.activate)
    threadConsumer.daemon = True
    threadConsumer.start()

    cameraRegister.flushPartition(CameraRegister.PARTITION_ACTIVATION)

    camera = SpeedCamera("Dragao", "Porto")
    threadProducer = threading.Thread(target=camera.activate, args=(50, 5))
    threadProducer.daemon = True
    threadProducer.start()

    time.sleep(5)

    camera.deactivate()
    threadProducer.join()

    cameraRegister.terminate()
    threadConsumer.join()

    entities = cameraRegister.retrieveAllActivations()
    assert len(entities) > 0

def test_police_monitor():
    policeMonitor = PoliceMonitor()
    threadConsumer = threading.Thread(target=policeMonitor.activate)
    threadConsumer.daemon = True
    threadConsumer.start()

    policeMonitor.flushPartition(PoliceMonitor.PARTITION)

    camera = SpeedCamera("Bomba Galp", "Porto")
    threadProducer = threading.Thread(target=camera.activate, args=(50, 15))
    threadProducer.daemon = True
    threadProducer.start()

    time.sleep(5)

    camera.deactivate()
    threadProducer.join()

    policeMonitor.terminate()
    threadConsumer.join()

    entities = policeMonitor.retrievePrioritySightings()
    assert len(entities) > 0

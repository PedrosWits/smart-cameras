import threading
from smartcameras.speedcamera import SpeedCamera
import smartcameras.speedcamera as speedcamera
import time

def test_constructor():
    camera = SpeedCamera("Blandford Square", "Newcastle")
    assert camera.street == "Blandford Square"
    assert camera.city == "Newcastle"

def test_uuids():
    camera1 = SpeedCamera("Blandford Square", "Newcastle")
    camera2 = SpeedCamera("Blandford Square", "Newcastle")
    assert camera1.id != camera2.id

def test_relocate():
    camera = SpeedCamera("Blandford Square", "Newcastle")
    camera.relocate("St. James Avenue")
    assert camera.street == "St. James Avenue"
    camera.relocate("Campo Alegre", "Porto")
    assert camera.street == "Campo Alegre"
    assert camera.city == "Porto"

def test_activity_with_threads():
    camera = SpeedCamera("Blandford Square", "Newcastle")
    t = threading.Thread(target=camera.activate, args=(50, 5))
    t.start()
    time.sleep(5)
    assert camera.isActive == True
    # print(camera.toJson())
    camera.deactivate()
    t.join()
    assert camera.isActive == False
    # print(camera.toJson())

# def test_pub_sub():
#     camera = SpeedCamera("Blandford Square", "Newcastle")
#     thread = speedcamera.activateInNewThread(camera, 50, 5)
    

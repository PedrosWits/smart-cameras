import threading
from smartcameras.speedcamera import SpeedCamera
import smartcameras.speedcamera as speedcamera
import time
import json

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
    camera = SpeedCamera("Queens Road", "Manchester")
    t = threading.Thread(target=camera.activate, args=(50, 5))
    t.start()
    time.sleep(5)
    assert camera.isActive
    #print(camera.toJson())
    camera.deactivate()
    t.join()
    assert not camera.isActive
    #print(camera.toJson())

def test_constants():
    assert SpeedCamera.TOPIC == "speedcamera"

def test_pub_sub():
    test_subscription = "TEST_PUB_SUB"
    camera = SpeedCamera("Big Ben", "London")

    camera.cloudhook.serviceBus.delete_subscription(SpeedCamera.TOPIC, test_subscription)

    camera.cloudhook.subscribe(SpeedCamera.TOPIC, test_subscription)

    thread = speedcamera.activateInNewThread(camera, 50, 1)
    assert camera.isActive

    camera_msg = camera.cloudhook.getMessage(SpeedCamera.TOPIC, test_subscription, timeout='5')
    assert json.loads(camera_msg.body)['event'] == SpeedCamera.EVENT_ACTIVATION

    msg_dict_values = json.loads(camera_msg.body)['camera'].values()
    assert camera.id in msg_dict_values
    assert camera.city in msg_dict_values
    assert camera.street in msg_dict_values
    assert camera.rate in msg_dict_values
    assert camera.speedLimit in msg_dict_values
    # print(camera_msg.body)

    vehicle_msg = camera.cloudhook.getMessage(SpeedCamera.TOPIC, test_subscription, timeout='5')
    assert json.loads(vehicle_msg.body)['event'] == SpeedCamera.EVENT_VEHICLE

    assert 'camera' in vehicle_msg.body
    assert 'vehicle' in vehicle_msg.body
    msg_camera_dict_values = json.loads(vehicle_msg.body)['camera'].values()
    msg_vehicle_dict_keys = json.loads(vehicle_msg.body)['vehicle'].keys()
    assert camera.id in msg_camera_dict_values
    assert camera.city in msg_camera_dict_values
    assert camera.street in msg_camera_dict_values
    assert camera.rate in msg_camera_dict_values
    assert camera.speedLimit in msg_camera_dict_values
    assert "plate" in msg_vehicle_dict_keys
    assert "speed" in msg_vehicle_dict_keys
    assert "type" in msg_vehicle_dict_keys
    # print(vehicle_msg.body)

    camera.deactivate()
    thread.join()
    assert not camera.isActive

    camera.cloudhook.serviceBus.delete_subscription(SpeedCamera.TOPIC, test_subscription)

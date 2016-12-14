import threading
from speedcamera import SpeedCamera

class CameraManager(object):

    def __init__(self):
        self.cameras = {}
        self.threads = {}

    # Terminate camera manager (from a different process)
    def clear(self):
        # Receive terminate message on zmq
        for camera in self.cameras.itervalues():
            self.remove(camera.uuid, force=True)

    # Add a camera
    def add(self, camera):
        if cameras.getByName(camera.name) is not None:
            raise ValueError("There is already a camera with name '%s'. Please rename and try again." % camera.name)
        self.cameras[camera.id] = camera

    def getIds(self):
        return self.cameras.keys()

    def get(self, uuid):
        return self.cameras[uuid]

    def getByName(self, name):
        for camera in cameras.itervalues():
            if(camera.name == name):
                return camera
        return None

    def activate(self, uuid, speedLimit, rate):
        return self.__activate(getById(uuid), speedLimit, rate)

    def activateByName(self, name, speedLimit, rate):
        camera = getByName(name)
        if camera is not None:
            return self.__activate(camera, speedLimit, rate)
        else:
            raise ValueError("Camera with given name does not exist: %s" % name)

    def __activate(self, camera, speedLimit, rate):
        thread = threading.Thread(target=camera.activate, args=(speedLimit, rate))
        thread.daemon = True
        thread.start()
        self.threads[camera.uuid] = thread
        return thread.isAlive

    def deactivateByName(self, name):
        camera = getByName(name)
        if camera is not None:
            return self.deactivate(camera.uuid)
        else:
            raise ValueError("Camera with given name does not exist: %s" % name)

    def deactivate(self, uuid, timeout=3):
        camera = self.get(uuid)
        if not camera.isActive:
            raise ValueError("Given camera is not active.")
        thread = self.threads[uuid]
        camera.deactivate()
        thread.join(timeout)
        del self.threads[uuid]
        return not camera.isActive

    def remove(self, uuid, force=False):
        camera = self.get(uuid)
        if camera.isActive and not force:
            raise ValueError("Camera is still active. Deactivate first.")
        elif camera.isActive:
            self.deactivate(uuid)
        del self.cameras[uuid]

    def removeByName(self, name):
        camera = getByName(name)
        if camera is not None:
            return self.remove(camera.uuid)
        else:
            raise ValueError("Camera with given name does not exist: %s" % name)

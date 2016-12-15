 #! /usr/bin/env python

from smartcameras.storagehandler import CameraRegister
import threading

def main():
    print("########################################")
    print ""
    print("Welcome to the Camera Monitor!")
    print ""
    print("########################################")

    cameraRegister = CameraRegister()
    cameraRegister.dump = True
    thread = threading.Thread(target=cameraRegister.activate)
    thread.daemon = True
    thread.start()
    print ""
    print("The Camera Monitor has been activated!")
    print ""

    while True:
        try:
            raw_input("Press Ctrl+D to exit.")
        except EOFError:
            print ""
            break

    cameraRegister.terminate()
    thread.join()
    print "Camera Monitor terminated."
    print "Closing..."

if __name__ == "__main__":
    main()

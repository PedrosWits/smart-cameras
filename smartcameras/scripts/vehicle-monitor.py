 #! /usr/bin/env python

from smartcameras.storagehandler import VehicleRegister
import threading

def main():
    print("########################################")
    print ""
    print("Welcome to the Vehicle Monitor!")
    print ""
    print("########################################")

    vehicleRegister = VehicleRegister()
    vehicleRegister.dump = True
    thread = threading.Thread(target=vehicleRegister.activate)
    thread.daemon = True
    thread.start()
    print ""
    print("The Vehicle Monitor has been activated!")
    print ""

    while True:
        try:
            raw_input("Press Ctrl+D to exit.")
        except EOFError:
            print ""
            break

    vehicleRegister.terminate()
    thread.join()
    print "Vehicle Monitor terminated."
    print "Closing..."

if __name__ == "__main__":
    main()

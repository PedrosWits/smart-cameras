 #! /usr/bin/env python

from smartcameras.subscriber import VehicleInspector
import threading

def main():
    print("########################################")
    print ""
    print("Welcome to the Vehicle Inspector!")
    print ""
    print("########################################")

    vehicleInspector = VehicleInspector()
    thread = threading.Thread(target=vehicleInspector.activate)
    thread.daemon = True
    thread.start()
    print ""
    print("The Vehicle Inspector has been activated!")
    print ""

    while True:
        try:
            raw_input("Press Ctrl+D to exit.")
        except EOFError:
            print ""
            break

    vehicleInspector.terminate()
    thread.join()
    print "Vehicle Inspector terminated."
    print "Closing..."

if __name__ == "__main__":
    main()

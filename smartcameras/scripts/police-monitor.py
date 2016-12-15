 #! /usr/bin/env python

from smartcameras.storagehandler import PoliceMonitor
import threading

def main():
    print("########################################")
    print ""
    print("Welcome to the Police Monitor!")
    print ""
    print("########################################")

    policeMonitor = PoliceMonitor()
    policeMonitor.dump = True
    thread = threading.Thread(target=policeMonitor.activate)
    thread.daemon = True
    thread.start()
    print ""
    print("The Police Monitor has been activated!")
    print ""

    while True:
        try:
            raw_input("Press Ctrl+D to exit.")
        except EOFError:
            print ""
            break

    policeMonitor.terminate()
    thread.join()
    print "Police Monitor terminated."
    print "Closing..."

if __name__ == "__main__":
    main()

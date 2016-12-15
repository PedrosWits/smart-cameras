 #! /usr/bin/env python

from smartcameras.speedcamera import SpeedCamera
import threading

def main():
    print("########################################")
    print ""
    print("You have ordered a new speed camera!")
    print("We need some details before activating it:")
    print ""
    print("########################################")
    street = raw_input('Please enter the street: ')
    city = raw_input('Please enter the city: ')
    speedLimit = 0
    while speedLimit < 30:
        speedLimit = raw_input('Please enter the speed limit (>= 30): [50]' )
        if speedLimit == "":
            speedLimit = 50
            break
        else:
            try:
                speedLimit = int(speedLimit)
            except ValueError:
                speedLimit = 0
                print "FAILED: Value must be an integer!"

    rate = 0
    while rate <= 0:
        rate = raw_input('Please enter the mean num of sightings per second (>0): [5] ')
        if rate == "":
            rate = 5
            break
        else:
            try:
                rate = float(rate)
            except ValueError:
                rate = 0
                print "FAILED: Value must be a float!"

    print("########################################")
    print ""
    print("Thanks! The camera is now being activated!")
    print ""
    print("########################################")
    print ""

    camera = SpeedCamera(street, city)
    thread = threading.Thread(target=camera.activate, args=(speedLimit, rate))
    thread.daemon = True
    thread.start()
    while not camera.isActive:
        time.sleep(1)
    print("The camera is now active!")
    print ""
    usage = '''
    Operate on the camera (type on the terminal one of the following commands):

        help        - prompt this message
        print       - print camera details
        relocate    - move the camera to a new street (and city)
        restart     - restart the camera with a new speed limit
        exit        - deactivate the camera and terminate
    '''
    print(usage)
    while True:
        todo = raw_input("----> ")
        if todo == 'relocate':
            newStreet = raw_input("New street: ")
            newCity = raw_input("New city: [same] ") or None
            camera.relocate(newStreet, newCity)
            print("Camera relocated! Operating on %s at %s" % (camera.street, camera.city))

        elif todo == 'restart':
            newLimit = 0
            while newLimit < 30:
                newLimit = raw_input('Please enter the speed limit (>= 30): [50] ')
                if newLimit == "":
                    newLimit = 50
                    break
                else:
                    try:
                        newLimit = int(newLimit)
                    except ValueError:
                        newLimit = 0
                        print "FAILED: Value must be an integer!"

            print "..."
            camera.deactivate()
            thread.join()
            thread = threading.Thread(target=camera.activate, args=(newLimit, rate))
            thread.daemon = True
            thread.start()
            print "Camera restarted!"

        elif todo == 'exit':
            break
        elif todo == 'print':
            print(camera.toJson())
        elif todo == '':
            continue
        else:
            print(usage)

    camera.deactivate()
    thread.join()
    print "Camera deactivated."
    print "Closing..."

if __name__ == "__main__":
    main()

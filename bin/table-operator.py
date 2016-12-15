 #! /usr/bin/env python

from smartcameras.storagehandler import CameraRegister, VehicleRegister, PoliceMonitor
import sys

def main():
    print("########################################")
    print ""
    print("Welcome to the Table Operator!")
    print ""
    print("########################################")
    print ""

    tableName = raw_input('Please state the name of the table: ')
    handler = None
    if tableName == CameraRegister.TABLE:
        handler = CameraRegister()
    elif tableName == VehicleRegister.TABLE:
        handler = VehicleRegister()
    elif tableName == PoliceMonitor.TABLE:
        handler = PoliceMonitor()
    else:
        print("No such table.")
        print("We support one of the following tables:")
        print("  %s" % CameraRegister.TABLE)
        print("  %s" % VehicleRegister.TABLE)
        print("  %s" % PoliceMonitor.TABLE)
        sys.exit(1)

    usage = '''
    Choose one of the following operations (type on the terminal one of the following commands):

        help          - print this usage
        flush         - flush the table (or a given partition if more than 1 partition exists)
        retrieve-all  - retrieve the entire table (or a given partition if more than 1 partition exists)
        query         - run your own query
        exit
    '''
    print(usage)
    while True:
        todo = raw_input("----> ")
        if todo == "flush" or todo == "retrieve-all":
            partitionName = raw_input("Partition Name: [%s] " % handler.partitions[0])
            if partitionName == "":
                partitionName = handler.partitions[0]
            elif partitionName not in handler.partitions:
                print "No such partition"
                continue
        if todo == "flush":
            handler.flushPartition(partitionName)
        elif todo == "retrieve-all":
            entities = handler.retrievePartition(partitionName)
            print ("%d total entities found!" % len(entities))
            print ""
            printThem = raw_input("Print? [y/n] ")
            if printThem == 'y':
                for entity in entities:
                    print(entity)
        elif todo == "query":
            queryString = raw_input("Query: ")
            entities = handler.queryTable(queryString)
            try:
                print ("%d total entities found!" % len(entities))
                print ""
                printThem = raw_input("Print? [y/n] ")
                if printThem == 'y':
                    for entity in entities:
                        print(entity)
            except Exception:
                print "Bad query"
        elif todo == 'exit':
            break
        elif todo == '':
            continue
        else:
            print(usage)


if __name__ == "__main__":
    main()

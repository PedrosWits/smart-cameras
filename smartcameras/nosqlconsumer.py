from speedcamera import SpeedCamera
import azurehook
import threading
import json
import math
from azure.storage.table import TableService, Entity

class TableBuilder(object):
    SUBSCRIPTION = "NOSQL_CONSUMER"
    TABLE_VEHICLE = "Vehicle"
    TABLE_CAMERA = "Camera"

    def __init__(self, table_cred = None):
        if table_cred is None:
            table_cred = azurehook.table_cred
        self.table = TableService(account_name=table_cred['account_name'],
                                  account_key=table_cred['mykey'])
        self.table.create_table(self.TABLE_VEHICLE)
        self.table.create_table(self.TABLE_CAMERA)
        self.azure = azurehook.AzureHook()

    def activate(self, timeout = 2):
        self.azure.subscribe(SpeedCamera.TOPIC, self.SUBSCRIPTION)
        self.isActive = True
        self.nextCheck = threading.Event()
        retries = 0
        while self.isActive:
            message = self.azure.getMessage(SpeedCamera.TOPIC,
                                            self.SUBSCRIPTION,
                                            timeout=timeout)
            if message is None:
                retries += 1
            else:
                body = json.loads(message.body)
                event = body['event']
                if event == SpeedCamera.EVENT_VEHICLE:
                    self.__insertVehicle(body)
                else:
                    self.__insertCamera(body)
                retries = 0
            self.nextCheck.wait(self.__nextTimeout(retries))

    def terminate(self):
        self.isActive = False
        self.nextCheck.set()

    def flushTable(self, tableName):
        self.table.delete_table(tableName)
        self.table.create_table(tableName)


    # Initially Amortized exponential backoff:
    # Given by the formula: timeout(seconds) = (2^ntries / 10)
    def __nextTimeout(self, ntries, maxNtries = 12):
        # Define maximum timeout
        if(ntries > maxNtries):
            ntries = maxNtries
        # if ntries == 0 -> timeout = 0.100 ms
        # if ntries == 12 -> timeout = 6.66 min
        return math.pow(2, ntries) / 10.

    # Design Considerations:
    #   What kind of queries are we performing on these tables?
    #
    #   Remember: The partition key and rowkey have a unique combination
    #   and are indexed together to create a combined index for fast look-ups
    #
    #   Performance of queries (best to worst):
    #       1. Point query (known both partition and row keys)
    #       2. Range query (known partition key and filter on a range of rowkey values)
    #       3. Partition Scan (known partition key and filter on another non-key property)
    #       4. Table Scan (unknown partition key - very inneficcient - even if u know rowkey)
    #
    # Taken from: https://docs.microsoft.com/en-us/azure/storage/storage-table-design-guide

    # Can query all activity of vehicle by partition key - assume plate is unique
    # Row key is timestamp again as no vehicle can be in the two places at the same time
    # and hence get registered by two different cameras at the same time
    # Row key cannot be camera id because then we could only have one sighting per camera instead
    # of having multiple sightings of the same vehicle from the same camera
    def __insertVehicle(self, dic):
        entity = Entity()
        entity.PartitionKey = dic['vehicle']['plate']
        entity.RowKey = str(dic['camera']['timestamp'])
        entity.event = dic['event']
        entity.camera = dic['camera']['id']
        entity.speed = dic['vehicle']['speed']
        # Compact json encoding (can be later decoded into dictionary)
        entity.json = json.dumps(dic, separators=(',',':'),
                                 sort_keys=False)
        # Insert to appropriate table
        self.table.insert_entity(self.TABLE_VEHICLE, entity)

    # Can query both camera activations and deactivations by partition key
    # Would like to have auto incrementing row key but there is no such thing in table storage
    # therefore we assume that - no two vehicles go through a camera at exactly the same time
    def __insertCamera(self, dic):
        entity = Entity()
        entity.PartitionKey = dic['event']
        entity.RowKey = str(dic['camera']['timestamp'])
        entity.id = dic['camera']['id']
        # Compact json encoding (can be later decoded into dictionary)
        entity.json = json.dumps(dic, separators=(',',':'),
                                 sort_keys=False)
        # Insert to appropriate table
        self.table.insert_entity(self.TABLE_CAMERA, entity)

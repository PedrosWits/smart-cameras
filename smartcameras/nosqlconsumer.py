from speedcamera import SpeedCamera
import azurehook
import threading
from azure.storage.table import TableService

class TableConsumer(object):
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
                                            Self.SUBSCRIPTION,
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
            nextCheck.wait(self.__nextTimeout())

    def terminate(self):
        self.isActive = False
        self.nextCheck.set()

    # Initially Amortized exponential backoff:
    # Given by the formula: timeout(seconds) = (2^ntries / 10)
    def __nextTimeout(self, ntries, maxNtries = 12):
        # Define maximum timeout
        if(ntries > maxNtries):
            ntries = maxNtries
        # if ntries == 0 -> timeout = 0.100 ms
        # if ntries == 12 -> timeout = 6.66 min
        return Math.pow(2, ntries) / 10.

    def __insertVehicle(self, dic):
        dic['PartitionKey'] = dic['vehicle']['plate']
        dic['RowKey'] = dic['camera']['uuid']
        self.table.insert_entity(self.TABLE_VEHICLE, dic)

    def __insertCamera(self, dic):
        dic['PartitionKey'] = dic['camera']['uuid']
        dic['RowKey'] = dic['camera']['timestamp']
        self.table.insert_entity(self.TABLE_CAMERA, dic)

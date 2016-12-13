from abc import ABCMeta, abstractmethod
from azure.storage.table import TableService, Entity
from azure.servicebus import Rule
from speedcamera import SpeedCamera
import azurehook
import json
import subscriber

## A Generic Class that Subscribes to a Topic
class PersistentSubscriber(subscriber.AzureSubscriber):
    __metaclass__ = ABCMeta

    def __init__(self, tableName, topicName, subscriptionName,
                       ruleName = None, rule = None, table_cred = None):
        # Call super class constructor
        subscriber.AzureSubscriber.__init__(self, topicName, subscriptionName, ruleName, rule)
        # Table Service and operations
        self.tableName = tableName
        if table_cred is None:
            table_cred = azurehook.table_cred
        self.table = TableService(account_name=table_cred['account_name'],
                                  account_key=table_cred['mykey'])
        if not self.table.exists(tableName):
            self.table.create_table(tableName)

    def flushTable(self):
        if not self.table.exists(self.tableName):
            raise ValueError("Given table does not exist")
        entities = self.retrieveAllEntities()
        for entity in entities:
            self.table.delete_entity(self.tableName,
                                     entity.PartitionKey,
                                     entity.RowKey)

    def onNewMessage(self, dic):
        entity = self.dictToEntity(dic)
        # print("INSERT CAMERA IN TABLE")
        self.table.insert_entity(self.tableName, entity)

    @abstractmethod
    def retrieveAllEntities(self):
        pass

    @abstractmethod
    def dictToEntity(self, dic):
        pass

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

## Class for persisting camera registrations (activations + deactivations)
class CameraRegister(PersistentSubscriber):
    TABLE = "Camera"
    def __init__(self, table_cred = None):
        rule = Rule()
        rule.filter_type = 'SqlFilter'
        rule.filter_expression = "event = '%s' OR event = '%s'" % (SpeedCamera.EVENT_ACTIVATION, SpeedCamera.EVENT_DEACTIVATION)
        # Call super class constructor
        PersistentSubscriber.__init__(self, self.TABLE,
                                      SpeedCamera.TOPIC, "CameraRegister",
                                      "CameraRegisterRule", rule)

    # Reference:
    # http://stackoverflow.com/questions/28019437/python-querying-all-rows-of-azure-table
    # Azure limitation: only a maximum of 1000 entities can be retrieved per query
    def retrieveAllEntities(self):
        if not self.table.exists(self.TABLE):
            raise ValueError('Table %s does not exist', self.TABLE)
        # hasRows = True
        marker = None
        cameras = []
        entities = self.table.query_entities(
                        self.TABLE,
                        "PartitionKey eq '%s'" % SpeedCamera.EVENT_ACTIVATION,
                        marker = marker,
                        num_results=1000)
        for entity in entities:
            cameras.append(entity)

        return cameras

    # Can query both camera activations and deactivations by partition key
    # Would like to have auto incrementing row key but there is no such thing in table storage
    # therefore we assume that - no two vehicles go through a camera at exactly the same time
    def dictToEntity(self, dic):
        entity = Entity()
        entity.PartitionKey = dic['event']
        entity.RowKey = str(dic['camera']['timestamp'])
        entity.id = dic['camera']['id']
        # Compact json encoding (can be later decoded into dictionary)
        entity.json = json.dumps(dic, separators=(',',':'),
                                 sort_keys=False)
        return entity

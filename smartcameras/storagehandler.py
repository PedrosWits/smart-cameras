from abc import ABCMeta, abstractmethod
from azure.storage.table import TableService, Entity
from azure.servicebus import Rule
from speedcamera import SpeedCamera
import azurehook
import json
import subscriber

################################################################################
################################################################################
#
#     A Generic Class responsible for handling and persisting data obtained
#     through an Azure subscription
#
################################################################################
################################################################################
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
        self.dump = False

    # Specify behavior on message received (from subscription).
    # Default is insert entity.
    def onNewMessage(self, dic):
        entity = self.dictToEntity(dic)
        # print("INSERT CAMERA IN TABLE")
        self.table.insert_entity(self.tableName, entity)

    # Wrapper function for querying the table
    # Azure limitation: only a maximum of 1000 entities can be retrieved per query
    #
    # Reference:
    # http://stackoverflow.com/questions/28019437/python-querying-all-rows-of-azure-table
    def queryTable(self, query_string):
        if not self.table.exists(self.TABLE):
            raise ValueError('Table %s does not exist', self.TABLE)
        # hasRows = True
        marker = None
        results = []
        entities = self.table.query_entities(
                        self.TABLE,
                        query_string,
                        marker = marker,
                        num_results=1000)
        for entity in entities:
            results.append(entity)
        return results

    # Retrieve all entities from a given partition (i.e. that match a given partitionkey)
    def retrievePartition(self, partitionKey):
        return self.queryTable("PartitionKey eq '%s'" % partitionKey);

    # Flush all entities from a given partition (i.e. that match a given partitionkey)
    def flushPartition(self, partitionKey):
        if not self.table.exists(self.tableName):
            raise ValueError("Given table does not exist")
        entities = self.retrievePartition(partitionKey)
        for entity in entities:
            self.table.delete_entity(self.tableName,
                                     entity.PartitionKey,
                                     entity.RowKey)

    # To be implemented by child classes: return an entity given the body
    # of the message (as a dictionary).
    @abstractmethod
    def dictToEntity(self, dic):
        pass

################################################################################
################################################################################
#
#    Design Considerations (Choosing values for Partition and Row keys)
#
################################################################################
################################################################################
#
#
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


################################################################################
################################################################################
#
#     Class responsible for handling and persisting camera activity
#
################################################################################
################################################################################

class CameraRegister(PersistentSubscriber):
    TABLE = "Cameras"
    PARTITION_ACTIVATION = "CameraActivation"
    PARTITION_DEACTIVATION = "CameraDeactivation"
    partitions = [PARTITION_ACTIVATION, PARTITION_DEACTIVATION]

    def __init__(self, table_cred = None):
        rule = Rule()
        rule.filter_type = 'SqlFilter'
        rule.filter_expression = "event = '%s' OR event = '%s'" % (SpeedCamera.EVENT_ACTIVATION, SpeedCamera.EVENT_DEACTIVATION)
        # Call super class constructor
        PersistentSubscriber.__init__(self, self.TABLE,
                                      SpeedCamera.TOPIC, "CameraRegister",
                                      "CameraRegisterRule", rule)

    # Query 1 of coursework
    def retrieveAllActivations(self):
        return self.retrievePartition(self.PARTITION_ACTIVATION)

    # Can query both camera activations and deactivations by partition key
    # Would like to have auto incrementing row key but there is no such thing in table storage
    # therefore we assume that - no two vehicles go through a camera at exactly the same time
    def dictToEntity(self, dic):
        entity = Entity()
        if dic['camera']['isActive'] == "True":
            entity.PartitionKey = self.PARTITION_ACTIVATION
        else:
            entity.PartitionKey = self.PARTITION_DEACTIVATION
        entity.RowKey = str(dic['camera']['timestamp'])
        entity.id = dic['camera']['id']
        entity.street = dic['camera']['street']
        entity.city = dic['camera']['city']
        entity.speedLimit = dic['camera']['speedLimit']
        entity.rate = dic['camera']['rate']
        if self.dump:
            print ""
            print "Partition Key = %s" % entity.PartitionKey
            print "Row Key = %s" % entity.RowKey
            print "Camera Id = %s" % entity.id
            print "Street = %s" % entity.street
            print "City = %s" % entity.city
            print "Speed Limit = %d" % entity.speedLimit
            print "Rate = %d" % entity.rate
            print ""
        return entity

################################################################################
################################################################################
#
#     Class responsible for handling and persisting vehicle sightings
#
################################################################################
################################################################################
class VehicleRegister(PersistentSubscriber):
    TABLE = "Sightings"
    PARTITION = "VehicleSightings"
    partitions = [PARTITION]

    def __init__(self, table_cred = None):
        rule = Rule()
        rule.filter_type = 'SqlFilter'
        rule.filter_expression = "event = '%s'" % (SpeedCamera.EVENT_VEHICLE)
        # Call super class constructor
        PersistentSubscriber.__init__(self, self.TABLE,
                                      SpeedCamera.TOPIC, "VehicleRegister",
                                      "VehicleRegisterRule", rule)

    # Can query both camera activations and deactivations by partition key
    # Would like to have auto incrementing row key but there is no such thing in table storage
    # therefore we assume that - no two vehicles go through a camera at exactly the same time
    def dictToEntity(self, dic):
        # Ditionary is nested so we have to un-nest it or else it fails
        entity = vehicleToEntity(dic, self.PARTITION, self.dump)
        return entity

################################################################################
################################################################################
#
#     Class responsible for handling and persisting speeding vehicle sightings
#
################################################################################
################################################################################

class PoliceMonitor(PersistentSubscriber):
    TABLE = "SpeedingSightings"
    PARTITION = "SpeedingVehicles"
    partitions = [PARTITION]
    
    def __init__(self, table_cred = None):
        rule = Rule()
        rule.filter_type = 'SqlFilter'
        rule.filter_expression = "event = '%s' AND isSpeeding = TRUE" % (SpeedCamera.EVENT_VEHICLE)
        # Call super class constructor
        PersistentSubscriber.__init__(self, self.TABLE,
                                      SpeedCamera.TOPIC, "PoliceMonitor",
                                      "PoliceMonitorRule", rule)

    # Query 2 of coursework
    def retrievePrioritySightings(self):
        return self.queryTable("PartitionKey eq '%s' and isPriority eq true" % self.PARTITION)

    # Can query both camera activations and deactivations by partition key
    # Would like to have auto incrementing row key but there is no such thing in table storage
    # therefore we assume that - no two vehicles go through a camera at exactly the same time
    def dictToEntity(self, dic):
        # Ditionary is nested so we have to un-nest it or else it fails
        entity = vehicleToEntity(dic, self.PARTITION, self.dump)
        return entity


# Helping function
def vehicleToEntity(dic, partitionKey, dump = False):
    entity = Entity()
    entity.PartitionKey = partitionKey
    entity.RowKey = str(dic['timestamp'])
    entity.camera = dic['camera']['id']
    entity.camera_activation = str(dic['camera']['timestamp'])
    entity.street = dic['camera']['street']
    entity.city = dic['camera']['city']
    entity.speedLimit = dic['camera']['speedLimit']
    entity.plate = dic['vehicle']['plate']
    entity.type = dic['vehicle']['type']
    entity.speed = dic['vehicle']['speed']
    entity.isSpeeding = dic['vehicle']['isSpeeding']
    entity.isPriority = dic['vehicle']['isPriority']
    if dump:
        print ""
        print "Partition Key = %s" % entity.PartitionKey
        print "Row Key = %s" % entity.RowKey
        print "Camera:"
        print "  Id = %s" % entity.camera
        print "  Street = %s" % entity.street
        print "  City = %s" % entity.city
        print "  Speed Limit = %d" % entity.speedLimit
        print "  Last Activation = %s" % entity.camera_activation
        print "Vehicle:"
        print "  Plate = %s" % entity.plate
        print "  Type = %s" % entity.type
        print "  Speed = %s" % str(entity.speed)
        print "  Speeding = %s" % entity.isSpeeding
        print "  Priority = %s" % entity.isPriority
        print ""
    return entity

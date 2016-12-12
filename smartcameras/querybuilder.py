from speedcamera import SpeedCamera
import nosqlconsumer
from azure.storage.table import TableService
import azurehook
import threading

class QueryBuilder(object):

    def __init__(self, table_cred = None):
        if table_cred is None:
            table_cred = azurehook.table_cred
        self.table = TableService(account_name=table_cred['account_name'],
                                  account_key=table_cred['mykey'])

    # Reference:
    # http://stackoverflow.com/questions/28019437/python-querying-all-rows-of-azure-table
    # Azure limitation: only a maximum of 1000 entities can be retrieved per query
    def retrieveCameraActivations(self):
        if not self.table.exists(nosqlconsumer.TableBuilder.TABLE_CAMERA):
            raise ValueError('Table %s does not exist', TableBuilder.TABLE_CAMERA)
        # hasRows = True
        marker = None
        cameras = []
        entities = self.table.query_entities(
                        nosqlconsumer.TableBuilder.TABLE_CAMERA,
                        "PartitionKey eq '%s'" % SpeedCamera.EVENT_ACTIVATION,
                        marker = marker,
                        num_results=1000)
        for entity in entities:
            cameras.append(entity)
        # while hasRows:
        #     entities = self.table.query_entities(
        #                     TableBuilder.TABLE_CAMERA,
        #                     "PartitionKey eq '%s'" % SpeedCamera.EVENT_ACTIVATION,
        #                     marker = marker,
        #                     num_results=1000)
        #     # for entity in entities:
            #     cameras.append(entity)
            #     print(entity)
            # if hasattr(entities, 'next_marker'):
            #     marker = getattr(entities, 'next_marker')
            # else:
            #     hasRows = False
        return cameras

    def retrieveVehicleObservations(self):
        return []

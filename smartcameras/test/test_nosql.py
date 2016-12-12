import threading
import time
import pytest
from smartcameras.nosqlconsumer import TableBuilder
from smartcameras.speedcamera import SpeedCamera
from smartcameras.querybuilder import QueryBuilder

def test_simple():
    table = TableBuilder()
    threadConsumer = threading.Thread(target=table.activate)
    threadConsumer.daemon = True
    threadConsumer.start()

    camera = SpeedCamera("Dragao", "Porto")
    threadProducer = threading.Thread(target=camera.activate, args=(50, 5))
    threadProducer.daemon = True
    threadProducer.start()

    time.sleep(5)

    camera.deactivate()
    threadProducer.join()

    table.terminate()
    threadConsumer.join()

    queryBuilder = QueryBuilder()
    entities = queryBuilder.retrieveCameraActivations()
    assert len(entities) > 0

def test_flushTables():    
    table = TableBuilder()
    table.flushTable(TableBuilder.TABLE_VEHICLE)
    table.flushTable(TableBuilder.TABLE_CAMERA)
    queryBuilder = QueryBuilder()
    entities = queryBuilder.retrieveCameraActivations()
    assert len(entities) == 0
    # with pytest.raises(ValueError):
    #     entities = queryBuilder.retrieveCameraActivations()

from smartcameras.azurehook import AzureHook

test_topic = "TESTING_TOPIC"
azure = AzureHook()

def test_constructor():
    assert azure.serviceBus.service_namespace == 'middle-earth'
    #assert azure.serviceBus.shared_access_key_name == 'RootManageSharedAccessKey'
    #assert azure.serviceBus.shared_access_key_value == 'LrEVp0ypG8jkxxnE1GHq0Jg1fT1DNGPgMaXGW1mKw3o='

def test_pupsub():
    azure.publish(test_topic)
    azure.subscribe(test_topic)

def test_queue():
    azure.queue("TESTING_QUEUE")

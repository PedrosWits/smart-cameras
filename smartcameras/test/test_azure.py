from smartcameras.azurehook import AzureHook

azure = AzureHook()

def test_constructor():
    assert azure.serviceBus.service_namespace == 'middle-earth'
    #assert azure.serviceBus.shared_access_key_name == 'RootManageSharedAccessKey'
    #assert azure.serviceBus.shared_access_key_value == 'LrEVp0ypG8jkxxnE1GHq0Jg1fT1DNGPgMaXGW1mKw3o='

def test_pupsub():
    test_topic = "TESTING_TOPIC"

    azure.createTopic(test_topic)
    azure.publish(test_topic, "Hello")

    azure.subscribe(test_topic)
    assert azure.getMessage(test_topic).body == "Hello"

def test_queue():
    test_queue = "TESTING_QUEUE"

    azure.createQueue(test_queue)
    azure.sendQueueMessage(test_queue, "Hello")
    assert azure.receiveQueueMessage(test_queue).body == "Hello"

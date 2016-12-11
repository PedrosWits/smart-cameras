from smartcameras.azurehook import AzureHook, AzurePublisher, AzureSubscriber, AzureQueue

def test_raw_hook():
    azure = AzureHook()
    assert azure.serviceBus.service_namespace == 'middle-earth'
    #assert azure.serviceBus.shared_access_key_name == 'RootManageSharedAccessKey'
    #assert azure.serviceBus.shared_access_key_value == 'LrEVp0ypG8jkxxnE1GHq0Jg1fT1DNGPgMaXGW1mKw3o='

def test_pupsub():
    test_topic = "TESTING_TOPIC"

    azurePub = AzurePublisher()
    azurePub.createTopic(test_topic)
    azurePub.publish(test_topic, "Hello")

    azureSub = AzureSubscriber()
    azureSub.subscribe(test_topic)
    assert azureSub.getMessage(test_topic).body == "Hello"

def test_queue():
    test_queue = "TESTING_QUEUE"

    azureQueue = AzureQueue()
    azureQueue.createQueue(test_queue)
    azureQueue.sendMessage(test_queue, "Hello")
    assert azureQueue.receiveMessage(test_queue).body == "Hello"

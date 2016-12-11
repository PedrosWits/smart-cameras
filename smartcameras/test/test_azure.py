from smartcameras.azurehook import AzureHook

azure = AzureHook()

def test_constructor():
    assert azure.serviceBus.service_namespace == 'middle-earth'

def test_pupsub():
    test_topic = "TESTING_TOPIC"

    azure.createTopic(test_topic)
    azure.publish(test_topic, "Hello")

    subscription = "helloworld"
    azure.subscribe(test_topic, subscription)
    assert azure.getMessage(test_topic, subscription, timeout='5').body == "Hello"
    azure.serviceBus.delete_subscription(test_topic, subscription)
    azure.serviceBus.delete_topic(test_topic)

def test_queue():
    test_queue = "TESTING_QUEUE"

    azure.createQueue(test_queue)
    azure.sendQueueMessage(test_queue, "Hello")
    assert azure.receiveQueueMessage(test_queue).body == "Hello"
    azure.serviceBus.delete_queue(test_queue)

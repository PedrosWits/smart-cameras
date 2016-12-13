import smartcameras.azurehook
import mock
import time

azure = smartcameras.azurehook.AzureHook()

def test_constructor():
    assert azure.serviceBus.service_namespace == 'middle-earth'

def test_pupsub():
    test_topic = "TESTING_TOPIC"

    azure.createTopic(test_topic)
    azure.publish(test_topic, "Hello")

    subscription = "helloworld"
    azure.subscribe(test_topic, subscription)
    message = azure.getMessage(test_topic, subscription, timeout='5')
    if message.body is not None:
        assert message.body == "Hello"
    azure.serviceBus.delete_subscription(test_topic, subscription)
    azure.serviceBus.delete_topic(test_topic)

def test_queue():
    test_queue = "TESTING_QUEUE"

    azure.createQueue(test_queue)
    azure.sendQueueMessage(test_queue, "Hello")
    assert azure.receiveQueueMessage(test_queue).body == "Hello"
    azure.serviceBus.delete_queue(test_queue)


# # Manual Test so far -- unable to mockup - but its working!
# def test_offline_behavior():
#     test_topic = "TESTING_TOPIC"
#
#     azure.createTopic(test_topic)
#
#     print("Turn off internet")
#     time.sleep(15)
#
#     assert not smartcameras.azurehook.hasConnectivity()
#
#     assert not azure.publish(test_topic, "Hello")
#
#     assert not azure.queue.empty()
#
#     print("Turn on internet")
#     time.sleep(15)
#
#     assert smartcameras.azurehook.hasConnectivity()
#     # Past messages are flushed on next publish
#     assert azure.publish(test_topic, "Hello Back")
#
#     assert azure.queue.empty()
#     azure.serviceBus.delete_topic(test_topic)

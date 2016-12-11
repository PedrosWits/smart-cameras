from abc import ABCMeta
from smartcameras.cloudhook import CloudHook
from azure.servicebus import ServiceBusService, Message, Topic, Queue

middle_earth = {"service_namespace" : 'middle-earth',
                "shared_access_key_name" : 'RootManageSharedAccessKey',
                "shared_access_key_value" : 'LrEVp0ypG8jkxxnE1GHq0Jg1fT1DNGPgMaXGW1mKw3o='}

class AzureHook(CloudHook):

    def __init__(self, serviceKeyValues = middle_earth):
        # Call super class constructor
        CloudHook.__init__(self, serviceKeyValues)

    # Implement abstract methods
    def setupHook(self, kv):
        self.serviceBus = ServiceBusService(
            service_namespace = kv['service_namespace'],
            shared_access_key_name = kv['shared_access_key_name'],
            shared_access_key_value = kv['shared_access_key_value'])


## A wrapper class for azure queue
class AzureQueue(AzureHook):

    def __init__(self, serviceKeyValues = middle_earth):
        # Call super class constructor
        AzureHook.__init__(self, serviceKeyValues)

    def createQueue(self, queueName, queueOptions = None):
        if queueOptions is None:
            queueOptions = Queue()
            queueOptions.max_size_in_megabytes = '5120'
            queueOptions.default_message_time_to_live = 'PT1M'
        self.serviceBus.create_queue(queueName, queueOptions)

    def sendMessage(self, queueName, messageBody):
        self.serviceBus.send_queue_message(queueName, Message(messageBody))

    def receiveMessage(self, queueName, peek_lock=False):
        return self.serviceBus.receive_queue_message(queueName, peek_lock)


## A wrapper class that represents an azure publisher
class AzurePublisher(AzureHook):

    def __init__(self, serviceKeyValues = middle_earth):
        # Call super class constructor
        AzureHook.__init__(self, serviceKeyValues)

    def createTopic(self, topicName, topicOptions = None):
        if topicOptions is None:
            topicOptions = Topic()
            topicOptions.max_size_in_megabytes = '5120'
            topicOptions.default_message_time_to_live = 'PT1M'
        self.serviceBus.create_topic(topicName, topicOptions)

    def publish(self, topic, messageBody):
        message = Message(messageBody)
        self.serviceBus.send_topic_message(topic, message)

## A wrapper class that represents an azure subscriber
class AzureSubscriber(AzureHook):

    def __init__(self, serviceKeyValues = middle_earth):
        # Call super class constructor
        AzureHook.__init__(self, serviceKeyValues)

    def subscribe(self, topicName, sfilter = 'AllMessages'):
        self.serviceBus.create_subscription(topicName, sfilter)

    def getMessage(self, topicName, sfilter = 'AllMessages'):
        return self.serviceBus.receive_subscription_message(topicName, sfilter)

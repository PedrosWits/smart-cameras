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


    def queue(self, queueName, queueOptions = None):
        if queueOptions is None:
            queueOptions = Queue()
            queueOptions.max_size_in_megabytes = '5120'
            queueOptions.default_message_time_to_live = 'PT1M'
        self.serviceBus.create_queue(queueName, queueOptions)


    def publish(self, topicName, topicOptions = None):
        if topicOptions is None:
            topicOptions = Topic()
            topicOptions.max_size_in_megabytes = '5120'
            topicOptions.default_message_time_to_live = 'PT1M'
        self.serviceBus.create_topic(topicName, topicOptions)

    def subscribe(self, topicName, sfilter = 'AllMessages'):
        self.serviceBus.create_subscription(topicName, sfilter)

    def sendMessage(self, target, message):
        pass

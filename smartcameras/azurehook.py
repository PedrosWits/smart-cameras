from abc import ABCMeta
from cloudhook import CloudHook
import urllib2
from azure.servicebus import ServiceBusService, Message, Topic, Queue
import Queue as pyqueue

middle_earth = {"service_namespace" : 'middle-earth',
                "shared_access_key_name" : 'RootManageSharedAccessKey',
                "shared_access_key_value" : 'LrEVp0ypG8jkxxnE1GHq0Jg1fT1DNGPgMaXGW1mKw3o='}

table_cred = {"mykey" : "umh7XfkHhN05Blx7+LltNoSZ8xr6qD7l5dJZ44LRJH6YoQ4sWvQ6D2lyl31h3RfOBS/YWdtUN5ZseAKTnSctpg==",
              "account_name" : "smartcamerasdiag952"}

class AzureHook(CloudHook):

    def __init__(self, serviceKeyValues = middle_earth):
        # Call super class constructor
        CloudHook.__init__(self, serviceKeyValues)
        self.queue = pyqueue.Queue()

    # Implement abstract methods
    def setupHook(self, kv):
        self.serviceBus = ServiceBusService(
            service_namespace = kv['service_namespace'],
            shared_access_key_name = kv['shared_access_key_name'],
            shared_access_key_value = kv['shared_access_key_value'])

    def createQueue(self, queueName, queueOptions = None):
        if queueOptions is None:
            queueOptions = Queue()
            queueOptions.max_size_in_megabytes = '5120'
            queueOptions.default_message_time_to_live = 'PT1M'
        self.serviceBus.create_queue(queueName, queueOptions)

    def sendQueueMessage(self, queueName, messageBody):
        self.serviceBus.send_queue_message(queueName, Message(messageBody))

    def receiveQueueMessage(self, queueName, peek_lock=False):
        return self.serviceBus.receive_queue_message(queueName, peek_lock)

    def createTopic(self, topicName, topicOptions = None):
        if topicOptions is None:
            topicOptions = Topic()
            topicOptions.max_size_in_megabytes = '5120'
            topicOptions.default_message_time_to_live = 'PT1M'
        self.serviceBus.create_topic(topicName, topicOptions)

    def publish(self, topicName, messageBody, extra = None):
        if hasConnectivity():
            self.flushQueue()
            message = Message(messageBody, custom_properties=extra)
            self.serviceBus.send_topic_message(topicName, message)
            return True
        else:
            self.queue.put({'topicName' : topicName,
                            'messageBody' : messageBody,
                            'extra' : extra})
            return False

    def subscribe(self, topicName, subscriptionName):
        self.serviceBus.create_subscription(topicName, subscriptionName)

    def getMessage(self, topicName, subscriptionName, peek_lock = False, timeout = '60'):
        return self.serviceBus.receive_subscription_message(topicName, subscriptionName,
                                                            peek_lock = peek_lock, timeout = timeout)

    # We could persist the data in a local sqllite database, which would be easy
    # but we feel that that goes beyond the scope of this project
    def flushQueue(self):
        while not self.queue.empty():
            try:
                dic = self.queue.get_nowait()
            except Queue.Empty:
                break
            message = Message(dic['messageBody'], custom_properties=dic['extra'])
            self.serviceBus.send_topic_message(dic['topicName'], message)


##########################################################################################
##########################################################################################
##########################################################################################
#
#       Helping Functions
#
##########################################################################################
##########################################################################################
##########################################################################################

# Taken from: http://stackoverflow.com/questions/3764291/checking-network-connection
def hasConnectivity():
    try:
        urllib2.urlopen('http://www.google.com', timeout=1)
        return True
    except urllib2.URLError as err:
        return False

from abc import ABCMeta, abstractmethod

class CloudHook(object):
    __metaclass__ = ABCMeta

    # Create a hook to a cloud provider for which you can
    # submit messages
    def __init__(self, serviceKeyValues):
        if type(serviceKeyValues) is not dict:
            raise ValueError('serviceKeyValues must be a dictionary \
                              with the keys and values necessary to \
                              communicate with the cloud provider')
        self.setupHook(serviceKeyValues)

    @abstractmethod
    def setupHook(self, serviceKeyValues):
        pass

    @abstractmethod
    def createQueue(self, queueName):
        pass

    @abstractmethod
    def sendQueueMessage(self, queueName, messageBody):
        pass

    @abstractmethod
    def receiveQueueMessage(self, queueName):
        pass

    @abstractmethod
    def createTopic(self, topicName):
        pass

    @abstractmethod
    def publish(self, topicName, messageBody):
        pass

    @abstractmethod
    def subscribe(self, topicName, sfilter):
        pass

    @abstractmethod
    def getMessage(self, topicName, sfilter):
        pass

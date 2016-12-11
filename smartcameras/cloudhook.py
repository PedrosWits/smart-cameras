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
    def publish(self, to, args):
        pass

    @abstractmethod
    def subscribe(self, to, args):
        pass


    @abstractmethod
    def sendMessage(self, to, message):
        pass

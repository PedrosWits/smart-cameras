from azure.servicebus import ServiceBusService, Message, Queue

# Example taken from:
# https://docs.microsoft.com/en-us/azure/service-bus-messaging/service-bus-python-how-to-use-queues
bus_service = ServiceBusService(
    service_namespace = 'middle-earth',
    shared_access_key_name = 'RootManageSharedAccessKey',
    shared_access_key_value = 'LrEVp0ypG8jkxxnE1GHq0Jg1fT1DNGPgMaXGW1mKw3o=')

# Change default queue options
queue_options = Queue()
queue_options.max_size_in_megabytes = '5120'
queue_options.default_message_time_to_live = 'PT1M'

# The queue is remotely known by 'taskqueue'
bus_service.create_queue('taskqueue', queue_options)

# Sending messages
msg = Message(b'Test Message')
bus_service.send_queue_message('taskqueue', msg)

msg2 = bus_service.receive_queue_message('taskqueue', peek_lock=False)
print(msg2.body)

import zmq

class CameraServer(object):

    def __init__(self, port = 5555):
        # Start zmq server
        context = zmq.Context()
        socket = context.socket(zmq.REP)
        url = "tcp://127.0.0.1:" + str(port)
        socket.bind(url)
        # If successful
        self.isAlive = True
        while isAlive:
            msg = socket.recv()
            self.parseMessage(msg)

    def terminate(self):
        


    def parseMessage(self, message):
        if message == 'zeromq':
            socket.send('ah ha!')
        else:
            socket.send('...nah')

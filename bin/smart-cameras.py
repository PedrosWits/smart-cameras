#!/usr/bin/env python
import sys
import argparse
import zmq

# What shall the manager of the smart-cameras do?
class CLIParser(object):

    def __init__(self):
        parser = argparse.ArgumentParser(
            description='A CLI for operating speed cameras in smart cities',
            usage='''smart-cameras <action> [<args>]

The available actions are:
   start        Start the cameras' service manager
   shutdown     Terminate the service manager
   status       Show the status of the service manager [dead or alive]
   camera       Execute operations on speed cameras,
                such as create, destroy, activate, relocate
''')
        parser.add_argument('action',
                            metavar="<action>",
                            choices=['start', 'shutdown', 'status', 'camera'],
                            help='%(choices)s')
        # parse_args defaults to [1:] for args, but you need to
        # exclude the rest of the args too, or validation will fail
        args = parser.parse_args(sys.argv[1:2])
        if not hasattr(self, args.action):
            print 'Unrecognized action'
            parser.print_help()
            exit(1)
        # use dispatch pattern to invoke method with same name
        getattr(self, args.action)()

    def start(self):
        parser = argparse.ArgumentParser(
            description='Start the smart camera manager')
        # now that we're inside a subcommand, ignore the first
        # TWO argvs, ie the command (git) and the subcommand (commit)
        args = parser.parse_args(sys.argv[2:])
        print 'Starting the manager'

    def shutdown(self):
        parser = argparse.ArgumentParser(
            description='Shut down the smart camera manager')
        args = parser.parse_args(sys.argv[2:])
        print 'Shutting down the manager'

    def status(self):
        parser = argparse.ArgumentParser(
            description='Query the status of the smart camera manager')
        args = parser.parse_args(sys.argv[2:])
        print 'Service status: [dead/alive]'

    def camera(self):
        CameraParser(sys.argv[1:])
        # NOT prefixing the argument with -- means it's not optional
        # parser.add_argument('street', action='store_true')
        # parser.add_argument('repository')


class CameraParser(object):

    def __init__(self, argv):
        parser = argparse.ArgumentParser(
            description='Operate speed cameras',
            usage='''smart-cameras camera <operation> [<parameters>]

The available actions are:
   create      Assign a new speed camera to the population of cameras
   destroy     Destroy an existing speed camera
   activate    Turn an existing speed camera on,
               i.e. start monitoring the speed of vehicles
   deactivate  Turn an existing speed camera off
   relocate    Move the speed camera to a different location
''')
        parser.add_argument('action',
                            metavar="<operation>",
                            choices=['create', 'destroy', 'activate', 'deactivate', 'relocate'],
                            help='%(choices)s')
        # parse_args defaults to [1:] for args, but you need to
        # exclude the rest of the args too, or validation will fail
        args = parser.parse_args(argv[1:2])
        if not hasattr(self, args.action):
            print 'Unrecognized operation'
            parser.print_help()
            exit(1)
        # use dispatch pattern to invoke method with same name
        getattr(self, args.action)()




# if args.bar:
#     # client
#     context = zmq.Context()
#     socket = context.socket(zmq.REQ)
#     socket.connect('tcp://127.0.0.1:5555')
#     socket.send(args.bar)
#     msg = socket.recv()
#     print msg
# else:
#     # server
#     context = zmq.Context()
#     socket = context.socket(zmq.REP)
#     socket.bind('tcp://127.0.0.1:5555')
#     while True:
#         msg = socket.recv()
#         if msg == 'zeromq':
#             socket.send('ah ha!')
#         else:
#             socket.send('...nah')


if __name__ == "__main__":
    CLIParser()

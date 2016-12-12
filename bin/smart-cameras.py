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

Available actions:
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
        getattr(self, args.action)(sys.argv[1:])

    def start(self, argv):
        parser = argparse.ArgumentParser(
            description='Start the smart camera manager')
        # now that we're inside a subcommand, ignore the first
        print 'Starting the manager'

    def shutdown(self, argv):
        parser = argparse.ArgumentParser(
            description='Shut down the smart camera manager')
        print 'Shutting down the manager'

    def status(self, argv):
        parser = argparse.ArgumentParser(
            description='Query the status of the smart camera manager')
        print 'Service status: [dead/alive]'

    def camera(self, argv):
        CameraParser(argv)


class CameraParser(object):

    def __init__(self, argv):
        parser = argparse.ArgumentParser(
            description='Operate speed cameras',
            usage='''smart-cameras camera <operation> [<parameters>]

Available operations:
   create      Create a new speed camera
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
        getattr(self, args.action)(argv[2:])

    def create(self, argv):
        parser = argparse.ArgumentParser(
            description='Create a new speed camera',
            prog="smart-cameras camera create")
        # NOT prefixing the argument with -- means it's not optional
        parser.add_argument('street', type=str)
        parser.add_argument('city', type=str)
        #parser.add_argument('--activate', action='store_true',
        #                    help="Activate the camera on successful creation")
        args = parser.parse_args(argv)
        #print(args)
        print 'Create camera at: %s, %s' % (args.street, args.city)

    def destroy(self, argv):
        parser = argparse.ArgumentParser(
            description='Destroy an existing speed camera',
            prog="smart-cameras camera destroy")
        # NOT prefixing the argument with -- means it's not optional
        parser.add_argument('uuid', type=str, help="Uuid or name of camera")
        args = parser.parse_args(argv)
        #print(args)
        print 'Destroy camera %s' % args.uuid

    def activate(self, argv):
        parser = argparse.ArgumentParser(
            description='Activate an existing speed camera',
            prog="smart-cameras camera activate")
        # NOT prefixing the argument with -- means it's not optional
        parser.add_argument('uuid', type=str, help="Uuid or name of camera")
        parser.add_argument('speed_limit', type=int, help="Maximum vehicle speed allowed in this zone")
        parser.add_argument('rate', type=int, help="Rate of vehicles detected by the camera")
        args = parser.parse_args(argv)
        #print(args)
        print 'Activate camera %s with: (%d, %d)' % (args.uuid, args.speed_limit, args.rate)

    def deactivate(self, argv):
        parser = argparse.ArgumentParser(
            description='Dectivate an existing speed camera',
            prog="smart-cameras camera deactivate")
        # NOT prefixing the argument with -- means it's not optional
        parser.add_argument('uuid', type=str, help="Uuid or name of camera")
        args = parser.parse_args(argv)
        #print(args)
        print 'Deactivate camera %s' % args.uuid

    def relocate(self, argv):
        parser = argparse.ArgumentParser(
            description='Relocate an existing speed camera',
            prog="smart-cameras camera relocate")
        # NOT prefixing the argument with -- means it's not optional
        parser.add_argument('uuid', type=str, help="Uuid or name of camera")
        parser.add_argument('street', type=str)
        parser.add_argument('city', type=str, nargs="?", default=None)
        args = parser.parse_args(argv)
        #print(args)
        print 'Relocate camera %s to: (%s, %s)' % (args.uuid, args.street, args.city)


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
#


if __name__ == "__main__":
    CLIParser()

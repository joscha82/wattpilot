import argparse
import json
import logging
import readline
import wattpilot
import yaml

from time import sleep
from types import SimpleNamespace

_LOGGER = logging.getLogger(__name__)

def printPropInfo(wpi, propName, value):
    propInfo = wpi['properties'][propName]
    propTitle = ""
    propDesc = ""
    propAlias = ""
    if 'alias' in propInfo:
        propAlias = f", alias:{propInfo['alias']}"
    if 'title' in propInfo:
        propTitle = propInfo['title']
    if 'description' in propInfo:
        propDesc = propInfo['description']
    print(f"- {propName} ({propInfo['type']}{propAlias}): {propTitle}")
    print(f"  Value: {value}")
    if propDesc:
        print(f"  Description: {propDesc}")
    if 'itemType' in propInfo:
        print(f"  Array item type: {propInfo['itemType']}")
    if 'min' in propInfo:
        print(f"  Minimum value: {propInfo['min']}")
    if 'max' in propInfo:
        print(f"  Maximum value: {propInfo['max']}")
    if 'example' in propInfo:
        print(f"  Example: {propInfo['example']}")

def watch_properties(name,value):
    if name in watching_properties:
        print(f"INFO: Property {name} changed to {value}")

def watch_messages(wsapp,msg):
    if msg.type in watching_messages:
        print(f"INFO: Message of type {msg.type} received: {msg}")

def process_command(wp, wpi, cmdline):
    """Process a Wattpilot shell command"""
    exit = False
    cmd_args = cmd_parser.parse_args(args=cmdline.strip().split(' '))
    cmd = cmd_args.cmd.strip()
    args = cmd_args.args
    if (cmd == ''):
        # Don't do anything
        exit = False
    elif (cmd == 'dump'):
        for propName, value in sorted(wp.allProps.items(), key=lambda x: x[0]): 
            print("{}: {}".format(propName, value))
    elif cmd == "exit":
        exit = True
    elif (cmd == 'get'):
        if len(args) != 1:
            print(f"Wrong number of arguments: get <property>")
        elif not args[0] in wp.allProps:
            print(f"Unknown property: {args[0]}")
        else:
            print(wp.allProps[args[0]])
    elif (cmd == 'help'):
        print("Wattpilot Shell Commands:")
        print("  dump: Dump all property values")
        print("  exit: Exit the shell")
        print("  get <name>: Get a property value")
        print("  info: Print most important infos")
        print("  list: List all known property keys")
        print("  set <name> <value>: Set a property value")
        print("  watch message <type>: Watch message of given message type")
        print("  watch property <name>: Watch value changes of given property name")
        print("  unwatch message <type>: Unwatch messages of given message type")
        print("  unwatch property <name>: Unwatch value changes of given property name")
    elif (cmd == 'info'):
        print(wp)
    elif (cmd == 'list'):
        print(f"List of available properties:")
        for propName, value in sorted(wp.allProps.items()):
            printPropInfo(wpi,propName,value)
        print()
    elif (cmd == 'set'):
        if len(args) != 2:
            print(f"Wrong number of arguments: set <property> <value>")
        elif not args[0] in wp.allProps:
            print(f"Unknown property: {args[0]}")
        else:
            if str(args[1]).isnumeric():
                v=int(args[1])
            elif str(args[1]).isdecimal():
                v=float(args[1])
            else:
                v=str(args[1])
            wp.send_update(args[0],v)
    elif (cmd == 'watch'):
        if len(args) != 2:
            print(f"Wrong number of arguments!")
        elif args[0] == "message" and not args[1] in wpi['messages']:
            print(f"Unknown message type: {args[1]}")
        elif args[0] == "message":
            if len(watching_messages) == 0:
                wp.register_message_callback(watch_messages)
            if args[1] not in watching_messages:
                watching_messages.append(args[1])
        elif args[0] == "property" and not args[1] in wp.allProps:
            print(f"Unknown property: {args[1]}")
        elif args[0] == "property":
            if len(watching_properties) == 0:
                wp.register_property_callback(watch_properties)
            if args[1] not in watching_properties:
                watching_properties.append(args[1])
        else:
            print(f"Unknown watch type: {args[0]}")
    elif (cmd == 'unwatch'):
        if len(args) != 2:
            print(f"Wrong number of arguments!")
        elif args[0] == "message" and not args[1] in watching_messages:
            print(f"Message of type '{args[1]}' is not watched")
        elif args[0] == "message":
            watching_messages.remove(args[1])
            if len(watching_messages) == 0:
                wp.unregister_message_callback()
        elif args[0] == "property" and not args[1] in watching_properties:
            print(f"Property with name '{args[1]}' is not watched")
        elif args[0] == "property":
            watching_properties.remove(args[1])
            if len(watching_properties) == 0:
                wp.unregister_property_callback()
        else:
            print(f"Unknown watch type: {args[0]}")
    else:
        print(f"Unknown command: {cmd}")
    return exit

def complete(text,state):
    """Simple readline completer"""
    volcab = ['dump','exit','get','help','info','list','set']
    results = [x for x in volcab if x.startswith(text)] + [None]
    return results[state]

def wait_timeout(fn, timeout):
    """Generic timeout waiter"""
    t = 0
    within_timeout = True
    while not fn() and t<timeout:
        sleep(1)
        t += 1
    if t>=timeout:
        within_timeout = False
    return within_timeout


# Timeouts:
connect_timeout = 10
initialized_timeout = 10

# Globals:
watching_properties = []
watching_messages = []

# Set debug level:
logging.basicConfig(level='WARNING')

# Setup readline
readline.parse_and_bind("tab: complete")
readline.set_completer(complete) 

# Commandline argument parser:
parser = argparse.ArgumentParser()
parser.add_argument("ip", help = "IP of Wattpilot Device")
parser.add_argument("password", help = "Password of Wattpilot")
parser.add_argument("cmdline", help = "Optional shell command", nargs="?")
args = parser.parse_args()

# Wattpilot shell command parser:
cmd_parser = argparse.ArgumentParser()
cmd_parser.add_argument("cmd", help = "Command")
cmd_parser.add_argument("args", help = "Arguments", nargs='*')

# Read Wattpilot config:
with open("wattpilot.yaml", 'r') as stream:
    try:
        wpi=yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

# Connect to Wattpilot:
wp = wattpilot.Wattpilot(args.ip,args.password)
wp.connect()

# Wait for connection and initializon:
wait_timeout(lambda: wp.connected, connect_timeout) or exit("ERROR: Timeout while connecting to Wattpilot!")
wait_timeout(lambda: wp.allPropsInitialized, initialized_timeout) or exit("ERROR: Timeout while waiting for property initialization!")

# Process commands:
if args.cmdline:
    # Process commands passed on the commandline
    process_command(wp,wpi,args.cmdline)
else:
    # Start interactive shell
    process_command(wp,wpi,"info")
    exit=False
    while not exit:
        try:
            command = input('> ')
        except EOFError as e:
            command = "exit"
            print()
        exit = process_command(wp,wpi,command)

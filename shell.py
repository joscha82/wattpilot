import argparse
import json
import logging
import readline
import wattpilot

from time import sleep
from types import SimpleNamespace

_LOGGER = logging.getLogger(__name__)

def process_command(wp, cmdline):
    """Process a Wattpilot shell command"""
    exit = False
    cmd_args = cmd_parser.parse_args(args=cmdline.strip().split(' '))
    cmd = cmd_args.cmd.strip()
    args = cmd_args.args
    if (cmd == ''):
        # Don't do anything
        exit = False
    elif (cmd == 'dump'):
        for key, value in sorted(wp.allProps.items(), key=lambda x: x[0]): 
            print("{}: {}".format(key, value))
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
    elif (cmd == 'info'):
        print(wp)
    elif (cmd == 'list'):
        for key in sorted(wp.allProps.keys()): 
            print(f"{key} ", end="")
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

# Connect to Wattpilot:
wp = wattpilot.Wattpilot(args.ip,args.password)
wp.connect()

# Wait for connection and initializon:
wait_timeout(lambda: wp.connected, connect_timeout) or exit("ERROR: Timeout while connecting to Wattpilot!")
wait_timeout(lambda: wp.allPropsInitialized, initialized_timeout) or exit("ERROR: Timeout while waiting for property initialization!")

# Process commands:
if args.cmdline:
    # Process commands passed on the commandline
    process_command(wp,args.cmdline)
else:
    # Start interactive shell
    process_command(wp,"info")
    exit=False
    while not exit:
        try:
            command = input('> ')
        except EOFError as e:
            command = "exit"
            print()
        exit = process_command(wp,command)

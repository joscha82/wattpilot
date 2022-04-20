import argparse
from ast import arg
import json
import logging
import os
import paho.mqtt.client as mqtt
import readline
import wattpilot
import yaml
import pkgutil

from time import sleep
from types import SimpleNamespace

_LOGGER = logging.getLogger(__name__)

def print_prop_info(wpi, propName, value):
    global wpi_properties

    #propInfo = next((x for x in wpi['properties'] if x['key'] == propName), None)
    propInfo = wpi_properties[propName]
    _LOGGER.debug(f"Property info: {propInfo}")
    propTitle = ""
    propDesc = ""
    propAlias = ""
    propRw = ""
    if 'rw' in propInfo:
        propRw = f", rw:{propInfo['rw']}"
    if 'alias' in propInfo:
        propAlias = f", alias:{propInfo['alias']}"
    if 'title' in propInfo:
        propTitle = propInfo['title']
    if 'description' in propInfo:
        propDesc = propInfo['description']
    print(f"- {propName} ({propInfo['jsonType']}{propRw}{propAlias}): {propTitle}")
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
    global watch_properties
    if name in watching_properties:
        _LOGGER.info(f"Property {name} changed to {value}")

def watch_messages(wp,wsapp,msg,msg_json):
    if msg.type in watching_messages:
        _LOGGER.info(f"Message of type {msg.type} received: {msg}")

def cmd_get(wp, args):
    if len(args) != 1:
        _LOGGER.error(f"Wrong number of arguments: get <property>")
    elif not args[0] in wp.allProps:
        _LOGGER.error(f"Unknown property: {args[0]}")
    else:
        print(wp.allProps[args[0]])

def cmd_mqtt_connect(wp, args):
    global mqtt_client
    if len(args) != 2:
        _LOGGER.error(f"Wrong number of arguments: mqtt-connect <host> <port>")
    else:
        host = args[0]
        port = int(args[1])
        mqtt_client.connect(host, port)

def cmd_mqtt_disconnect(wp):
    if mqtt_client.is_connected():
        _LOGGER.info(f"Disconnecting from MQTT server ...")
        mqtt_client.disconnect()

def cmd_set(wp, args):
    if len(args) != 2:
        _LOGGER.error(f"Wrong number of arguments: set <property> <value>")
    elif not args[0] in wp.allProps:
        _LOGGER.error(f"Unknown property: {args[0]}")
    else:
        if args[1].lower() in ["false","true"]:
            v=json.loads(args[1].lower())
        elif str(args[1]).isnumeric():
            v=int(args[1])
        elif str(args[1]).isdecimal():
            v=float(args[1])
        else:
            v=str(args[1])
        wp.send_update(args[0],v)

def cmd_watch_message(wp, name):
    global watch_messages

    if len(watching_messages) == 0:
        wp.register_message_callback(watch_messages)
    if name not in watching_messages:
        watching_messages.append(name)

def cmd_watch_property(wp, name):
    global watch_properties
    if len(watching_properties) == 0:
        wp.register_property_callback(watch_properties)
    if name not in watching_properties:
        watching_properties.append(name)

def cmd_watch(wp, args):
    if len(args) != 2:
        _LOGGER.error(f"Wrong number of arguments!")
    elif args[0] == "message" and not args[1] in wpi['messages']:
        _LOGGER.error(f"Unknown message type: {args[1]}")
    elif args[0] == "message":
        cmd_watch_message(wp, args[1])
    elif args[0] == "property" and not args[1] in wp.allProps:
        _LOGGER.error(f"Unknown property: {args[1]}")
    elif args[0] == "property":
        cmd_watch_property(wp, args[1])
    else:
        _LOGGER.error(f"Unknown watch type: {args[0]}")

def cmd_unwatch(wp,args):
    if len(args) != 2:
        _LOGGER.error(f"Wrong number of arguments!")
    elif args[0] == "message" and not args[1] in watching_messages:
        _LOGGER.warning(f"Message of type '{args[1]}' is not watched")
    elif args[0] == "message":
        watching_messages.remove(args[1])
        if len(watching_messages) == 0:
            wp.unregister_message_callback()
    elif args[0] == "property" and not args[1] in watching_properties:
        _LOGGER.warning(f"Property with name '{args[1]}' is not watched")
    elif args[0] == "property":
        watching_properties.remove(args[1])
        if len(watching_properties) == 0:
            wp.unregister_property_callback()
    else:
        _LOGGER.error(f"Unknown watch type: {args[0]}")

def process_command(wp, wpi, cmdline):

    global cmd_parser
    global parse
    global wpi_properties

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
        cmd_get(wp,args)
    elif (cmd == 'help'):
        print("Wattpilot Shell Commands:")
        print("  dump: Dump all property values")
        print("  exit: Exit the shell")
        print("  get <name>: Get a property value")
        print("  info: Print most important infos")
        print("  list [propsearch]: List all properties (starting with propsearch if given)")
        print("  mqtt-connect <host> <port>: Connect to MQTT server")
        print("  mqtt-disconnect: Disconnect from MQTT server")
        print("  set <name> <value>: Set a property value")
        print("  watch message <type>: Watch message of given message type")
        print("  watch property <name>: Watch value changes of given property name")
        print("  unwatch message <type>: Unwatch messages of given message type")
        print("  unwatch property <name>: Unwatch value changes of given property name")
    elif (cmd == 'info'):
        print(wp)
    elif (cmd == 'list'):
        print(f"List of available properties:")
        if len(args)==1:
            props = {k:v for k,v in wp.allProps.items() if k.startswith(args[0])}
        else:
            props = wp.allProps
        for propName, value in sorted(props.items()):
            print_prop_info(wpi,propName,value)
        print()
    elif (cmd == 'mqtt-connect'):
        cmd_mqtt_connect(wp, args)
    elif (cmd == 'mqtt-disconnect'):
        cmd_mqtt_disconnect(wp)
    elif (cmd == 'set'):
        cmd_set(wp, args)
    elif (cmd == 'watch'):
        cmd_watch(wp,args)
    elif (cmd == 'unwatch'):
        cmd_unwatch(wp,args)
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

# MQTT functions

def mqtt_message(wp,wsapp,msg,msg_json):
    global MQTT_PUBLISH_MESSAGES
    global MQTT_BASE_TOPIC
    global MQTT_PUBLISH_PROPERTIES
    global MQTT_WATCH_PROPERTIES
    global MQTT_PROPERTY_READ_TOPIC_PATTERN
    global MQTT_MESSAGE_TOPIC_PATTERN

    if mqtt_client == None:
        _LOGGER.debug(f"Skipping MQTT message publishing.")
        return
    if msg.type not in ["fullStatus", "deltaStatus"]:
        _LOGGER.debug(f"Skipping MQTT message publishing of type {msg.type}.")
        return
    msg_dict = json.loads(msg_json)
    if MQTT_PUBLISH_MESSAGES == "true":
        message_topic = MQTT_MESSAGE_TOPIC_PATTERN \
            .replace("{baseTopic}",MQTT_BASE_TOPIC) \
            .replace("{serialNumber}",wp.serial) \
            .replace("{messageType}",msg.type)
        mqtt_client.publish(message_topic, msg_json)
    if MQTT_PUBLISH_PROPERTIES == "true":
        for prop_name, value in msg_dict["status"].items():
            if MQTT_WATCH_PROPERTIES == [] or prop_name in MQTT_WATCH_PROPERTIES:
                _LOGGER.debug(f"Publishing property '{prop_name}' with value '{value}' to MQTT ...")
                property_topic = MQTT_PROPERTY_READ_TOPIC_PATTERN \
                    .replace("{baseTopic}",MQTT_BASE_TOPIC) \
                    .replace("{serialNumber}",wp.serial) \
                    .replace("{propName}",prop_name)
                mqtt_client.publish(property_topic, json.dumps(value))


def main():
    # Timeout config:
    WATTPILOT_CONNECT_TIMEOUT = int(os.environ.get('WATTPILOT_CONNECT_TIMEOUT','30'))
    WATTPILOT_INITIALIZED_TIMEOUT = int(os.environ.get('WATTPILOT_INITIALIZED_TIMEOUT','30'))

    # Globals:
    global cmd_parser
    global parser
    global wpi_properties
    global wpi_messages
    global mqtt_client
    global watching_messages
    global watching_properties
    global MQTT_PUBLISH_MESSAGES
    global MQTT_BASE_TOPIC
    global MQTT_PUBLISH_PROPERTIES
    global MQTT_WATCH_PROPERTIES
    global MQTT_PROPERTY_READ_TOPIC_PATTERN
    global MQTT_MESSAGE_TOPIC_PATTERN


    watching_properties = []
    watching_messages = []
    mqtt_client = None

    # MQTT config:
    MQTT_ENABLED = os.environ.get('MQTT_ENABLED','false')
    if MQTT_ENABLED == "true":
        MQTT_CLIENT_ID = os.environ.get('MQTT_CLIENT_ID','wattpilot2mqtt')
        MQTT_HA_DISCOVERY_ENABLED = os.environ.get('MQTT_HA_DISCOVERY_ENABLED','false')
        MQTT_HOST = os.environ.get('MQTT_HOST')
        MQTT_PORT = int(os.environ.get('MQTT_PORT','1883'))
        MQTT_BASE_TOPIC = os.environ.get('MQTT_BASE_TOPIC','wattpilot')
        MQTT_PUBLISH_MESSAGES = os.environ.get('MQTT_PUBLISH_MESSAGES','true')
        MQTT_MESSAGE_TOPIC_PATTERN = os.environ.get('MQTT_MESSAGE_TOPIC_PATTERN','{baseTopic}/{serialNumber}/messages/{messageType}')
        MQTT_PUBLISH_PROPERTIES = os.environ.get('MQTT_PUBLISH_PROPERTIES','false')
        MQTT_WATCH_PROPERTIES = os.environ.get('MQTT_WATCH_PROPERTIES','amp car fna lmo sse').split(sep=' ')
        MQTT_PROPERTY_READ_TOPIC_PATTERN = os.environ.get('MQTT_PROPERTY_READ_TOPIC_PATTERN','{baseTopic}/{serialNumber}/properties/{propName}')
        MQTT_PROPERTY_SET_TOPIC_PATTERN = os.environ.get('MQTT_PROPERTY_SET_TOPIC_PATTERN','{baseTopic}/{serialNumber}/properties/{propName}/set')
        mqtt_client = mqtt.Client(MQTT_CLIENT_ID)
        mqtt_client.connect(MQTT_HOST, MQTT_PORT)


    # Set debug level:
    logging.basicConfig(level=os.environ.get('WATTPILOT_DEBUG_LEVEL','INFO'))

    # Setup readline
    readline.parse_and_bind("tab: complete")
    readline.set_completer(complete) 

    # Commandline argument parser:
    parser = argparse.ArgumentParser()
    parser.add_argument("ip", help = "IP of Wattpilot Device", nargs="?")
    parser.add_argument("password", help = "Password of Wattpilot", nargs="?")
    parser.add_argument("cmdline", help = "Optional shell command", nargs="?")

    args = parser.parse_args()

    # Wattpilot shell command parser:
    cmd_parser = argparse.ArgumentParser()
    cmd_parser.add_argument("cmd", help = "Command")
    cmd_parser.add_argument("args", help = "Arguments", nargs='*')

    # Read Wattpilot config:

    wattpilotAPIDesc = pkgutil.get_data(__name__, "ressources/wattpilot.yaml")
    #wattpilotAPIDesc = "wattpilot.yaml"


    try:
        wpi=yaml.safe_load(wattpilotAPIDesc)
        wpi_messages = dict(zip(
            [x["key"] for x in wpi["messages"]],
            [x for x in wpi["messages"]],
        ))
        wpi_properties = dict(zip(
            [x["key"] for x in wpi["properties"]],
            [x for x in wpi["properties"]],
        ))
    except yaml.YAMLError as exc:
        print(exc)

    # Connect to Wattpilot:
    ip = args.ip or os.environ.get('WATTPILOT_HOST')
    password = args.password or os.environ.get('WATTPILOT_PASSWORD')
    wp = wattpilot.Wattpilot(ip,password)

    # Enable MQTT integration:
    if MQTT_ENABLED == "true":
        _LOGGER.debug(f"Registering message callback for MQTT integration.")
        wp.register_message_callback(mqtt_message)
    wp.connect()

    # Wait for connection and initializon:
    wait_timeout(lambda: wp.connected, WATTPILOT_CONNECT_TIMEOUT) or exit("ERROR: Timeout while connecting to Wattpilot!")
    wait_timeout(lambda: wp.allPropsInitialized, WATTPILOT_INITIALIZED_TIMEOUT) or exit("ERROR: Timeout while waiting for property initialization!")

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


if __name__ == '__main__':
    main()

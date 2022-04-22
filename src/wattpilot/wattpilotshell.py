import argparse
import json
import logging
import math
import os
import paho.mqtt.client as mqtt
import re
import readline
import wattpilot
import yaml
import pkgutil

from ast import arg
from enum import Enum
from time import sleep
from threading import Event
from types import SimpleNamespace
from typing import Any, Callable, List

_LOGGER = logging.getLogger(__name__)


#### Utility Functions ####

def utils_add_to_dict_unique(d, k, v):
    if k in d:
        _LOGGER.warning(
            f"About to add duplicate key {k} to dictionary - skipping!")
    else:
        d[k] = v
    return d


def utils_wait_timeout(fn, timeout):
    """Generic timeout waiter"""
    t = 0
    within_timeout = True
    while not fn() and t < timeout:
        sleep(1)
        t += 1
    if t >= timeout:
        within_timeout = False
    return within_timeout


class JSONNamespaceEncoder(json.JSONEncoder):
    # See https://gist.github.com/jdthorpe/313cafc6bdaedfbc7d8c32fcef799fbf
    def default(self, obj):
        if isinstance(obj, SimpleNamespace):
            return obj.__dict__
        return super(JSONNamespaceEncoder, self).default(obj)


def utils_value2json(value):
    return json.dumps(value, cls=JSONNamespaceEncoder)


#### Wattpilot Functions ####

def wp_read_config():
    api_definition = pkgutil.get_data(__name__, "ressources/wattpilot.yaml")
    wpcfg = {}
    try:
        wpcfg["config"] = yaml.safe_load(api_definition)
        wpcfg["messages"] = dict(zip(
            [x["key"] for x in wpcfg["config"]["messages"]],
            [x for x in wpcfg["config"]["messages"]],
        ))
        wpcfg["properties"] = {}
        for p in wpcfg["config"]["properties"]:
            wpcfg["properties"] = utils_add_to_dict_unique(
                wpcfg["properties"], p["key"], p)
            if "childProps" in p:
                for cp in p["childProps"]:
                    cp["compoundProperty"] = p["key"]
                    wpcfg["properties"] = utils_add_to_dict_unique(
                        wpcfg["properties"], cp["key"], cp)
        _LOGGER.debug(
            f"Resulting properties config:\n{utils_value2json(wpcfg['properties'])}")
    except yaml.YAMLError as exc:
        print(exc)
    return wpcfg


def wp_initialize(host, password):
    # Connect to Wattpilot:
    wp = wattpilot.Wattpilot(host, password)
    wp.connect()
    # Wait for connection and initialization:
    utils_wait_timeout(lambda: wp.connected, WATTPILOT_CONNECT_TIMEOUT) or exit(
        "ERROR: Timeout while connecting to Wattpilot!")
    utils_wait_timeout(lambda: wp.allPropsInitialized, WATTPILOT_INIT_TIMEOUT) or exit(
        "ERROR: Timeout while waiting for property initialization!")
    return wp


#### Shell Functions ####

def shell_print_prop_info(wp_propdef, prop_name, value):
    pd = wp_propdef[prop_name]
    _LOGGER.debug(f"Property info: {pd}")
    title = ""
    desc = ""
    alias = ""
    rw = ""
    if 'rw' in pd:
        rw = f", rw:{pd['rw']}"
    if 'alias' in pd:
        alias = f", alias:{pd['alias']}"
    if 'title' in pd:
        title = pd['title']
    if 'description' in pd:
        desc = pd['description']
    print(f"- {prop_name} ({pd['jsonType']}{rw}{alias}): {title}")
    print(f"  Raw Value: {utils_value2json(value)}")
    if "valueMap" in pd:
        print(f"  Mapped Value: {mqtt_get_encoded_property(pd,value)}")
    if desc:
        print(f"  Description: {desc}")
    if 'itemType' in pd:
        print(f"  Array item type: {pd['itemType']}")
    if 'min' in pd:
        print(f"  Minimum value: {pd['min']}")
    if 'max' in pd:
        print(f"  Maximum value: {pd['max']}")
    if 'example' in pd:
        print(f"  Example: {utils_value2json(pd['example'])}")


def shell_watched_property_changed(name, value):
    global wp_propdef
    global shell_watching_properties
    if name in shell_watching_properties:
        pd = wp_propdef[name]
        _LOGGER.info(
            f"Property {name} changed to {mqtt_get_encoded_property(pd,value)}")


def shell_watched_message_received(wp, wsapp, msg, msg_json):
    global shell_watching_messages
    if msg.type in shell_watching_messages:
        _LOGGER.info(f"Message of type {msg.type} received: {msg}")


def shell_cmd_exit(wp, args):
    return True


def shell_cmd_get(wp, args):
    global wp_propdef
    if len(args) != 1:
        _LOGGER.error(f"Wrong number of arguments: get <property>")
    elif args[0] not in wp.allProps:
        _LOGGER.error(f"Unknown property: {args[0]}")
    else:
        pd = wp_propdef[args[0]]
        print(mqtt_get_encoded_property(pd, wp.allProps[args[0]]))


def shell_cmd_ha(wp, args):
    global HA_ENABLED
    global HA_PROPERTIES
    global mqtt_client
    if len(args) != 1:
        _LOGGER.error(
            f"Wrong number of arguments: {ShellCommand.HA.value.help()}")
        return
    if args[0] == "start":
        HA_ENABLED = 'true'
        mqtt_client = ha_setup(wp)
    elif args[0] == "stop":
        ha_stop(mqtt_client)
        HA_ENABLED = 'false'
    elif args[0] == "status":
        print(
            f"HA discovery is {'enabled' if HA_ENABLED == 'true' else 'disabled'}.")
    else:
        _LOGGER.error(f"Unsupported argument: {args[0]}")


def shell_cmd_help(wp, args):
    print("Wattpilot Shell Commands:")
    for cmd_desc in list(ShellCommand):
        c = cmd_desc.value
        print(f"  {c.help()}")


def shell_cmd_info(wp, args):
    print(wp)


def shell_cmd_mqtt(wp, args):
    global mqtt_client
    global MQTT_ENABLED
    if len(args) != 1:
        _LOGGER.error(
            f"Wrong number of arguments: {ShellCommand.MQTT.value.help()}")
        return
    if args[0] == "start":
        MQTT_ENABLED = 'true'
        mqtt_client = mqtt_setup(wp)
    elif args[0] == "stop":
        mqtt_stop(mqtt_client)
        MQTT_ENABLED = 'false'
    elif args[0] == "status":
        print(
            f"MQTT client is {'enabled' if MQTT_ENABLED == 'true' else 'disabled'}.")
    else:
        _LOGGER.error(f"Unsupported argument: {args[0]}")


def shell_cmd_properties(wp, args):
    global wpcfg
    print(f"Properties:")
    props = shell_get_props_matching_regex(wp, args)
    for pd, value in sorted(props.items()):
        shell_print_prop_info(wpcfg["properties"], pd, value)
    print()


def shell_cmd_server(wp, args):
    _LOGGER.info("Server started.")
    Event().wait()


def shell_cmd_set(wp, args):
    global wp_propdef
    if len(args) != 2:
        _LOGGER.error(f"Wrong number of arguments: set <property> <value>")
    elif args[0] not in wp.allProps:
        _LOGGER.error(f"Unknown property: {args[0]}")
    else:
        if args[1].lower() in ["false", "true"]:
            v = json.loads(args[1].lower())
        elif str(args[1]).isnumeric():
            v = int(args[1])
        elif str(args[1]).isdecimal():
            v = float(args[1])
        else:
            v = str(args[1])
        wp.send_update(args[0], mqtt_get_decoded_property(
            wp_propdef[args[0]], v))


def shell_cmd_values(wp, args):
    global wpcfg
    print(f"List mapped values of available properties:")
    props = shell_get_props_matching_regex(wp, args)
    for pd, value in sorted(props.items()):
        print(
            f"- {pd}: {mqtt_get_encoded_property(wpcfg['properties'][pd],value)}")
    print()


def shell_cmd_values_raw(wp, args):
    print(f"List raw values of available properties:")
    props = shell_get_props_matching_regex(wp, args)
    for pd, value in sorted(props.items()):
        print(f"- {pd}: {utils_value2json(value)}")
    print()


def shell_watch_message(wp, name):
    global shell_watching_messages
    if len(shell_watching_messages) == 0:
        wp.register_message_callback(shell_watched_message_received)
    if name not in shell_watching_messages:
        shell_watching_messages.append(name)


def shell_watch_property(wp, name):
    global shell_watching_properties
    if len(shell_watching_properties) == 0:
        wp.register_property_callback(shell_watched_property_changed)
    if name not in shell_watching_properties:
        shell_watching_properties.append(name)


def shell_cmd_watch_message(wp, args):
    global wpcfg
    if len(args) != 1:
        _LOGGER.error(f"Wrong number of arguments!")
    elif args[0] not in wpcfg['messages']:
        _LOGGER.error(f"Unknown message type: {args[0]}")
    else:
        shell_watch_message(wp, args[0])


def shell_cmd_watch_property(wp, args):
    if len(args) != 1:
        _LOGGER.error(f"Wrong number of arguments!")
    elif args[0] not in wp.allProps:
        _LOGGER.error(f"Unknown property: {args[0]}")
    else:
        shell_watch_property(wp, args[0])


def shell_cmd_unwatch_message(wp, args):
    global shell_watching_messages
    if len(args) != 1:
        _LOGGER.error(f"Wrong number of arguments!")
    elif args[0] not in shell_watching_messages:
        _LOGGER.warning(f"Message of type '{args[0]}' is not watched")
    else:
        shell_watching_messages.remove(args[0])
        if len(shell_watching_messages) == 0:
            wp.unregister_message_callback()


def shell_cmd_unwatch_property(wp, args):
    global shell_watching_properties
    if len(args) != 1:
        _LOGGER.error(f"Wrong number of arguments!")
    elif args[0] not in shell_watching_properties:
        _LOGGER.warning(f"Property with name '{args[0]}' is not watched")
    else:
        shell_watching_properties.remove(args[0])
        if len(shell_watching_properties) == 0:
            wp.unregister_property_callback()


def shell_get_props_matching_regex(wp, args):
    global wp_propdef
    prop_regex = '.*'
    if len(args) > 0:
        prop_regex = args[0]
    props = {k: v for k, v in wp.allProps.items() if re.match(
        r'^'+prop_regex+'$', k, flags=re.IGNORECASE)}
    value_regex = '.*'
    if len(args) > 1:
        value_regex = args[1]
    props = {k: v for k, v in props.items() if re.match(r'^'+value_regex+'$',
                                                        str(mqtt_get_encoded_property(wp_propdef[k], v)), flags=re.IGNORECASE)}
    return props


class CmdDesc():
    def __init__(self, name, args, desc, fn: Callable[[wattpilot.Wattpilot, List[str]], bool] = None):
        self.name = name
        self.args = args
        self.desc = desc
        self.execute = fn

    def help(self):
        return f"{self.name}{(' ' + self.args) if self.args else ''}: {self.desc}"


class ShellCommand(Enum):
    EXIT = CmdDesc('exit', '', 'Exit the shell', shell_cmd_exit)
    GET = CmdDesc('get', '<propName>', 'Get a property value', shell_cmd_get)
    HA = CmdDesc('ha', '<start|status|stop>',
                 'Control Home Assistant discovery (+MQTT client)', shell_cmd_ha)
    HELP = CmdDesc('help', '', 'This help message', shell_cmd_help)
    INFO = CmdDesc('info', '', 'Print device infos', shell_cmd_info)
    MQTT = CmdDesc('mqtt', '<start|status|stop>',
                   'Control MQTT support', shell_cmd_mqtt)
    PROPERTIES = CmdDesc(
        'properties', '[nameRegex]', 'List property definitions and values', shell_cmd_properties)
    SERVER = CmdDesc(
        'server', '', 'Start in server mode (infinite wait loop)', shell_cmd_server)
    SET = CmdDesc('set', '<propName> <value>',
                  'Set a property value', shell_cmd_set)
    UNWATCH_MESSAGE = CmdDesc(
        'unwatch-message', '<msgType>', 'Unwatch message of given message type', shell_cmd_unwatch_message)
    UNWATCH_PROPERTY = CmdDesc(
        'unwatch-property', '<propName>', 'Unwatch value changes of given property name', shell_cmd_unwatch_property)
    VALUES = CmdDesc('values', '[propRegex] [valueRegex]',
                     'List values of properties (with value mapping enabled)', shell_cmd_values)
    VALUES_RAW = CmdDesc(
        'values-raw', '', 'List raw values of properties (without value mapping)', shell_cmd_values_raw)
    WATCH_MESSAGE = CmdDesc('watch-message', '<msgType>',
                            'Watch message of given message type', shell_cmd_watch_message)
    WATCH_PROPERTY = CmdDesc(
        'watch-property', '<propName>', 'Watch value changes of given property name', shell_cmd_watch_property)

    @staticmethod
    def from_name(name: str):
        for cmd in list(ShellCommand):
            if cmd.value.name == name:
                return cmd
        return None


def shell_process_command(wp, wpcfg, cmdline):
    """Process a Wattpilot shell command"""
    #global wp_propdef
    # Wattpilot shell command parser:
    cmd_parser = argparse.ArgumentParser()
    cmd_parser.add_argument("cmd", help="Command")
    cmd_parser.add_argument("args", help="Arguments", nargs='*')

    exit = False
    cmd_args = cmd_parser.parse_args(args=cmdline.strip().split(' '))
    cmd = cmd_args.cmd.strip()
    args = cmd_args.args
    if (cmd == ''):
        # Don't do anything
        exit = False
    elif ShellCommand.from_name(cmd):
        exit = ShellCommand.from_name(cmd).value.execute(wp, args)
    else:
        print(f"Unknown command: {cmd}")
    return exit


def shell_complete(text, state):
    """Simple readline completer"""
    vocab = [x.value for x in list(ShellCommand)]
    results = [x for x in vocab if x.startswith(text)] + [None]
    return results[state]


def shell_setup():
    global wp
    # Setup readline
    readline.parse_and_bind("tab: complete")
    readline.set_completer(shell_complete)
    # Commandline argument parser:
    parser = argparse.ArgumentParser()
    parser.add_argument("cmdline", help="Optional shell command", nargs="?")
    args = parser.parse_args()
    return args


def shell_start(wp, wpcfg, args):
    # Process commands:
    if args.cmdline:
        # Process commands passed on the commandline
        shell_process_command(wp, wpcfg, args.cmdline)
    else:
        # Start interactive shell
        shell_process_command(wp, wpcfg, "info")
        exit = False
        while not exit:
            try:
                command = input('> ')
            except EOFError:
                command = "exit"
                print()
            exit = shell_process_command(wp, wpcfg, command)


#### MQTT Functions ####

def mqtt_get_mapped_value(pd, value):
    mapped_value = value
    if "valueMap" in pd:
        if str(value) in list(pd["valueMap"].keys()):
            mapped_value = pd["valueMap"][str(value)]
        else:
            _LOGGER.warning(
                f"Unable to map value '{value}' of property '{pd['key']} - using unmapped value!")
    return mapped_value


def mqtt_get_mapped_property(pd, value):
    if "jsonType" in pd and pd["jsonType"] == "array":
        mapped_value = []
        for v in value:
            mapped_value.append(mqtt_get_mapped_value(pd, v))
    else:
        mapped_value = mqtt_get_mapped_value(pd, value)
    return mapped_value


def mqtt_get_remapped_value(pd, mapped_value):
    remapped_value = mapped_value
    if "valueMap" in pd:
        if mapped_value in pd["valueMap"].values():
            remapped_value = json.loads(str(list(pd["valueMap"].keys())[
                                        list(pd["valueMap"].values()).index(mapped_value)]))
        else:
            _LOGGER.warning(
                f"Unable to remap value '{mapped_value}' of property '{pd['key']} - using mapped value!")
    return remapped_value


def mqtt_get_remapped_property(pd, mapped_value):
    if "jsonType" in pd and pd["jsonType"] == "array":
        remapped_value = []
        for v in mapped_value:
            remapped_value.append(mqtt_get_remapped_value(pd, v))
    else:
        remapped_value = mqtt_get_remapped_value(pd, mapped_value)
    return remapped_value


def mqtt_get_encoded_property(pd, value):
    mapped_value = mqtt_get_mapped_property(pd, value)
    if "jsonType" in pd and (
            pd["jsonType"] == "array"
            or pd["jsonType"] == "object"
            or pd["jsonType"] == "boolean"):
        return json.dumps(mapped_value, cls=JSONNamespaceEncoder)
    else:
        return mapped_value


def mqtt_get_decoded_property(pd, value):
    if "jsonType" in pd and (pd["jsonType"] == "array" or pd["jsonType"] == "object"):
        decoded_value = json.loads(value)
    else:
        decoded_value = value
    return mqtt_get_remapped_property(pd, decoded_value)

# Publish a property value change from wattpilot to MQTT


def mqtt_publish_property(wp, mqtt_client, pd, value, force_publish=False):
    prop_name = pd["key"]
    if not (force_publish or MQTT_PROPERTIES == [''] or prop_name in MQTT_PROPERTIES):
        _LOGGER.debug(f"Skipping publishing of property '{prop_name}' ...")
        return
    property_topic = mqtt_subst_topic(MQTT_TOPIC_PROPERTY_STATE, {
        "baseTopic": MQTT_TOPIC_BASE,
        "serialNumber": wp.serial,
        "propName": prop_name,
    })
    encoded_value = mqtt_get_encoded_property(pd, value)
    _LOGGER.debug(
        f"Publishing property '{prop_name}' with value '{encoded_value}' to MQTT ...")
    mqtt_client.publish(property_topic, encoded_value)
    if MQTT_DECOMPOSE_PROPERTIES and "childProps" in pd:
        _LOGGER.debug(
            f"Splitting child props of property {prop_name} as {pd['jsonType']} for value {value} ...")
        for p in pd["childProps"]:
            _LOGGER.debug(f"Extracting child property {p['key']},  ...")
            if pd["jsonType"] == "array":
                v = value[int(p["valueRef"])]
                _LOGGER.debug(f"  -> got array value {v}")
            elif pd["jsonType"] == "object" and p["valueRef"] in value.__dict__:
                v = value.__dict__[p["valueRef"]]
                _LOGGER.debug(f"  -> got object value {v}")
            else:
                continue
            _LOGGER.debug(
                f"Publishing sub-property {p['key']} with value {v} to MQTT ...")
            mqtt_publish_property(wp, mqtt_client, p, v, True)

# Publish a message received from wattpilot to MQTT


def mqtt_publish_message(wp, wsapp, msg, msg_json):
    global mqtt_client
    global MQTT_PUBLISH_MESSAGES
    global MQTT_TOPIC_BASE
    global MQTT_PUBLISH_PROPERTIES
    global MQTT_TOPIC_MESSAGES
    if mqtt_client == None:
        _LOGGER.debug(f"Skipping MQTT message publishing.")
        return
    if msg.type not in ["fullStatus", "deltaStatus"]:
        _LOGGER.debug(f"Skipping MQTT message publishing of type {msg.type}.")
        return
    msg_dict = json.loads(msg_json)
    if MQTT_PUBLISH_MESSAGES == "true":
        message_topic = mqtt_subst_topic(MQTT_TOPIC_MESSAGES, {
            "baseTopic": MQTT_TOPIC_BASE,
            "serialNumber": wp.serial,
            "messageType": msg.type,
        })
        mqtt_client.publish(message_topic, msg_json)
    if MQTT_PUBLISH_PROPERTIES == "true":
        for prop_name, value in msg_dict["status"].items():
            pd = wp_propdef[prop_name]
            mqtt_publish_property(wp, mqtt_client, pd, value)

# Substitute topic patterns


def mqtt_subst_topic(s, values, expand=True):
    if expand:
        s = re.sub(r'^~', MQTT_TOPIC_PROPERTY_BASE, s)
    all_values = {
        "baseTopic": MQTT_TOPIC_BASE,
    } | values
    return s.format(**all_values)


def mqtt_setup_client(host, port, client_id, command_topic):
    # Connect to MQTT server:
    mqtt_client = mqtt.Client(client_id)
    mqtt_client.on_message = mqtt_set_value
    _LOGGER.info(f"Connecting to MQTT host {host} on port {port} ...")
    mqtt_client.connect(host, port)
    mqtt_client.loop_start()
    _LOGGER.info(f"Subscribing to command topics {command_topic}")
    mqtt_client.subscribe(command_topic)
    return mqtt_client


def mqtt_setup(wp):
    global MQTT_CLIENT_ID
    global MQTT_HOST
    global MQTT_PORT
    global MQTT_PROPERTIES
    global MQTT_TOPIC_PROPERTY_SET
    # Connect to MQTT server:
    mqtt_client = mqtt_setup_client(MQTT_HOST, MQTT_PORT, MQTT_CLIENT_ID, mqtt_subst_topic(
        MQTT_TOPIC_PROPERTY_SET, {"propName": "+"}))
    MQTT_PROPERTIES = mqtt_get_watched_properties(wp)
    _LOGGER.info(
        f"Registering message callback to publish updates to the following properties to MQTT: {MQTT_PROPERTIES}")
    wp.register_message_callback(mqtt_publish_message)
    return mqtt_client


def mqtt_stop(mqtt_client):
    if mqtt_client.is_connected():
        _LOGGER.info(f"Disconnecting from MQTT server ...")
        mqtt_client.disconnect()

# Subscribe to topic for setting property values:


def mqtt_set_value(client, userdata, message):
    topic_regex = mqtt_subst_topic(
        MQTT_TOPIC_PROPERTY_SET, {"propName": "([^/]+)"})
    name = re.sub(topic_regex, r'\1', message.topic)
    if not name or name == "" or not wp_propdef[name]:
        _LOGGER.warning(f"Unknown property '{name}'!")
    pd = wp_propdef[name]
    if pd['rw'] == "R":
        _LOGGER.warning(f"Property '{name}' is not writable!")
    value = mqtt_get_decoded_property(
        pd, str(message.payload.decode("utf-8")))
    _LOGGER.info(
        f"MQTT Message received: topic={message.topic}, name={name}, value={value}")
    wp.send_update(name, value)


def mqtt_get_watched_properties(wp):
    global MQTT_PROPERTIES
    if MQTT_PROPERTIES == [] or MQTT_PROPERTIES == ['']:
        return list(wp.allProps.keys())
    else:
        return MQTT_PROPERTIES


#### Home Assistant Functions ####

# Generate device information for HA discovery
def ha_get_device_info(wp):
    ha_device = {
        "connections": [
        ],
        "identifiers": [
            f"wattpilot_{wp.serial}",
        ],
        "manufacturer": wp.manufacturer,
        "model": wp.devicetype,
        "name": wp.name,
        "suggested_area": "Garage",
        "sw_version": wp.version,
    }
    if "maca" in wp.allProps:
        ha_device["connections"] += [["mac", wp.allProps["maca"]]]
    if "macs" in wp.allProps:
        ha_device["connections"] += [["mac", wp.allProps["macs"]]]
    return ha_device


def ha_get_component_for_prop(prop_info):
    component = "sensor"
    if "rw" in prop_info and prop_info["rw"] == "R/W":
        if "valueMap" in prop_info:
            component = "select"
        elif "jsonType" in prop_info and prop_info["jsonType"] == "boolean":
            component = "switch"
        elif "jsonType" in prop_info and prop_info["jsonType"] == "float":
            component = "number"
        elif "jsonType" in prop_info and prop_info["jsonType"] == "integer":
            component = "number"
    elif "rw" in prop_info and prop_info["rw"] == "R":
        if "jsonType" in prop_info and prop_info["jsonType"] == "boolean":
            component = "binary_sensor"
    return component


def ha_get_default_config_for_prop(prop_info):
    config = {}
    if "rw" in prop_info and prop_info["rw"] == "R/W" and \
        "jsonType" in prop_info and \
            (prop_info["jsonType"] == "float" or prop_info["jsonType"] == "integer"):
        config["mode"] = "box"
    if "homeAssistant" not in prop_info:
        config["enabled_by_default"] = False
    return config


def ha_get_template_filter_from_json_type(json_type):
    template = "{{ value | string }}"
    if json_type == "float":
        template = "{{ value | float }}"
    elif json_type == "integer":
        template = "{{ value | int }}"
    elif json_type == "boolean":
        template = "{{ value == 'true' }}"
    return template

# Publish HA discovery config for a single property


def ha_discover_property(wp, mqtt_client, pd, disable_discovery=False):
    global HA_TOPIC_CONFIG
    global MQTT_DECOMPOSE_PROPERTIES
    global MQTT_TOPIC_PROPERTY_BASE
    global MQTT_TOPIC_PROPERTY_SET
    global MQTT_TOPIC_PROPERTY_STATE
    name = pd["key"]
    ha_info = {}
    if "homeAssistant" in pd:
        ha_info = pd["homeAssistant"] or {}
    component = ha_get_component_for_prop(pd)
    if "component" in ha_info:  # Override component from config
        component = ha_info["component"]
    _LOGGER.debug(
        f"Homeassistant config: haInfo={ha_info}, component={component}")
    title = pd.get("title", pd.get("alias", name))
    _LOGGER.debug(
        f"Publishing HA discovery config for property '{name}' ...")
    ha_config = ha_info.get("config", {})
    unique_id = f"wattpilot_{wp.serial}_{name}"
    object_id = f"wattpilot_{name}"
    topic_subst_map = {
        "component": component,
        "propName": name,
        "serialNumber": wp.serial,
        "uniqueId": unique_id,
    }
    ha_device = ha_get_device_info(wp)
    base_topic = mqtt_subst_topic(
        MQTT_TOPIC_PROPERTY_BASE, topic_subst_map, False)
    ha_discovery_config = ha_get_default_config_for_prop(pd) | {
        "~": base_topic,
        "name": title,
        "object_id": object_id,
        "unique_id": unique_id,
        "state_topic": mqtt_subst_topic(MQTT_TOPIC_PROPERTY_STATE, topic_subst_map, False),
        "device": ha_device,
    }
    if "valueMap" in pd:
        ha_discovery_config["options"] = list(pd["valueMap"].values())
    if pd.get("rw", "") == "R/W":
        ha_discovery_config["command_topic"] = mqtt_subst_topic(
            MQTT_TOPIC_PROPERTY_SET, topic_subst_map, False)
    ha_discovery_config = dict(
        list(ha_discovery_config.items())
        + list(ha_config.items())
    )
    topic_cfg = mqtt_subst_topic(HA_TOPIC_CONFIG, topic_subst_map)
    if disable_discovery:
        payload = ''
    else:
        payload = utils_value2json(ha_discovery_config)
    _LOGGER.debug(
        f"Publishing property '{name}' to {topic_cfg}: {payload}")
    mqtt_client.publish(topic_cfg, payload, retain=True)
    if MQTT_DECOMPOSE_PROPERTIES and "childProps" in pd:
        for p in pd["childProps"]:
            ha_discover_property(wp, mqtt_client, p, disable_discovery)


def ha_get_discovery_properties():
    global HA_PROPERTIES
    global wp_propdef
    _LOGGER.debug(
        f"get_ha_discovery_properties(): HA_PROPERTIES='{HA_PROPERTIES}', wp_propdef size='{len(wp_propdef)}'")
    ha_properties = HA_PROPERTIES
    if ha_properties == [''] or ha_properties == []:
        ha_properties = [p["key"]
                         for p in wp_propdef.values() if "homeAssistant" in p]
    _LOGGER.debug(
        f"get_ha_discovery_properties(): ha_properties='{ha_properties}'")
    return ha_properties


def ha_discover_properties(mqtt_client, ha_properties, disable_discovery=True):
    global wpcfg
    _LOGGER.info(
        f"{'Disabling' if disable_discovery else 'Enabling'} HA discovery for the following properties: {ha_properties}")
    for name in ha_properties:
        ha_discover_property(
            wp, mqtt_client, wpcfg["properties"][name], disable_discovery)


def ha_publish_initial_properties(wp, mqtt_client):
    global HA_PROPERTIES
    _LOGGER.info(
        f"Publishing all initial property values to MQTT to populate the entity values ...")
    for prop_name in HA_PROPERTIES:
        if prop_name in wp.allProps:
            value = wp.allProps[prop_name]
            pd = wp_propdef[prop_name]
            mqtt_publish_property(wp, mqtt_client, pd, value)


def ha_setup(wp):
    global HA_PROPERTIES
    global HA_WAIT_INIT_S
    global HA_WAIT_PROPS_MS
    global MQTT_PROPERTIES
    global wp_propdef
    # Configure list of relevant properties:
    HA_PROPERTIES = ha_get_discovery_properties()
    if MQTT_PROPERTIES == [] or MQTT_PROPERTIES == ['']:
        MQTT_PROPERTIES = HA_PROPERTIES
    # Setup MQTT client:
    mqtt_client = mqtt_setup(wp)
    # Publish HA discovery config:
    ha_discover_properties(mqtt_client, HA_PROPERTIES, False)
    # Wait a bit for HA to catch up:
    wait_time = math.ceil(
        HA_WAIT_INIT_S + len(HA_PROPERTIES)*HA_WAIT_PROPS_MS*0.001)
    _LOGGER.info(
        f"Waiting {wait_time}s to allow Home Assistant to discovery entities and subscribe MQTT topics before publishing initial values ...")
    # Sleep to let HA discover the entities before publishing values
    sleep(wait_time)
    # Publish initial property values to MQTT:
    ha_publish_initial_properties(wp, mqtt_client)
    return mqtt_client


def ha_stop(mqtt_client):
    global HA_PROPERTIES
    ha_discover_properties(mqtt_client, HA_PROPERTIES, True)
    mqtt_stop(mqtt_client)


#### Main Program ####

def main_setup_env():
    global HA_ENABLED
    global HA_PROPERTIES
    global HA_TOPIC_CONFIG
    global HA_WAIT_INIT_S
    global HA_WAIT_PROPS_MS
    global MQTT_CLIENT_ID
    global MQTT_DECOMPOSE_PROPERTIES
    global MQTT_ENABLED
    global MQTT_HOST
    global MQTT_PORT
    global MQTT_PROPERTIES
    global MQTT_PUBLISH_MESSAGES
    global MQTT_PUBLISH_PROPERTIES
    global MQTT_TOPIC_BASE
    global MQTT_TOPIC_MESSAGES
    global MQTT_TOPIC_PROPERTY_BASE
    global MQTT_TOPIC_PROPERTY_SET
    global MQTT_TOPIC_PROPERTY_STATE
    global WATTPILOT_CONNECT_TIMEOUT
    global WATTPILOT_DEBUG_LEVEL
    global WATTPILOT_HOST
    global WATTPILOT_INIT_TIMEOUT
    global WATTPILOT_PASSWORD
    HA_ENABLED = os.environ.get('HA_ENABLED', 'false')
    HA_PROPERTIES = os.environ.get('HA_PROPERTIES', '').split(sep=' ')
    HA_TOPIC_CONFIG = os.environ.get(
        'HA_TOPIC_CONFIG', 'homeassistant/{component}/{uniqueId}/config')
    HA_WAIT_INIT_S = int(os.environ.get('HA_WAIT_INIT_S', '5'))
    HA_WAIT_PROPS_MS = int(os.environ.get('HA_WAIT_PROPS_MS', '50'))
    MQTT_CLIENT_ID = os.environ.get('MQTT_CLIENT_ID', 'wattpilot2mqtt')
    MQTT_DECOMPOSE_PROPERTIES = bool(
        os.environ.get('MQTT_DECOMPOSE_PROPERTIES', 'true'))
    MQTT_ENABLED = os.environ.get('MQTT_ENABLED', 'false')
    MQTT_HOST = os.environ.get('MQTT_HOST', '')
    MQTT_PORT = int(os.environ.get('MQTT_PORT', '1883'))
    MQTT_PROPERTIES = os.environ.get('MQTT_PROPERTIES', '').split(sep=' ')
    MQTT_PUBLISH_MESSAGES = os.environ.get('MQTT_PUBLISH_MESSAGES', 'false')
    MQTT_PUBLISH_PROPERTIES = os.environ.get('MQTT_PUBLISH_PROPERTIES', 'true')
    MQTT_TOPIC_BASE = os.environ.get('MQTT_TOPIC_BASE', 'wattpilot')
    MQTT_TOPIC_MESSAGES = os.environ.get(
        'MQTT_TOPIC_MESSAGES', '{baseTopic}/messages/{messageType}')
    MQTT_TOPIC_PROPERTY_BASE = os.environ.get(
        'MQTT_TOPIC_PROPERTY_BASE', '{baseTopic}/properties/{propName}')
    MQTT_TOPIC_PROPERTY_SET = os.environ.get(
        'MQTT_TOPIC_PROPERTY_SET', '~/set')
    MQTT_TOPIC_PROPERTY_STATE = os.environ.get(
        'MQTT_TOPIC_PROPERTY_STATE', '~/state')
    WATTPILOT_CONNECT_TIMEOUT = int(
        os.environ.get('WATTPILOT_CONNECT_TIMEOUT', '30'))
    WATTPILOT_DEBUG_LEVEL = os.environ.get('WATTPILOT_DEBUG_LEVEL', 'INFO')
    WATTPILOT_HOST = os.environ.get('WATTPILOT_HOST', '')
    WATTPILOT_INIT_TIMEOUT = int(
        os.environ.get('WATTPILOT_INIT_TIMEOUT', '30'))
    WATTPILOT_PASSWORD = os.environ.get('WATTPILOT_PASSWORD', '')


def main():
    global WATTPILOT_HOST
    global WATTPILOT_PASSWORD
    global MQTT_ENABLED
    global MQTT_HOST
    global WATTPILOT_DEBUG_LEVEL
    global shell_watching_properties
    global shell_watching_messages
    global mqtt_client
    global wp
    global wp_propdef
    global wpcfg

    main_setup_env()

    # Ensure wattpilot host an password are set:
    assert WATTPILOT_HOST != '', "WATTPILOT_HOST not set!"
    assert WATTPILOT_PASSWORD != '', "WATTPILOT_PASSWORD not set!"
    assert MQTT_ENABLED == 'false' or MQTT_HOST != '', 'MQTT_HOST not set!'

    # Set debug level:
    logging.basicConfig(level=WATTPILOT_DEBUG_LEVEL)

    # Read config:
    wpcfg = wp_read_config()
    wp_propdef = wpcfg["properties"]

    # Initialize globals:
    shell_watching_properties = []
    shell_watching_messages = []
    mqtt_client = None

    args = shell_setup()
    wp = wp_initialize(WATTPILOT_HOST, WATTPILOT_PASSWORD)

    # Enable MQTT and/or HA integration:
    if MQTT_ENABLED == "true" and HA_ENABLED == "false":
        mqtt_client = mqtt_setup(wp)
    elif MQTT_ENABLED == "true" and HA_ENABLED == "true":
        mqtt_client = ha_setup(wp)

    shell_start(wp, wpcfg, args)


if __name__ == '__main__':
    main()

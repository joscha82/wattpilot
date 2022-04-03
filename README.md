# Wattpilot

### This project is still in early development and might never leave this state

`wattpilot` is a Python 3 (>= 3.9) module to interact with Fronius Wattpilot wallboxes which do not support (at the time of writting) a documented API. This functionality of this module utilized a undocumented websockets API, which is also utilized by the official Wattpilot.Solar mobile app.

## Wattpilot Shell

The shell provides an easy way to explore the available properties and get or set their values.

```bash
# Install the wattpilot module, if not yet done so:
pip install .
```

Run the interactive shell

```bash
# Usage:
python3 shell.py <wattpilot_ip> <password>
> help
Wattpilot Shell Commands:
  dump: Dump all property values
  exit: Exit the shell
  get <name>: Get a property value
  info: Print most important infos
  list [propsearch]: List all properties (starting with propsearch if given)
  mqtt-connect <host> <port>: Connect to MQTT server
  mqtt-disconnect: Disconnect from MQTT server
  set <name> <value>: Set a property value
  watch message <type>: Watch message of given message type
  watch property <name>: Watch value changes of given property name
  unwatch message <type>: Unwatch messages of given message type
  unwatch property <name>: Unwatch value changes of given property name
```

It's also possible to pass a single command to the shell to integrate it into scripts:

```bash
# Usage:
python3 shell.py <wattpilot_ip> <password> "<command> <args...>"

# Examples:
python3 shell.py <wattpilot_ip> <password> "get amp"
python3 shell.py <wattpilot_ip> <password> "set amp 6"
```

## Environment Variables

| Environment Variable             | Description                                                                                   | Default Value                                        |
| -------------------------------- | --------------------------------------------------------------------------------------------- | ---------------------------------------------------- |
| MQTT_BASE_TOPIC                  | Base topic for MQTT                                                                           | wattpilot                                            |
| MQTT_CLIENT_ID                   | MQTT client ID                                                                                | wattpilot2mqtt                                       |
| MQTT_ENABLED                     | Enable MQTT                                                                                   | false                                                |
| MQTT_HA_DISCOVERY_ENABLED        | Enable Home Assistant Discovery (not yet implemented)                                         | false                                                |
| MQTT_HOST                        | MQTT host to connect to                                                                       |                                                      |
| MQTT_MESSAGE_TOPIC_PATTERN       | Topic pattern to publish Wattpilot messages to                                                | {baseTopic}/{serialNumber}/messages/{messageType}    |
| MQTT_PORT                        | Port of the MQTT host to connect to                                                           | 1883                                                 |
| MQTT_PROPERTY_READ_TOPIC_PATTERN | Topic pattern to publish property values to                                                   | {baseTopic}/{serialNumber}/properties/{propName}     |
| MQTT_PROPERTY_SET_TOPIC_PATTERN  | Topic pattern to listen for property value changes for (not yet implemented)                  | {baseTopic}/{serialNumber}/properties/{propName}/set |
| MQTT_PUBLISH_MESSAGES            | Publish received Wattpilot messages to MQTT                                                   | true                                                 |
| MQTT_PUBLISH_PROPERTIES          | Publish received property values to MQTT                                                      | false                                                |
| MQTT_WATCH_PROPERTIES            | List of space-separated default properties to publish changes for (use "" for all properties) | amp car fna lmo sse                                  |
| WATTPILOT_CONNECT_TIMEOUT        | Connect timeout for Wattpilot connection                                                      | 30                                                   |
| WATTPILOT_DEBUG_LEVEL            | Debug level                                                                                   | INFO                                                 |
| WATTPILOT_INITIALIZED_TIMEOUT    | Wait timeout for property initialization                                                      | 30                                                   |
| WATTPILOT_HOST                   | IP address of the Wattpilot device to connect to                                              |                                                      |
| WATTPILOT_PASSWORD               | Password for connecting to the Wattpilot device                                               |                                                      |

## MQTT Support

The easiest way to start the shell with MQTT support is using these environment variables:

```bash
export MQTT_ENABLED=true
export MQTT_HOST=<mqtt_host>
export WATTPILOT_HOST=<wattpilot_ip>
export WATTPILOT_PASSWORD=<wattpilot_password>
python3 shell.py
```

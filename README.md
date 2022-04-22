# Wattpilot

> :warning: This project is still in early development and might never leave this state

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
export WATTPILOT_HOST=<wattpilot_ip>
export WATTPILOT_PASSWORD=<password>
wattpilotshell
> help
Wattpilot Shell Commands:
  exit: Exit the shell
  get <propName>: Get a property value
  ha <start|status|stop>: Control Home Assistant discovery (+MQTT client)
  help: This help message
  info: Print device infos
  list [propRegex]: List property infos
  mqtt <start|status|stop>: Control MQTT support
  set <propName> <value>: Set a property value
  unwatch-message <msgType>: Unwatch message of given message type
  unwatch-property <propName>: Unwatch value changes of given property name
  values [propRegex] [valueRegex]: List values of properties (with value mapping enabled)
  values-raw: List raw values of properties (without value mapping)
  watch-message <msgType>: Watch message of given message type
  watch-property <propName>: Watch value changes of given property name
```

It's also possible to pass a single command to the shell to integrate it into scripts:

```bash
# Usage:
wattpilotshell <wattpilot_ip> <password> "<command> <args...>"

# Examples:
wattpilotshell <wattpilot_ip> <password> "get amp"
wattpilotshell <wattpilot_ip> <password> "set amp 6"
```

## MQTT Support

It is possible to publish JSON messages received from Wattpilot and/or individual property value changes to an MQTT server.
The easiest way to start the shell with MQTT support is using these environment variables:

```bash
export MQTT_ENABLED=true
export MQTT_HOST=<mqtt_host>
export WATTPILOT_HOST=<wattpilot_ip>
export WATTPILOT_PASSWORD=<wattpilot_password>
wattpilotshell
```

Pay attention to environment variables starting with `MQTT_` to fine-tune the MQTT support (e.g. which messages or properties should published to MQTT topics).

MQTT support can be easily tested using mosquitto:

```bash
# Start mosquitto in a separate console:
mosquitto

# Subscribe to topics in a separate console:
mosquitto_sub -t 'wattpilot/#' -v
```

## Home Assistant Support

To enable Home Assistant integration (using MQTT) set `MQTT_ENABLED` and `HA_ENABLED` to `true` and make sure to correctly configure the [MQTT Integration](https://www.home-assistant.io/integrations/mqtt).
It provides auto-discovery of entities using property configuration from `wattpilot.yaml`.
The is the simplest possible way to start the shell with HA support:

```bash
export MQTT_ENABLED=true
export HA_ENABLED=true
export MQTT_HOST=<mqtt_host>
export WATTPILOT_HOST=<wattpilot_ip>
export WATTPILOT_PASSWORD=<wattpilot_password>
wattpilotshell
```

Pay attention to environment variables starting with `HA_` to fine-tune the Home Assistant integration (e.g. which properties should be exposed).

The discovery config published to MQTT can be tested using this in addition to the testing steps from MQTT above:

```bash
MQTT support can be easily tested using mosquitto:

```bash
# Subscribe to homeassisant topics in a separate console:
mosquitto_sub -t 'homeassistant/#' -v
```

## Environment Variables

| Environment Variable             | Description                                                                                   | Default Value                                        |
| -------------------------------- | --------------------------------------------------------------------------------------------- | ---------------------------------------------------- |
| `HA_ENABLED`             | Enable Home Assistant Discovery                                                               | `false`                                                |
| `HA_PROPERTIES` | Only discover given properties (leave unset for all properties having `homeAssistant` set in `wattpilot.yaml`) |  |
| `HA_TOPIC_CONFIG` | Topic pattern for HA discovery config | `homeassistant/{component}/{uniqueId}/config` |
| `HA_WAIT_INIT_S` | Wait initial number of seconds after starting discovery (in addition to wait time depending on the number of properties). May be increased, if entities in HA are not populated with values. | `5` |
| `HA_WAIT_PROPS_MS` | Wait milliseconds per property after discovery before publishing property values. May be increased, if entities in HA are not populated with values. | `50` |
| `MQTT_CLIENT_ID`                   | MQTT client ID                                                                                | `wattpilot2mqtt`                                       |
| `MQTT_DECOMPOSE_PROPERTIES` | Whether compound properties (e.g. JSON arrays or objects) should be decomposed into separate properties | `true` |
| `MQTT_ENABLED`                     | Enable MQTT                                                                                   | `false`                                                |
| `MQTT_HOST`                        | MQTT host to connect to                                                                       |                                                      |
| `MQTT_PORT`                        | Port of the MQTT host to connect to                                                           | `1883`                                                 |
| `MQTT_PROPERTIES`            | List of space-separated property names to publish changes for (leave unset for all properties) |                                   |
| `MQTT_PUBLISH_MESSAGES`            | Publish received Wattpilot messages to MQTT                                                   | `false`                                                 |
| `MQTT_PUBLISH_PROPERTIES`          | Publish received property values to MQTT                                                      | `true`                                                |
| `MQTT_TOPIC_BASE`                  | Base topic for MQTT                                                                           | `wattpilot`                                            |
| `MQTT_TOPIC_MESSAGES`       | Topic pattern to publish Wattpilot messages to                                                | `{baseTopic}/messages/{messageType}`    |
| `MQTT_TOPIC_PROPERTY_BASE` | Base topic for properties | `{baseTopic}/properties/{propName}` |
| `MQTT_TOPIC_PROPERTY_SET`  | Topic pattern to listen for property value changes for                                        | `~/set` |
| `MQTT_TOPIC_PROPERTY_STATE` | Topic pattern to publish property values to                                                   | `~/state`     |
| `WATTPILOT_CONNECT_TIMEOUT`        | Connect timeout for Wattpilot connection                                                      | `30`                                                   |
| `WATTPILOT_DEBUG_LEVEL`            | Debug level                                                                                   | `INFO`                                                 |
| `WATTPILOT_HOST`                   | IP address of the Wattpilot device to connect to                                              |                                                      |
| `WATTPILOT_INIT_TIMEOUT`    | Wait timeout for property initialization                                                      | `30`                                                   |
| `WATTPILOT_PASSWORD`               | Password for connecting to the Wattpilot device                                               |                                                      |

## HELP improving wattpilot.yaml

The MQTT and Home Assistant support heavily depends on the property description in `[src/wattpilot/ressources/wattpilot.yaml](wattpilot.yaml)` which has been compiled from different sources and das not yet contain a full set of information for all relevant properties.
See [API.md](API.md) for a generated documentation of the data.

If you want to help, please have a look at the properties defined in `wattpilot.yaml` and fill in the missing pieces (e.g. `title`, `description`, `rw`, `jsonType`, `childProps`, `homeAssistant`, `device_class`, `unit_of_measurement`, `enabled_by_default`) to properties you care about.
The file contains enough documentation and a lot of working examples to get you started.

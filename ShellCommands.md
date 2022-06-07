# Wattpilot Shell Commands

## connect

```bash
Connect to Wattpilot (using WATTPILOT_* env variables)
Usage: connect
```

## exit

```bash
Exit the shell
Usage: exit
```

## get

```bash
Get a property value
Usage: get <propName>
```

## updateInverter

```bash
(un)pairs a connected inverter
Usage: updateInverter (pair|unpair)  <inverterID>

<inverterID> is normally in the form 123.456789
```

## ha

```bash
Control Home Assistant discovery (+MQTT client)
Usage: ha <enable|disable|discover|properties|start|status|stop|undiscover> [args...]

Home Assistant commands:
  enable <propName>
    Enable a discovered entity representing the property <propName>
    NOTE: Re-enabling of disabled entities may still be broken in HA and require a restart of HA.
  disable <propName>
    Disable a discovered entity representing the property <propName>
  discover <propName>
    Let HA discover an entity representing the property <propName>
  properties
    List properties activated for HA discovery
  start
    Start HA MQTT discovery (using HA_* env variables)
  status
    Status of HA MQTT discovery
  stop
    Stop HA MQTT discovery
  undiscover <propName>
    Let HA remove a discovered entity representing the property <propName>
    NOTE: Removing of disabled entities may still be broken in HA and require a restart of HA.

```

## help

```bash
List available commands with "help" or detailed help with "help cmd".
```

## info

```bash
Print device infos
Usage: info
```

## mqtt

```bash
Control the MQTT bridge
Usage: mqtt <publish|start|status|stop|unpublish> [args...]

MQTT commands:
  properties
    List properties activated for MQTT publishing
  publish <messages|properties>
    Enable publishing of messages or properties
  publish <message> <msgType>
    Enable publishing of a certain message type
  publish <property> <propName>
    Enable publishing of a certain property
  start
    Start the MQTT bridge (using MQTT_* env variables)
  status
    Status of the MQTT bridge
  stop
    Stop the MQTT bridge
  unpublish <messages|properties>
    Disable publishing of messages or properties
  unpublish <message> <msgType>
    Disable publishing of a certain message type
  unpublish <property> <propName>
    Disable publishing of a certain property

```

## properties

```bash
List property definitions and values
Usage: properties [propRegex]
```

## rawvalues

```bash
List raw values of properties (without value mapping)
Usage: rawvalues [propRegex] [valueRegex]
```

## server

```bash
Start in server mode (infinite wait loop)
Usage: server
```

## set

```bash
Set a property value
Usage: set <propName> <value>
```

## unwatch

```bash
Unwatch a message or property
Usage: unwatch <message|property> <msgType|propName>
```

## values

```bash
List values of properties (with value mapping enabled)
Usage: values [propRegex] [valueRegex]
```

## watch

```bash
Watch message or a property
Usage: watch <message|property> <msgType|propName>
```

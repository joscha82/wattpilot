# Wattpilot Shell Environment Variables

|Environment Variable|Type|Default Value|Description|
|--------------------|----|-------------|-----------|
|`HA_DISABLED_ENTITIES`|`boolean`|`false`|Create disabled entities in Home Assistant|
|`HA_ENABLED`|`boolean`|`false`|Enable Home Assistant Discovery|
|`HA_PROPERTIES`|`list`||List of space-separated properties that should be discovered by Home Assistant (leave unset for all properties having `homeAssistant` set in [wattpilot.yaml](src/wattpilot/ressources/wattpilot.yaml)|
|`HA_TOPIC_CONFIG`|`string`|`homeassistant/{component}/{uniqueId}/config`|Topic pattern for HA discovery config|
|`HA_WAIT_INIT_S`|`integer`|`0`|Wait initial number of seconds after starting discovery (in addition to wait time depending on the number of properties). May be increased, if entities in HA are not populated with values.|
|`HA_WAIT_PROPS_MS`|`integer`|`0`|Wait milliseconds per property after discovery before publishing property values. May be increased, if entities in HA are not populated with values.|
|`MQTT_AVAILABLE_PAYLOAD`|`string`|`online`|Payload for the availability topic in case the MQTT bridge is online|
|`MQTT_CLIENT_ID`|`string`|`wattpilot2mqtt`|MQTT client ID|
|`MQTT_ENABLED`|`boolean`|`false`|Enable MQTT|
|`MQTT_HOST`|`string`||MQTT host to connect to|
|`MQTT_MESSAGES`|`list`||List of space-separated message types to be published to MQTT (leave unset for all messages)|
|`MQTT_NOT_AVAILABLE_PAYLOAD`|`string`|`offline`|Payload for the availability topic in case the MQTT bridge is offline (last will message)|
|`MQTT_PASSWORD`|`password`||Password for connecting to MQTT|
|`MQTT_PORT`|`integer`|`1883`|Port of the MQTT host to connect to|
|`MQTT_PROPERTIES`|`list`||List of space-separated property names to publish changes for (leave unset for all properties)|
|`MQTT_PUBLISH_MESSAGES`|`boolean`|`false`|Publish received Wattpilot messages to MQTT|
|`MQTT_PUBLISH_PROPERTIES`|`boolean`|`true`|Publish received property values to MQTT|
|`MQTT_TOPIC_AVAILABLE`|`string`|`{baseTopic}/available`|Topic pattern to publish Wattpilot availability status to|
|`MQTT_TOPIC_BASE`|`string`|`wattpilot`|Base topic for MQTT|
|`MQTT_TOPIC_MESSAGES`|`string`|`{baseTopic}/messages/{messageType}`|Topic pattern to publish Wattpilot messages to|
|`MQTT_TOPIC_PROPERTY_BASE`|`string`|`{baseTopic}/properties/{propName}`|Base topic for properties|
|`MQTT_TOPIC_PROPERTY_SET`|`string`|`~/set`|Topic pattern to listen for property value changes for|
|`MQTT_TOPIC_PROPERTY_STATE`|`string`|`~/state`|Topic pattern to publish property values to|
|`MQTT_USERNAME`|`string`||Username for connecting to MQTT|
|`WATTPILOT_AUTOCONNECT`|`boolean`|`true`|Automatically connect to Wattpilot on startup|
|`WATTPILOT_AUTO_RECONNECT`|`boolean`|`true`|Automatically re-connect to Wattpilot on lost connections|
|`WATTPILOT_CONNECT_TIMEOUT`|`integer`|`30`|Connect timeout for Wattpilot connection|
|`WATTPILOT_HOST`|`string`||IP address of the Wattpilot device to connect to|
|`WATTPILOT_INIT_TIMEOUT`|`integer`|`30`|Wait timeout for property initialization|
|`WATTPILOT_LOGLEVEL`|`string`|`INFO`|Log level (CRITICAL,ERROR,WARNING,INFO,DEBUG)|
|`WATTPILOT_PASSWORD`|`password`||Password for connecting to the Wattpilot device|
|`WATTPILOT_RECONNECT_INTERVAL`|`integer`|`30`|Waiting time in seconds before a lost connection is re-connected|
|`WATTPILOT_SPLIT_PROPERTIES`|`boolean`|`true`|Whether compound properties (e.g. JSON arrays or objects) should be decomposed into separate properties|

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
  list: List all known property keys
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

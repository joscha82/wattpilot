# Wattpilot Shell Commands

## alias

```bash
Usage: alias [-h] SUBCOMMAND ...

Manage aliases

An alias is a command that enables replacement of a word by another string.

optional arguments:
  -h, --help  show this help message and exit

subcommands:
  SUBCOMMAND
    create    create or overwrite an alias
    delete    delete aliases
    list      list aliases

See also:
  macro

```

## connect

```bash
Connect to Wattpilot
Usage: connect
```

## disconnect

```bash
Disconnect from Wattpilot
Usage: disconnect
```

## edit

```bash
Usage: edit [-h] [file_path]

Run a text editor and optionally open a file with it

The editor used is determined by a settable parameter. To set it:

  set editor (program-name)

positional arguments:
  file_path   optional path to a file to open in editor

optional arguments:
  -h, --help  show this help message and exit

```

## exit

```bash
Exit the shell
Usage: exit
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
Usage: help [-h] [-v] [command] ...

List available commands or provide detailed help for a specific command

positional arguments:
  command        command to retrieve help for
  subcommands    subcommand(s) to retrieve help for

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  print a list of all commands with descriptions of each

```

## history

```bash
Usage: history [-h] [-r | -e | -o FILE | -t TRANSCRIPT_FILE | -c] [-s] [-x]
               [-v] [-a]
               [arg]

View, run, edit, save, or clear previously entered commands

positional arguments:
  arg                   empty               all history items
                        a                   one history item by number
                        a..b, a:b, a:, ..b  items by indices (inclusive)
                        string              items containing string
                        /regex/             items matching regular expression

optional arguments:
  -h, --help            show this help message and exit
  -r, --run             run selected history items
  -e, --edit            edit and then run selected history items
  -o, --output_file FILE
                        output commands to a script file, implies -s
  -t, --transcript TRANSCRIPT_FILE
                        output commands and results to a transcript file,
                        implies -s
  -c, --clear           clear all history

formatting:
  -s, --script          output commands in script format, i.e. without command
                        numbers
  -x, --expanded        output fully parsed commands with any aliases and
                        macros expanded, instead of typed commands
  -v, --verbose         display history and include expanded commands if they
                        differ from the typed command
  -a, --all             display all commands, including ones persisted from
                        previous sessions

```

## info

```bash
Print device infos
Usage: info
```

## macro

```bash
Usage: macro [-h] SUBCOMMAND ...

Manage macros

A macro is similar to an alias, but it can contain argument placeholders.

optional arguments:
  -h, --help  show this help message and exit

subcommands:
  SUBCOMMAND
    create    create or overwrite a macro
    delete    delete macros
    list      list macros

See also:
  alias

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

## propget

```bash
Get a property value
Usage: propget <propName>
```

## propset

```bash
Set a property value
Usage: propset <propName> <value>
```

## quit

```bash
Usage: quit [-h]

Exit this application

optional arguments:
  -h, --help  show this help message and exit

```

## rawvalues

```bash
List raw values of properties (without value mapping)
Usage: rawvalues [propRegex] [valueRegex]
```

## run_pyscript

```bash
Usage: run_pyscript [-h] script_path ...

Run a Python script file inside the console

positional arguments:
  script_path       path to the script file
  script_arguments  arguments to pass to script

optional arguments:
  -h, --help        show this help message and exit

```

## run_script

```bash
Usage: run_script [-h] [-t TRANSCRIPT_FILE] script_path

Run commands in script file that is encoded as either ASCII or UTF-8 text

Script should contain one command per line, just like the command would be
typed in the console.

If the -t/--transcript flag is used, this command instead records
the output of the script commands to a transcript for testing purposes.

positional arguments:
  script_path           path to the script file

optional arguments:
  -h, --help            show this help message and exit
  -t, --transcript TRANSCRIPT_FILE
                        record the output of the script as a transcript file

```

## server

```bash
Start in server mode (infinite wait loop)
Usage: server
```

## set

```bash
Usage: set [-h] [param] [value]

Set a settable parameter or show current settings of parameters

positional arguments:
  param       parameter to set or view
  value       new value for settable

optional arguments:
  -h, --help  show this help message and exit

```

## shell

```bash
Usage: shell [-h] command ...

Execute a command as if at the OS prompt

positional arguments:
  command       the command to run
  command_args  arguments to pass to command

optional arguments:
  -h, --help    show this help message and exit

```

## shortcuts

```bash
Usage: shortcuts [-h]

List available shortcuts

optional arguments:
  -h, --help  show this help message and exit

```

## unwatch

```bash
Unwatch a message or property
Usage: unwatch <event|message|property> <eventType|msgType|propName>
```

## values

```bash
List values of properties (with value mapping enabled)
Usage: values [propRegex] [valueRegex]
```

## watch

```bash
Watch an event, a message or a property
Usage: watch <event|message|property> <eventType|msgType|propName>
```

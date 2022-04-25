#!/bin/bash

# This script helps during development to test certain aspects of the wattpilot shell.

if [ -f dev.env ]; then
    source dev.env
fi

export PYTHONPATH=src

WPCONFIG_FILE="src/wattpilot/ressources/wattpilot.yaml"

cmd="${1:-default}"
shift 1

function runShell() {
    python -m wattpilot.wattpilotshell "${@}"
}

function runShellWithProps() {
    PROPS="${1:-}"
    echo "Enabled properties: ${PROPS}"
    MQTT_ENABLED=true HA_ENABLED=true MQTT_PROPERTIES="${PROPS}" HA_PROPERTIES="${PROPS}" runShell
}

function runShellWithAllProps() {
    PROP_FILTER="${1:-.*}"
    PROPS=$(yq -r -c '.properties[] | (.key, .childProps?[]?.key?)' "${WPCONFIG_FILE}" | grep "^${PROP_FILTER}" | xargs echo)
    runShellWithProps "${PROPS}"
}


case "${cmd}" in
    default)
        runShell
    ;;
    shell-only)
        WATTPILOT_AUTOCONNECT=false MQTT_ENABLED=false HA_ENABLED=false runShell "${@}"
    ;;
    server)
        WATTPILOT_AUTOCONNECT=true MQTT_ENABLED=true HA_ENABLED=true runShell "server"
    ;;
    save)
        logfile=work/status-$(date +"%Y-%m-%d_%H-%M-%S")-${1:-adhoc}.log
        mkdir -p work
        WATTPILOT_DEBUG_LEVEL=WARNING MQTT_ENABLED=false HA_ENABLED=false runShell "values" >>${logfile} 2>&1
        WATTPILOT_DEBUG_LEVEL=WARNING MQTT_ENABLED=false HA_ENABLED=false runShell "rawvalues" >>${logfile} 2>&1
        WATTPILOT_DEBUG_LEVEL=WARNING MQTT_ENABLED=false HA_ENABLED=false runShell "properties" >>${logfile} 2>&1
    ;;
    ha-default)
        runShellWithProps ""
    ;;
    ha-all)
        runShellWithAllProps ""
    ;;
    ha-test-props)
        runShellWithProps "alw loe nrg fhz spl3 acu ama cdi ffna fna"
    ;;
    ha-test-array)
        runShellWithProps "nrg"
    ;;
    ha-test-boolean)
        runShellWithProps "alw loe"
    ;;
    ha-test-float)
        runShellWithProps "fhz spl3"
    ;;
    ha-test-integer)
        runShellWithProps "acu ama"
    ;;
    ha-test-object)
        runShellWithProps "cdi"
    ;;
    ha-test-string)
        runShellWithProps "ffna fna"
    ;;
    *)
        echo "Unknown command: ${cmd}"
        exit 1
    ;;
esac

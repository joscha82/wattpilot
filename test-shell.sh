#!/bin/bash

# This script helps during development to test certain aspects of the wattpilot shell.

source .env


WPCONFIG_FILE="src/wattpilot/ressources/wattpilot.yaml"

cmd="${1:-ha-default}"
shift 1

function runShellWithProps() {
    PROPS="${1:-}"
    echo "Enabled properties: ${PROPS}"
    MQTT_ENABLED=true HA_ENABLED=true MQTT_PROPERTIES="${PROPS}" HA_PROPERTIES="${PROPS}" wattpilotshell
}

function runShellWithAllProps() {
    PROP_FILTER="${1:-.*}"
    PROPS=$(yq -r -c '.properties[] | (.key, .childProps?[]?.key?)' "${WPCONFIG_FILE}" | grep "^${PROP_FILTER}" | xargs echo)
    runShellWithProps "${PROPS}"
}


case "${cmd}" in
    shell)
        MQTT_ENABLED=false HA_ENABLED=false wattpilotshell
    ;;
    save)
        logfile=work/status-$(date +"%Y-%m-%d_%H-%M-%S")-${1:-adhoc}.log
        mkdir -p work
        WATTPILOT_DEBUG_LEVEL=WARNING MQTT_ENABLED=false HA_ENABLED=false wattpilotshell "list" >${logfile} 2>&1
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
esac
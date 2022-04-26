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

function runShellOnly() {
    WATTPILOT_AUTOCONNECT=false MQTT_ENABLED=false HA_ENABLED=false runShell "${@}"
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
        runShell "${@}"
    ;;
    shell-only)
        runShellOnly "${@}"
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
    update-docs)
        python gen-apidocs.py >API.md
        (
            echo "# Wattpilot Shell Commands"
            for cmd in $(
                runShellOnly "help" \
                | awk 'BEGIN {p=0} {if(p) print $0} /^==/ {p=1}' \
                | xargs -n 1 echo \
                | grep -E -v '^EOF$' \
                | sort \
            ); do
                echo ""
                echo "## ${cmd}"
                echo ""
                echo "\`\`\`bash"
                runShellOnly "help ${cmd}"
                echo "\`\`\`"
            done
        ) >ShellCommands.md
        (
            # NOTE: The file cannot yet fully replace the table in README.md since the description is missing
            echo "# Wattpilot Shell Environment Variables"
            echo ""
            echo "| Environment Variable | Default Value |"
            echo "|----------------------|---------------|"
            cat src/wattpilot/wattpilotshell.py \
            | awk 'BEGIN {p=0} /^ +/ {if(p) print $0} /^def / {p=0} /^def main_setup_env\(\):/ {p=1}' \
            | grep -E -v '\b(global|assert)\b' \
            | sed -re 's/#.*//g;s/\n//g' \
            | tr '\n' ' ' \
            | sed -re "s/os\\.environ\\.get\\(\\s*'([A-Z_]+)'\\s*,\\s*'([^']*)'\\s*\\)/\n| \`\1\` | \`\2\` |\n/g; s/\`\`//g" \
            | grep -E '^\|' \
            | sort
        ) >ShellEnvVariables.md
    ;;
    *)
        echo "Unknown command: ${cmd}"
        exit 1
    ;;
esac

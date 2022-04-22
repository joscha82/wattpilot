#!/bin/bash

cmd="${1}"
shift 1

case "${cmd}" in
    shell)
        wattpilotshell "${@}"
    ;;
    server)
        wattpilotshell server
    ;;
esac

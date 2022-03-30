#!/usr/bin/env bash
#

set -e
set -o pipefail

HELP="
Runs the webserver for the \"Hash Map as a service\" challenge.

By default, it runs using uWSGI server.
For other run mode, please read the following command line options:

Usage:
    docker run ... [MODE] [OPTIONS]

Modes:
    -- | uwsgi    Runs the application using uWSGI server.
                  This is the default run mode.

    flask         Runs the application using Flask.
                  This is only for development purpose
                   and always runs in DEBUG mode.

    *             Any other value will be treated as a normal
                   command to execute inside the Docker container.

Options:
    --debug             Runs the application in DEBUG mode.

    -h | -? | --help    Prints this help message."

#
# Functions:
#
function init()
{
    mkdir -p "${DATA_VOLUME}/collections" \
             "${DATA_VOLUME}/logs" \
             "${DATA_VOLUME}/tmp"

    chown -R www-data:www-data "${DATA_VOLUME}"
}

function run-flask()
{
    export DEBUG="true"

    su-exec www-data python run.py ${@}
}
function run-uwsgi()
{
    local ARGS=()

    while [[ ${#} -gt 0 ]]
    do
        case "${1}" in
            --debug)
                export DEBUG="true"
                ;;
            *)
                ARGS+=("${1}")
                ;;
        esac

        shift
    done

    set -- "${ARGS[@]}"

    uwsgi --ini uwsgi.ini ${@}
}

#
# Execution:
#
init

case "${1}" in
    -h | -? | --help)
        echo "${HELP}"

        exit 0
        ;;


    -- | uwsgi)
        shift

        run-uwsgi ${@}

        ;;
    -*)
        run-uwsgi ${@}

        ;;

    flask)
        shift

        run-flask ${@}

        ;;
    *)
        exec ${@}

        ;;
esac

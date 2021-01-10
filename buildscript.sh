#!/usr/bin/env bash

function runcmd() {
    echo "$@"
    "$@"
    if [ $((exitstatus=$?)) -ne 0 ]; then
        echo "Command '$@' failed! Exit status $exitstatus"
        exit $exitstatus
    fi
}

function phase1() {
    runcmd apt-get update
    runcmd apt-get upgrade -y

    runcmd apt-get install -y x11-apps locales
    runcmd locale-gen "en_US.UTF-8"
    runcmd export uid=$ARG_UID gid=$ARG_GID
    runcmd mkdir -p /home/user
    runcmd chown "${uid}:${gid}" -R /home/user
    runcmd bash -c "echo \"user:x:${uid}:${gid}:User,,,:/home/user:/bin/bash\" >> /etc/passwd"
    runcmd bash -c "echo \"user:x:${gid}:\" >> /etc/group"
}

function phase2() {
    runcmd apt-get install -y lsb-release apt-transport-https ca-certificates
    runcmd apt-get update
    runcmd apt-get install -y tmux vim less curl
    export DEBIAN_FRONTEND=noninteractive
    runcmd bash -c 'export DEBIAN_FRONTEND=noninteractive; apt-get install -y tzdata'
    runcmd apt-get install -y unzip anki
    runcmd apt-get install -y python3-nltk python3-jsonpickle
    runcmd apt-get install -y python3-distutils
}


if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    # script is not sourced
    "$@"
fi

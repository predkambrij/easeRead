#!/usr/bin/env bash
echo -n "" > .env
echo "ARG_UID=$(id -u)" >> .env
echo "ARG_GID=$(id -g)" >> .env

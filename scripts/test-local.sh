#! /usr/bin/env bash

# Exit in case of error
set -e

COMPOSE="docker compose -f compose.backend.yml"

$COMPOSE down -v --remove-orphans # Remove possibly previous broken stacks left hanging after an error

if [ $(uname -s) = "Linux" ]; then
    echo "Remove __pycache__ files"
    sudo find . -type d -name __pycache__ -exec rm -r {} \+
fi

$COMPOSE build
$COMPOSE up -d
$COMPOSE exec -T backend bash scripts/tests-start.sh "$@"

#! /usr/bin/env sh

# Exit in case of error
set -e
set -x

COMPOSE="docker compose -f compose.backend.yml"

$COMPOSE build
$COMPOSE down -v --remove-orphans # Remove possibly previous broken stacks left hanging after an error
$COMPOSE up -d
$COMPOSE exec -T backend bash scripts/tests-start.sh "$@"
$COMPOSE down -v --remove-orphans

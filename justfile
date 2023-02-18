set dotenv-load := false

compose := "docker-compose run --rm --no-deps web"
manage := compose + " python manage.py"

alias shell := console

# ----------------------------------------------------------------
# Just nice-to-haves
# ----------------------------------------------------------------

@_default:
    just --list

@fmt:
    just --fmt --unstable

# ----------------------------------------------------------------
# Scripts to rule them all
#
# Research:
# - https://www.encode.io/reports/april-2020#our-workflow-approach
# - https://github.blog/2015-06-30-scripts-to-rule-them-all/
# ----------------------------------------------------------------

bootstrap:
    #!/usr/bin/env bash
    set -euo pipefail

    if [ ! -f ".env" ]; then
        echo ".env created"
        cp .env-dist .env
    fi

    docker compose build --force-rm

# TODO: might remove this if we don't use it...
@cibuild:
    python -m pytest
    python -m black --check .
    interrogate -c pyproject.toml .

# Bash shell in the web container
@console:
    docker compose run --rm web bash

@server *ARGS:
    just up {{ ARGS }}
    # docker compose run --rm web python manage.py migrate --noinput
    # docker compose up

@setup:
    just bootstrap
    docker compose build --force-rm
    # docker compose run --rm web python manage.py migrate --noinput

@test +ARGS="":
    just test_pytest {{ ARGS }}

@update:
    docker compose rm --force web
    docker compose pull
    docker compose build --force-rm
    docker compose run --rm web python manage.py migrate --noinput

# ----------------------------------------------------------------
# Common Docker Compose shortcuts
# ----------------------------------------------------------------

@build:
    docker compose build

@down:
    docker compose down

@logs *ARGS:
    docker compose logs {{ ARGS }}

@rebuild:
    docker compose rm --force web
    docker compose build --force-rm

@restart *ARGS:
    docker compose restart {{ ARGS }}

@start +ARGS="--detach":
    just server {{ ARGS }}

@stop:
    docker compose down

@tail:
    just logs --follow --tail 100

@up *ARGS:
    docker compose up {{ ARGS }}

# ----------------------------------------------------------------
# Everything else
# ----------------------------------------------------------------

# Compile new python dependencies
@pip-compile *ARGS:
    docker compose run \
        --entrypoint= \
        --rm web \
            bash -c "pip-compile {{ ARGS }} ./requirements.in \
                --generate-hashes \
                --resolver=backtracking \
                --output-file ./requirements.txt"

# Upgrade existing Python dependencies to their latest versions
@pip-compile-upgrade:
    just pip-compile --upgrade

# Python linting
@pre-commit:
    git ls-files -- . | xargs pre-commit run --config=./.pre-commit-config.yaml --files

@run +ARGS="--help":
    {{ manage }} {{ ARGS }}

@test_interrogate:
    docker compose run --rm web interrogate -vv --fail-under 100 --whitelist-regex "test_.*" .

@test_pytest +ARGS="":
    docker compose run --rm web pytest -s {{ ARGS }}

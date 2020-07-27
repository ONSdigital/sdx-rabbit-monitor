# sdx-rabbit-monitor

[![Build Status](https://travis-ci.org/ONSdigital/sdx-rabbit-monitor.svg?branch=develop)](https://travis-ci.org/ONSdigital/sdx-rabbit-monitor) [![Codacy Badge](https://api.codacy.com/project/badge/Grade/46cbdc2821814a028448e0b2255a85f2)](https://www.codacy.com/app/ons-sdc/sdx-rabbit-monitor?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=ONSdigital/sdx-rabbit-monitor&amp;utm_campaign=Badge_Grade) [![codecov](https://codecov.io/gh/ONSdigital/sdx-rabbit-monitor/branch/develop/graph/badge.svg)](https://codecov.io/gh/ONSdigital/sdx-rabbit-monitor)

`sdx-rabbit-monitor` is a component of the Office for National Statistics (ONS) Survey Data Exchange (SDX) product which polls the RabbitMQ management API for monitoring purposes.

Data returned is logged to sys.stderr.

## Installation
This application presently installs required packages from requirements files:
- `requirements.txt`: packages for the application, with hashes for all packages: see https://pypi.org/project/hashin/
- `test-requirements.txt`: packages for testing and linting

It's also best to use `pyenv` and `pyenv-virtualenv`, to build in a virtual environment with the currently recommended version of Python.  To install these, see:
- https://github.com/pyenv/pyenv
- https://github.com/pyenv/pyenv-virtualenv
- (Note that the homebrew version of `pyenv` is easiest to install, but can lag behind the latest release of Python.)

### Getting started
Once your virtual environment is set, install the requirements:
```shell
$ make build
```

To test, first run `make build` as above, then run:
```shell
$ make test
```

It's also possible to install within a container using docker. From the sdx-rabbit-monitor directory:
```shell
$ docker build -t sdx-rabbit-monitor .
```

## Usage

Start sdx-rabbit-monitor service using the following command:

```shell
$ make start
```
## API
Available endpoints are listed below:

| Endpoint          | Request Method       | Description
|-------------------|----------------------|--------------------------
| `/healthcheck`    | `GET`                | Returns `200` status and a JSON payload of ```{"status": "ok"}``` if the service is running.

The endpoint accepts a `GET` request, and is located at:

  - `/healthcheck`

## Python Version
The current implementation uses Python 3.8 . (It uses the asyncio coroutine syntax not async and await)

## Configuration

The main configuration options are listed below:

| Environment Variable            | Example       | Description
|---------------------------------|---------------|--------------------------
| RABBITMQ_DEFAULT_USER           | `rabbit`      | RabbitMQ username
| RABBITMQ_DEFAULT_PASS           | `rabbit`      | RabbitMQ password
| RABBITMQ_HOST                   | `0.0.0.0`     | Host for the RabbitMQ service
| RABBIT_MGT_PORT                 | `15672`       | Port for the RabbitMQ Management Console API
| RABBIT_MONITOR_WAIT_TIME        | `10`          | Number of seconds between 1 round of API calls |
| RABBIT_MONITOR_STATS_WINDOW     | `300`         | Length of statistics window in seconds
| RABBIT_MONITOR_STATS_INCREMENT  | `RABBIT_MONITOR_STATS_WINDOW / 10` | Statistics sample frequency in seconds |
| RABBITMQ_DEFAULT_VHOST          | `%2f`         | Vhost for RabbitMQ service

### License

Copyright (c) 2017 Crown Copyright (Office for National Statistics)

Released under MIT license, see [LICENSE](LICENSE) for details.

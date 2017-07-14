# sdx-rabbit-monitor

[![Build Status](https://travis-ci.org/ONSdigital/sdx-rabbit-monitor.svg?branch=develop)](https://travis-ci.org/ONSdigital/sdx-rabbit-monitor) [![Codacy Badge](https://api.codacy.com/project/badge/Grade/46cbdc2821814a028448e0b2255a85f2)](https://www.codacy.com/app/ons-sdc/sdx-rabbit-monitor?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=ONSdigital/sdx-rabbit-monitor&amp;utm_campaign=Badge_Grade) [![codecov](https://codecov.io/gh/ONSdigital/sdx-rabbit-monitor/branch/develop/graph/badge.svg)](https://codecov.io/gh/ONSdigital/sdx-rabbit-monitor)

`sdx-rabbit-monitor` is a component of the Office for National Statistics (ONS) Survey Data Exchange (SDX) product which polls the RabbitMQ management API for monitoring purposes.

Data returned is logged to sys.stderr.

## Installation

To install, use:

```
make build
```

To install using local sdx-common repo (requires SDX_HOME environment variable), use:

```
make dev
```

To run the test suite, use:

```
make test
```

## API
Available endpoints are listed below:

| Endpoint          | Request Method       | Description
|-------------------|----------------------|--------------------------
| `/healthcheck`    | `GET`                | Returns `200` status and a JSON payload of ```{"status": "ok"}``` if the service is running.

The endpoint accepts a `GET` request, and is located at:

  - `/healthcheck`



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

# sdx-rabbit-monitor

[![Build Status](https://travis-ci.org/ONSdigital/sdx-rabbit-monitor.svg?branch=develop)](https://travis-ci.org/ONSdigital/sdx-rabbit-monitor)

`sdx-rabbit-monitor` is a component of the Office for National Statistics (ONS) Survey Data Exchange (SDX) product which polls the RabbitMQ management API for monitoring purposes.

Data returned is logged to sys.stderr.

## Installation

To install, use:

```
make build
```

To run the test suite, use:

```
make test
```

## Configuration

The main configuration options are listed below:

| Environment Variable            | Default       | Description 
|---------------------------------|---------------|--------------------------
| RABBITMQ_DEFAULT_USER           | `rabbit`      | RabbitMQ username
| RABBITMQ_DEFAULT_PASS           | `rabbit`      | RabbitMQ password
| RABBITMQ_HOST                   | `0.0.0.0`     | Host for the RabbitMQ service
| RABBIT_MGT_HOST                 | `15672`       | Port for the RabbitMQ Management Console API
| RABBIT_MONITOR_WAIT_TIME        | 10            | Number of seconds between 1 round of API calls |

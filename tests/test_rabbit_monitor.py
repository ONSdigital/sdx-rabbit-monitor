#!/usr/bin/env python
#   coding: UTF-8
import unittest

import responses

import rabbit_monitor
from rabbit_monitor import RabbitMonitor
import settings


class TestRabbitHealthcheck(unittest.TestCase):

    rm = RabbitMonitor()

    def test_process_healthcheck(self):
        url = settings.URLS['healthcheck']

        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET,
                     url,
                     body='{"status": "ok"}',
                     status=200,
                     content_type='application/json')

            with self.assertLogs('rabbit_monitor', level='INFO') as cm:
                self.rm.call_healthcheck()

            self.assertIn("INFO:rabbit_monitor:status=200 event='Rabbit health ok'",
                          cm.output)

        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET,
                     url,
                     body='{"status": "bad"}',
                     status=500,
                     content_type='application/json')

            with self.assertLogs('rabbit_monitor', level='ERROR') as cm:
                self.rm.call_healthcheck()

            self.assertIn("ERROR:rabbit_monitor:status=500 event='Rabbit health bad'",
                          cm.output)

    def test_process_aliveness(self):
        url = settings.URLS['aliveness']

        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET,
                     url,
                     body='{"status": "ok"}',
                     status=200,
                     content_type='application/json')

            with self.assertLogs('rabbit_monitor', level='INFO') as cm:
                self.rm.call_aliveness()

            self.assertIn("INFO:rabbit_monitor:status=200 event='Rabbit aliveness ok'",
                          cm.output)

        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET,
                     url,
                     body='{"status": "bad"}',
                     status=500,
                     content_type='application/json')

            with self.assertLogs('rabbit_monitor', level='ERROR') as cm:
                self.rm.call_aliveness()

            self.assertIn("ERROR:rabbit_monitor:status=500 event='Rabbit aliveness bad'",
                          cm.output)

    def test_shutdown(self):
        with self.assertRaises(SystemExit) as cm:
            self.rm.shutdown()
            self.assertEqual(cm.exception.code, 0)

    def test_healthcheck_endpoint_method(self):
        self.assertEqual('{"status": "ok"}', rabbit_monitor.healthcheck())


if __name__ == '__main__':
    unittest.main()

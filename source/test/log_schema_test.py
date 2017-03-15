import datetime
import unittest
from emis_log import create_app
from emis_log.api.schema import *


class LogSchemaTestCase(unittest.TestCase):


    def setUp(self):
        self.app = create_app("test")

        self.app_context = self.app.app_context()
        self.app_context.push()

        self.client = self.app.test_client()
        self.schema = LogSchema()


    def tearDown(self):
        self.schema = None

        self.app_context.pop()


    def test_empty1(self):
        client_data = {
        }
        data, errors = self.schema.load(client_data)

        self.assertTrue(errors)
        self.assertEqual(errors, {
            "_schema": ["Input data must have a log key"]
        })


    def test_empty2(self):
        client_data = {
                "log": {}
            }
        data, errors = self.schema.load(client_data)

        self.assertTrue(errors)
        self.assertEqual(errors, {
                "timestamp": ["Missing data for required field."],
                "priority": ["Missing data for required field."],
                "severity": ["Missing data for required field."],
                "message": ["Missing data for required field."],
            })


    def test_use_case1(self):
        timestamp = datetime.datetime.utcnow()
        client_data = {
                "log": {
                    "timestamp": timestamp.isoformat(),
                    "priority": "high",
                    "severity": "critical",
                    "message": "fixme",
                }
            }
        data, errors = self.schema.load(client_data)

        self.assertFalse(errors)

        self.assertTrue(hasattr(data, "id"))
        self.assertTrue(isinstance(data.id, type(None)))

        self.assertTrue(hasattr(data, "timestamp"))
        self.assertEqual(data.timestamp, timestamp)

        self.assertTrue(hasattr(data, "severity"))
        self.assertEqual(data.severity, "critical")

        self.assertTrue(hasattr(data, "priority"))
        self.assertEqual(data.priority, "high")

        self.assertTrue(hasattr(data, "message"))
        self.assertEqual(data.message, "fixme")

        data.id = 5

        data, errors = self.schema.dump(data)

        self.assertFalse(errors)
        self.assertTrue("log" in data)

        log_record = data["log"]

        self.assertTrue("id" in log_record)
        self.assertEqual(log_record["id"], 5)

        self.assertTrue("severity" in log_record)
        self.assertEqual(log_record["severity"], "critical")

        self.assertTrue("priority" in log_record)
        self.assertEqual(log_record["priority"], "high")

        self.assertTrue("message" in log_record)
        self.assertEqual(log_record["message"], "fixme")

        self.assertTrue("posted_at" not in log_record)

        self.assertTrue("_links" in log_record)

        links = log_record["_links"]

        self.assertTrue("self" in links)
        self.assertTrue("collection" in links)


    def test_use_case2(self):
        timestamp = datetime.datetime.utcnow()
        client_data = {
                "log": {
                    "timestamp": timestamp.isoformat(),
                    "priority": "invalid",
                    "severity": "critical",
                    "message": "fixme",
                }
            }
        data, errors = self.schema.load(client_data)

        self.assertTrue(errors)
        self.assertEqual(errors, {
            "priority": ["Value (invalid) must be one of (low, high)"]
        })


    def test_use_case3(self):
        timestamp = datetime.datetime.utcnow()
        client_data = {
                "log": {
                    "timestamp": timestamp.isoformat(),
                    "priority": "high",
                    "severity": "invalid",
                    "message": "fixme",
                }
            }
        data, errors = self.schema.load(client_data)

        self.assertTrue(errors)
        self.assertEqual(errors, {
            "severity": ["Value (invalid) must be one of "
                "(non_critical, critical)"]
        })


    def test_use_case4(self):
        timestamp = datetime.datetime.utcnow()
        client_data = {
                "log": {
                    "timestamp": timestamp.isoformat(),
                    "priority": "high",
                    "severity": "critical",
                    "message": "",
                }
            }
        data, errors = self.schema.load(client_data)

        self.assertTrue(errors)
        self.assertEqual(errors, {
            "message": ["Data not provided"]
        })


if __name__ == "__main__":
    unittest.main()

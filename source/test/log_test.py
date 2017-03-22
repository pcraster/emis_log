import os.path
import unittest
from flask import current_app, json
from emis_log import create_app, db
from emis_log.api.schema import *


class LogTestCase(unittest.TestCase):


    def setUp(self):
        self.app = create_app("test")
        self.app.config["TESTING"] = True
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()

        self.timestamp1 = datetime.datetime.utcnow()
        self.timestamp2 = datetime.datetime.utcnow()
        self.timestamp3 = datetime.datetime.utcnow()


    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


    def post_log_records(self):
        payloads = [
                {
                    "timestamp": self.timestamp1.isoformat(),
                    "priority": "high",
                    "severity": "critical",
                    "message": "fixme1",
                },
                {
                    "timestamp": self.timestamp2.isoformat(),
                    "priority": "low",
                    "severity": "critical",
                    "message": "fixme2",
                },
                {
                    "timestamp": self.timestamp3.isoformat(),
                    "priority": "high",
                    "severity": "non_critical",
                    "message": "fixme3",
                },
            ]

        for payload in payloads:
            response = self.client.post("/logs",
                data=json.dumps({"log": payload}),
                content_type="application/json")
            data = response.data.decode("utf8")

            self.assertEqual(response.status_code, 201, "{}: {}".format(
                response.status_code, data))


    def test_get_all_log_records1(self):
        # No records posted.
        response = self.client.get("/logs")
        data = response.data.decode("utf8")

        self.assertEqual(response.status_code, 200, "{}: {}".format(
            response.status_code, data))

        data = json.loads(data)

        self.assertTrue("logs" in data)
        self.assertEqual(data["logs"], [])


    def test_get_all_log_records2(self):
        # Some records posted.
        self.post_log_records()

        response = self.client.get("/logs")
        data = response.data.decode("utf8")

        self.assertEqual(response.status_code, 200, "{}: {}".format(
            response.status_code, data))

        data = json.loads(data)

        self.assertTrue("logs" in data)

        records = data["logs"]

        self.assertEqual(len(records), 3)


    def test_get_log(self):
        self.post_log_records()

        response = self.client.get("/logs")
        data = response.data.decode("utf8")
        data = json.loads(data)
        records = data["logs"]
        record = records[0]
        uri = record["_links"]["self"]
        response = self.client.get(uri)

        data = response.data.decode("utf8")

        self.assertEqual(response.status_code, 200, "{}: {}".format(
            response.status_code, data))

        data = json.loads(data)

        self.assertTrue("log" in data)

        record = data["log"]

        self.assertEqual(data["log"], record)

        self.assertTrue("id" in record)

        self.assertTrue("severity" in record)
        self.assertEqual(record["severity"], "critical")

        self.assertTrue("priority" in record)
        self.assertEqual(record["priority"], "high")

        self.assertTrue("message" in record)
        self.assertEqual(record["message"], "fixme1")

        self.assertTrue("timestamp" in record)

        self.assertTrue("posted_at" not in record)

        self.assertTrue("_links" in record)

        links = record["_links"]

        self.assertTrue("self" in links)
        self.assertEqual(links["self"], uri)

        self.assertTrue("collection" in links)


    def test_get_unexisting_log(self):
        self.post_log_records()

        response = self.client.get("/logs")
        data = response.data.decode("utf8")
        data = json.loads(data)
        records = data["logs"]
        record = records[0]
        uri = record["_links"]["self"]
        # Invalidate uri
        uri = os.path.join(os.path.split(uri)[0], "4")
        response = self.client.get(uri)

        data = response.data.decode("utf8")

        self.assertEqual(response.status_code, 400, "{}: {}".format(
            response.status_code, data))

        data = json.loads(data)

        self.assertTrue("message" in data)


    def test_post_log(self):
        timestamp = datetime.datetime.utcnow()
        payload = {
            "timestamp": timestamp.isoformat(),
            "priority": "low",
            "severity": "non_critical",
            "message": "fixme",
        }
        response = self.client.post("/logs",
            data=json.dumps({"log": payload}),
            content_type="application/json")
        data = response.data.decode("utf8")

        self.assertEqual(response.status_code, 201, "{}: {}".format(
            response.status_code, data))

        data = json.loads(data)

        self.assertTrue("log" in data)

        record = data["log"]

        self.assertTrue("id" in record)

        self.assertTrue("severity" in record)
        self.assertEqual(record["severity"], "non_critical")

        self.assertTrue("priority" in record)
        self.assertEqual(record["priority"], "low")

        self.assertTrue("message" in record)
        self.assertEqual(record["message"], "fixme")

        self.assertTrue("timestamp" in record)

        self.assertTrue("posted_at" not in record)

        self.assertTrue("_links" in record)

        links = record["_links"]

        self.assertTrue("self" in links)
        self.assertTrue("collection" in links)


    def test_post_bad_request(self):
        response = self.client.post("/logs")
        data = response.data.decode("utf8")

        self.assertEqual(response.status_code, 400, "{}: {}".format(
            response.status_code, data))

        data = json.loads(data)

        self.assertTrue("message" in data)


    def test_post_unprocessable_entity(self):
        payload = ""
        response = self.client.post("/logs",
            data=json.dumps({"log": payload}),
            content_type="application/json")
        data = response.data.decode("utf8")

        self.assertEqual(response.status_code, 422, "{}: {}".format(
            response.status_code, data))

        data = json.loads(data)

        self.assertTrue("message" in data)


if __name__ == "__main__":
    unittest.main()

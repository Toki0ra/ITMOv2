import json
import threading
import unittest
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from app.server import create_server


class HttpTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = create_server(port=0)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.base = f"http://127.0.0.1:{cls.server.server_port}"

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=5)

    def request(self, method, path, payload=None, raw=None):
        data = raw
        if payload is not None:
            data = json.dumps(payload).encode("utf-8")
        request = Request(self.base + path, data=data, method=method)
        if payload is not None:
            request.add_header("Content-Type", "application/json")
        try:
            with urlopen(request, timeout=5) as response:
                return response.status, response.read().decode("utf-8")
        except HTTPError as exc:
            return exc.code, exc.read().decode("utf-8")

    def post_json(self, payload):
        status, body = self.request("POST", "/api/analyze", payload=payload)
        return status, json.loads(body)

    def test_index_page(self):
        status, body = self.request("GET", "/")
        self.assertEqual(status, 200)
        for element in ('id="text"', 'id="limit"', 'id="analyze"', 'id="results"'):
            self.assertIn(element, body)

    def test_end_to_end_contract(self):
        status, data = self.post_json({"text": "b a b c a b", "limit": 3})
        self.assertEqual(status, 200)
        self.assertEqual(
            data,
            {
                "items": [
                    {"word": "b", "count": 3},
                    {"word": "a", "count": 2},
                    {"word": "c", "count": 1},
                ],
                "total_words": 6,
                "unique_words": 3,
            },
        )

    def test_default_limit(self):
        status, data = self.post_json({"text": "a b c d"})
        self.assertEqual(status, 200)
        self.assertEqual(len(data["items"]), 3)

    def test_empty_text_gives_empty_items(self):
        status, data = self.post_json({"text": "   "})
        self.assertEqual(status, 200)
        self.assertEqual(data["items"], [])
        self.assertEqual(data["total_words"], 0)

    def test_invalid_text(self):
        status, data = self.post_json({"text": 123})
        self.assertEqual(status, 400)
        self.assertEqual(data["error"]["code"], "invalid_text")

    def test_invalid_limit(self):
        status, data = self.post_json({"text": "a", "limit": 0})
        self.assertEqual(status, 400)
        self.assertEqual(data["error"]["code"], "invalid_limit")
        self.assertIn("message", data["error"])

    def test_text_too_long(self):
        status, data = self.post_json({"text": "a" * 10001})
        self.assertEqual(status, 413)
        self.assertEqual(data["error"]["code"], "text_too_long")

    def test_invalid_json_body(self):
        status, body = self.request("POST", "/api/analyze", raw=b"{not json")
        self.assertEqual(status, 400)
        self.assertEqual(json.loads(body)["error"]["code"], "invalid_body")

    def test_non_object_body(self):
        status, body = self.request("POST", "/api/analyze", raw=b"[1, 2]")
        self.assertEqual(status, 400)
        self.assertEqual(json.loads(body)["error"]["code"], "invalid_body")

    def test_method_not_allowed(self):
        status, body = self.request("GET", "/api/analyze")
        self.assertEqual(status, 405)
        self.assertEqual(json.loads(body)["error"]["code"], "method_not_allowed")

    def test_not_found(self):
        status, body = self.request("GET", "/missing")
        self.assertEqual(status, 404)
        self.assertEqual(json.loads(body)["error"]["code"], "not_found")


if __name__ == "__main__":
    unittest.main()

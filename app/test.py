import unittest
import json

from main import app
from main import reset_shortened_urls

class TestURLShorten(unittest.TestCase):
    client = None
    def setUp(self):
        reset_shortened_urls()
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_bad_request_no_short_code(self):
        rv = self.client.get("/")
        self.assertTrue(rv.status_code == 400)
    
    def test_redirect_if_code_exists(self):
        rv = self._post_json({
            "url": "https://www.google.com",
            "short_code": "google"
        })
        self.assertTrue(rv.status_code == 200)

        rv = self.client.get("/?short_code=google")
        self.assertTrue(rv.status_code == 302)

    def test_create_short_code_fails_if_exists(self):
        short_code_req = {
            "url": "https://www.google.com",
            "short_code": "google"
        }
        rv = self._post_json(short_code_req)
        self.assertTrue(rv.status_code == 200)

        rv = self._post_json(short_code_req)
        self.assertTrue(rv.status_code == 400)

    def _post_json(self, data):
        return self.client.post(
            "/", data=json.dumps(data),
            content_type="application/json",
        )

if __name__ == '__main__':
    unittest.main()
import unittest
from unittest.mock import Mock, patch

import baidutongji.api as api


class ApiResponseParsingTests(unittest.TestCase):
	def setUp(self):
		api.proxies = None

	def tearDown(self):
		api.proxies = None

	@patch("baidutongji.api.GET")
	def test_get_baidu_json_returns_valid_json_payload(self, mock_get):
		response = Mock()
		response.json.return_value = {"result": "ok"}
		mock_get.return_value = response

		payload = api._get_baidu_json(url="https://example.com", params={"a": 1})

		self.assertEqual(payload, {"result": "ok"})
		mock_get.assert_called_once_with(url="https://example.com", params={"a": 1})

	@patch("baidutongji.api.GET")
	def test_get_baidu_json_preserves_baidu_error_payload(self, mock_get):
		response = Mock()
		response.json.return_value = {"error_code": 111, "error_msg": "token expired"}
		mock_get.return_value = response

		payload = api._get_baidu_json(url="https://example.com")

		self.assertEqual(payload, {"error_code": 111, "error_msg": "token expired"})

	@patch("baidutongji.api.GET")
	def test_get_baidu_json_normalizes_invalid_json_response(self, mock_get):
		response = Mock()
		response.json.side_effect = ValueError("not json")
		response.text = "<html>bad gateway</html>"
		mock_get.return_value = response

		payload = api._get_baidu_json(url="https://example.com")

		self.assertEqual(
			payload,
			{
				"error_code": "invalid_json_response",
				"error_message": "Baidu returned a non-JSON response",
				"response_text": "<html>bad gateway</html>",
			},
		)

	@patch("baidutongji.api.requests.get")
	def test_get_uses_proxies_when_configured(self, mock_requests_get):
		api.proxies = {"http": "http://proxy.local:8080"}

		api.GET(url="https://example.com", params={"site_id": "1"})

		mock_requests_get.assert_called_once_with(
			url="https://example.com",
			params={"site_id": "1"},
			proxies={"http": "http://proxy.local:8080"},
		)


if __name__ == "__main__":
	unittest.main()

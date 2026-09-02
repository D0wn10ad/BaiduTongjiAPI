import unittest
from unittest.mock import patch

import baidutongji.api as api


class ProxyBehaviorTests(unittest.TestCase):
	def setUp(self):
		api.proxies = None

	def tearDown(self):
		api.proxies = None

	def test_set_proxy_none_clears_existing_proxy(self):
		api.proxies = {"http": "http://proxy.local:8080"}

		result = api.setProxy(None)

		self.assertTrue(result)
		self.assertIsNone(api.proxies)

	@patch("baidutongji.api.requests.get")
	def test_get_prefers_per_call_proxies_over_global_proxy(self, mock_requests_get):
		api.proxies = {"http": "http://global-proxy.local:8080"}
		per_call_proxies = {"https": "http://per-call-proxy.local:8080"}

		api.GET(url="https://example.com", proxies=per_call_proxies)

		mock_requests_get.assert_called_once_with(
			url="https://example.com",
			proxies=per_call_proxies,
		)


if __name__ == "__main__":
	unittest.main()

import unittest
from unittest.mock import MagicMock, patch
import requests

from breach_check import check_pwned_password, split_sha1_digest
from checker import evaluate_password
from generator import generate_password


class TestPasswordToolkitEdgeCases(unittest.TestCase):
    def test_empty_and_whitespace(self):
        for sample in ("", "   "):
            res = evaluate_password(sample)
            self.assertEqual(res["rating"], "Weak")
            self.assertEqual(res["score"], 0)

    def test_common_passwords(self):
        for sample in ("password", "  QWERTY  "):
            res = evaluate_password(sample)
            self.assertEqual(res["rating"], "Weak")

    def test_generator_length_and_toggles(self):
        with self.assertRaises(ValueError):
            generate_password(length=3)

        no_sym = generate_password(length=24, use_symbols=False)
        self.assertEqual(len(no_sym), 24)
        self.assertTrue(all(ch.isalnum() for ch in no_sym))

    @patch("breach_check.requests.get", side_effect=requests.Timeout("timed out"))
    def test_offline_or_timeout_handled_gracefully(self, _mock_get):
        with self.assertRaises(RuntimeError):
            check_pwned_password("synthetic-offline-sample")

    @patch("breach_check.requests.get")
    def test_breached_vs_clean_suffix_matching(self, mock_get):
        sample = "synthetic-breach-sample"
        prefix, suffix = split_sha1_digest(sample)
        mock_resp = MagicMock()
        mock_resp.text = f"00000000000000000000000000000000000:2\n{suffix}:42\n"
        mock_resp.raise_for_status.return_value = None
        mock_get.return_value = mock_resp

        self.assertEqual(check_pwned_password(sample), 42)
        called_url = mock_get.call_args[0][0]
        self.assertTrue(called_url.endswith(prefix))
        self.assertNotIn(suffix, called_url)


if __name__ == "__main__":
    unittest.main()
import unittest
from unittest.mock import patch
from typer.testing import CliRunner
from src.gmaps_avoid_swiss.cli import app


class TestCLI(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()

    @patch('src.gmaps_avoid_swiss.gmaps_avoid_swiss.GMapsRoutingClient.compute_route')
    def test_cli_compute_route(self, mock_compute_route):
        mock_compute_route.return_value = unittest.mock.Mock(routes=[unittest.mock.Mock()])

        result = self.runner.invoke(app, ["api_key", "New York, NY, USA", "New Jersey, NJ, USA"])

        self.assertEqual(result.exit_code, 0)
        mock_compute_route.assert_called_once_with(
            {'address': 'New York, NY, USA'},
            {'address': 'New Jersey, NJ, USA'},
        )

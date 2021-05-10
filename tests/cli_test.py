from unittest import TestCase, mock
from better_drone.cli import main


class TestCli(TestCase):
    @mock.patch('better_drone.cli.submit')
    def test_main(self, submit):
        submit.return_value = mock.MagicMock()
        main("assignment")

        submit.assert_called()

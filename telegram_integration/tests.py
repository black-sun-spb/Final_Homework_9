from django.test import TestCase
from telegram_integration.tasks import send_telegram_message_for_user
from unittest.mock import patch


class TelegramTasksTestCase(TestCase):
    @patch("telegram_integration.tasks.requests.Session.post")
    def test_send_telegram_message_for_user(self, mock_post):
        mock_post.return_value.status_code = 200
        send_telegram_message_for_user("12345", "Hello")
        mock_post.assert_called_once()

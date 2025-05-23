from django.test import TestCase
from unittest.mock import patch

class Tests(TestCase):
    @patch('task.models.Task.objects.all')
    def test_get_tasks_with_mock(self, mock):
        mock.return_value = []
        response = mock()
        self.assertIsInstance(response, list)
        self.assertEqual(response, [])

    def test_get_tesk_by_request(self):
        request = self.client.get(
            path='/api/task/all/',
            headers={},
            data={}
        )
        status = request.status_code
        response = request.json()
        self.assertEqual(status, 200)
        self.assertIsInstance(response, list)
        self.assertEqual(len(response), 0)
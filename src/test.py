'''To test the features by using pytest'''
import unittest
from unittest.mock import patch, MagicMock
from services import Tumblr, store_data

class TestTumblrAPI(unittest.TestCase):
    """Test case for the Tumblr API functionality."""

    def setUp(self):
        """Sets up the necessary environment for the tests."""
        self.tumblr = Tumblr()
        self.auth = ('your_consumer_key', 'your_consumer_secret')
        self.settings = MagicMock()
        self.settings.BLOG_IDENTIFIER = "your_blog_identifier"
    @patch('builtins.input', side_effect=['Test Title','Test Body'])
    @patch('requests.post')
    def test_create_post_success(self, mock_post):
        """Tests the successful creation of a post."""
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "meta": {"status": 201, "msg": "Created"},
            "response": {"id": 12345, "state": "published"}
        }
        mock_post.return_value = mock_response
        result= self.tumblr.create_post()
        self.assertIsNotNone(result)
        self.assertIn("id", result['response'])
        self.assertEqual(result['meta']['status'], 201)
    @patch('builtins.input', side_effect=['12345'])
    @patch('requests.post')
    def test_delete_post_success(self, mock_post):
        """Tests the successful deletion of a post."""
        mock_response = MagicMock()
        mock_response.status_code = 204  # Assuming Tumblr returns 204 for successful deletion
        mock_response.json.return_value = {"meta": {"status": 204, "msg": "Deleted"}}
        mock_post.return_value = mock_response
        result = self.tumblr.delete_post()
        self.assertIsNotNone(result)
        self.assertEqual(result['meta']['status'], 204)

    @patch('builtins.input', side_effect=['tag1'])
    @patch('requests.get')
    def test_search_posts_success(self, mock_get):
        """Tests the successful search of a post."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "meta": {"status": 200, "msg": "OK"},
            "response": [{"type": "text", "body": "Sample post"}]
        }
        mock_get.return_value = mock_response
        result = self.tumblr.search_posts()
        self.assertIsNotNone(result)
        self.assertIn("response", result)
        self.assertGreater(len(result['response']), 0)

    @patch('requests.get')
    def test_get_posts_success(self, mock_get):
        """Tests the successful get of a post."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "meta": {"status": 200, "msg": "OK"},
            "response": [{"id": 12345, "type": "text"}]
        }
        mock_get.return_value = mock_response
        result = self.tumblr.get_post()
        self.assertIsNotNone(result)
        self.assertIn("response", result)
        self.assertGreater(len(result['response']), 0)

    @patch('services.connection.execute')  # Adjust with the actual path of your connection
    def test_store_data_success(self, mock_execute):
        """Tests the successful store of a post."""
        response_data = {
            "meta": {"status": 201, "msg": "Created"},
            "response": {"id": 12345, "state": "published"}
        }
        post_data = {"title": "Test", "body": "Test body"}
        store_data(response_data, post_data)
        mock_execute.assert_called_once()

if __name__ == '__main__':
    unittest.main()

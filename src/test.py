"""Tests for the Tumblr service functionality using pytest."""

from unittest.mock import patch, MagicMock
import pytest
from services import Tumblr, store_data

@pytest.fixture(name="tumblr_instance")
def tumblr_instance_fixture():
    """Fixture for setting up Tumblr instance."""
    tumblr = Tumblr()
    return tumblr

def test_create_post_success(tumblr_instance):
    """Tests the successful creation of a post."""
    with patch('builtins.input', side_effect=['Test Title', 'Test Body']), \
         patch('requests.post') as mock_post:
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "meta": {"status": 201, "msg": "Created"},
            "response": {"id": 12345, "state": "published"}
        }
        mock_post.return_value = mock_response

        result, post_data = tumblr_instance.create_post()

        assert result is not None
        assert "id" in result['response']
        assert result['meta']['status'] == 201

def test_delete_post_success(tumblr_instance):
    """Tests the successful deletion of a post."""
    with patch('builtins.input', side_effect=['12345']), \
         patch('requests.post') as mock_post:
        mock_response = MagicMock()
        mock_response.status_code = 204
        mock_response.json.return_value = {"meta": {"status": 204, "msg": "Deleted"}}
        mock_post.return_value = mock_response

        result = tumblr_instance.delete_post()

        assert result is not None
        assert result['meta']['status'] == 204

def test_search_posts_success(tumblr_instance):
    """Tests the successful search of a post."""
    with patch('builtins.input', side_effect=['tag1']), \
         patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "meta": {"status": 200, "msg": "OK"},
            "response": [{"type": "text", "body": "Sample post"}]
        }
        mock_get.return_value = mock_response

        result = tumblr_instance.search_posts()

        assert result is not None
        assert "response" in result
        assert len(result['response']) > 0

def test_get_posts_success(tumblr_instance):
    """Tests the successful retrieval of posts."""
    with patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "meta": {"status": 200, "msg": "OK"},
            "response": [{"id": 12345, "type": "text"}]
        }
        mock_get.return_value = mock_response

        result = tumblr_instance.get_post()

        assert result is not None
        assert "response" in result
        assert len(result['response']) > 0

def test_store_data_success():
    """Tests the successful storage of post data."""
    with patch('services.connection.execute') as mock_execute:
        response_data = {
            "meta": {"status": 201, "msg": "Created"},
            "response": {"id": 12345, "state": "published"}
        }
        post_data = {"title": "Test", "body": "Test body"}
        store_data(response_data, post_data)
        mock_execute.assert_called_once()

# tests/test_validators.py
import unittest
from unittest.mock import MagicMock
from src.validators import validate_video_request, validate_video_id, ValidationError
from bson import ObjectId

class TestValidators(unittest.TestCase):

    def setUp(self):
        # Create a mock request object
        self.mock_request = MagicMock()

    def test_validate_video_request_valid(self):
        # Test with valid JSON and title
        self.mock_request.is_json = True
        self.mock_request.get_json.return_value = {'title': 'Sample Video'}
        try:
            validate_video_request(self.mock_request)
        except ValidationError:
            self.fail("validate_video_request raised ValidationError unexpectedly!")

    def test_validate_video_request_no_json(self):
        # Test with request not in JSON format
        self.mock_request.is_json = False
        with self.assertRaises(ValidationError) as context:
            validate_video_request(self.mock_request)
        self.assertEqual(context.exception.status_code, 777)
        self.assertEqual(context.exception.message, "Request must be in JSON format.")

    def test_validate_video_request_invalid_json(self):
        # Test with invalid JSON format (not a dict)
        self.mock_request.is_json = True
        self.mock_request.get_json.return_value = []
        with self.assertRaises(ValidationError) as context:
            validate_video_request(self.mock_request)
        self.assertEqual(context.exception.status_code, 400)
        self.assertEqual(context.exception.message, "Invalid JSON data format.")

    def test_validate_video_request_missing_title(self):
        # Test with JSON missing title
        self.mock_request.is_json = True
        self.mock_request.get_json.return_value = {'description': 'Sample Description'}
        with self.assertRaises(ValidationError) as context:
            validate_video_request(self.mock_request)
        self.assertEqual(context.exception.status_code, 400)
        self.assertEqual(context.exception.message, "Missing 'title' in request data.")

    def test_validate_video_id_valid(self):
        # Test with a valid ObjectId
        valid_id = str(ObjectId())
        try:
            validate_video_id(valid_id)
        except ValidationError:
            self.fail("validate_video_id raised ValidationError unexpectedly!")

    def test_validate_video_id_invalid(self):
        # Test with an invalid ObjectId
        invalid_id = "123"
        with self.assertRaises(ValidationError) as context:
            validate_video_id(invalid_id)
        self.assertEqual(context.exception.status_code, 400)
        self.assertEqual(context.exception.message, "Invalid video ID format.")

if __name__ == '__main__':
    unittest.main()

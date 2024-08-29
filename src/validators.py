# src/validators.py
from bson import ObjectId

class ValidationError(Exception):
    """Custom exception for validation errors with status code and message."""
    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message
        super().__init__(self.message)

def validate_video_request(request):
    """Validate the request data for video creation or update."""
    if not request.is_json:
        raise ValidationError(400, "Request must be in JSON format.")
    
    data = request.get_json()
    if not isinstance(data, dict):
        raise ValidationError(400, "Invalid JSON data format.")
    
    if 'title' not in data:
        raise ValidationError(400, "Missing 'title' in request data.")

def validate_video_id(video_id):
    """Validate video_id format."""
    if not ObjectId.is_valid(video_id):
        raise ValidationError(400, "Invalid video ID format.")

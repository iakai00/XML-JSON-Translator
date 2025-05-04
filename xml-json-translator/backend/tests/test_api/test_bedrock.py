
import pytest
from unittest.mock import patch, MagicMock
from app.services.bedrock_service import BedrockTranslationService

@pytest.fixture
def mock_boto3_session():
    with patch('boto3.Session') as mock_session:
        # Mock the client and its methods
        mock_client = MagicMock()
        mock_session.return_value.client.return_value = mock_client
        
        # Mock response for invoke_model
        mock_response = {
            'body': MagicMock()
        }
        mock_response['body'].read.return_value = '{"content": [{"text": "[TRANSLATED TEXT]"}]}'
        mock_client.invoke_model.return_value = mock_response
        
        yield mock_session

def test_bedrock_translation_service(mock_boto3_session):
    """Test the BedrockTranslationService"""
    service = BedrockTranslationService()
    
    # Test translation
    result = service.translate("Hello world", "fr")
    
    # Check that the client was called correctly
    mock_boto3_session.assert_called_once()
    mock_client = mock_boto3_session.return_value.client.return_value
    mock_client.invoke_model.assert_called_once()
    
    # Check that the result is as expected
    assert result == "[TRANSLATED TEXT]"

def test_bedrock_error_handling(mock_boto3_session):
    """Test error handling in BedrockTranslationService"""
    # Set up the mock to raise an exception
    mock_client = mock_boto3_session.return_value.client.return_value
    mock_client.invoke_model.side_effect = Exception("Test error")
    
    service = BedrockTranslationService()
    
    # Test that we get the original text back on error
    original_text = "Hello world"
    result = service.translate(original_text, "fr")
    
    assert result == original_text
"""
Unit tests for OpenAI ChatCompletion API calls using pytest.
Tests both streaming and non-streaming responses.
"""
import os
import pytest
from unittest.mock import Mock, patch
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


@pytest.fixture
def api_key():
    """Fixture for API key from environment"""
    key = os.getenv('API_KEY_TEST')
    if not key:
        pytest.skip("API_KEY_TEST not set in environment")
    return key


@pytest.fixture
def base_url():
    """Fixture for base URL"""
    return 'http://localhost:8000/v1'


@pytest.fixture
def client(api_key, base_url):
    """Fixture for OpenAI client"""
    return OpenAI(
        api_key=api_key,
        base_url=base_url,
    )


@pytest.fixture
def messages():
    """Fixture for test messages"""
    return [
        {"role": "developer", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"}
    ]


class TestChatCompletionNonStreaming:
    """Test cases for non-streaming chat completions"""

    def test_chat_completion_basic(self, client, messages):
        """Test basic chat completion without streaming"""
        completion = client.chat.completions.create(
            model="anthropic/claude-sonnet-4.5",
            messages=messages,
            stream=False
        )

        # Assertions
        assert completion is not None
        assert hasattr(completion, 'choices')
        assert len(completion.choices) > 0
        assert hasattr(completion.choices[0], 'message')
        assert completion.choices[0].message.content is not None
        assert len(completion.choices[0].message.content) > 0

        print(f"\n✅ Response: {completion.choices[0].message.content}")

    def test_chat_completion_with_usage(self, client, messages):
        """Test chat completion includes usage information"""
        completion = client.chat.completions.create(
            model="anthropic/claude-sonnet-4.5",
            messages=messages,
            stream=False
        )

        # Check usage if available
        if hasattr(completion, 'usage'):
            usage = completion.usage
            assert usage is not None
            print(f"\n📊 Usage - Total tokens: {usage.total_tokens if hasattr(usage, 'total_tokens') else 'N/A'}")

    def test_chat_completion_response_structure(self, client, messages):
        """Test response structure matches OpenAI format"""
        completion = client.chat.completions.create(
            model="anthropic/claude-sonnet-4.5",
            messages=messages,
            stream=False
        )

        # Check required fields
        assert hasattr(completion, 'id')
        assert hasattr(completion, 'model')
        assert hasattr(completion, 'choices')
        assert hasattr(completion, 'created')
        assert hasattr(completion, 'object')

        # Check choices structure
        choice = completion.choices[0]
        assert hasattr(choice, 'message')
        assert hasattr(choice, 'finish_reason')

        # Check message structure
        message = choice.message
        assert hasattr(message, 'role')
        assert hasattr(message, 'content')


class TestChatCompletionStreaming:
    """Test cases for streaming chat completions"""

    def test_streaming_basic(self, client, messages):
        """Test basic streaming chat completion"""
        stream = client.chat.completions.create(
            model="anthropic/claude-sonnet-4.5",
            messages=messages,
            stream=True
        )

        # Assert stream is iterable
        assert stream is not None

        # Collect chunks
        chunks = []
        full_content = ""

        for chunk in stream:
            assert chunk is not None
            chunks.append(chunk)

            # Check chunk structure
            if chunk.choices and len(chunk.choices) > 0:
                delta = chunk.choices[0].delta
                if delta and delta.content is not None:
                    content = delta.content
                    full_content += content
                    print(content, end="", flush=True)

        print(f"\n\n✅ Received {len(chunks)} chunks")
        print(f"✅ Full message length: {len(full_content)} characters")

        # Assertions
        assert len(chunks) > 0
        assert len(full_content) > 0

    def test_streaming_chunk_structure(self, client, messages):
        """Test streaming chunk structure matches OpenAI format"""
        stream = client.chat.completions.create(
            model="anthropic/claude-sonnet-4.5",
            messages=messages,
            stream=True
        )

        chunks = []
        for chunk in stream:
            chunks.append(chunk)

            # Check chunk has required fields
            assert hasattr(chunk, 'id') or chunk.id is not None
            assert hasattr(chunk, 'object')
            assert hasattr(chunk, 'choices')

            # Check first chunk structure
            if len(chunks) == 1:
                first_chunk = chunk
                assert first_chunk.object == "chat.completion.chunk"
                assert first_chunk.choices is not None
                assert len(first_chunk.choices) > 0

        assert len(chunks) > 0
        print(f"\n✅ All {len(chunks)} chunks have correct structure")

    def test_streaming_content_accumulation(self, client, messages):
        """Test that streaming chunks can be accumulated correctly"""
        stream = client.chat.completions.create(
            model="anthropic/claude-sonnet-4.5",
            messages=messages,
            stream=True
        )

        full_content = ""
        chunk_count = 0

        for chunk in stream:
            if chunk.choices and len(chunk.choices) > 0:
                delta = chunk.choices[0].delta
                if delta and delta.content is not None:
                    full_content += delta.content
                    chunk_count += 1

        # Verify content was accumulated
        assert len(full_content) > 0
        assert chunk_count > 0
        print(f"\n✅ Accumulated {chunk_count} content chunks")
        print(f"✅ Full content: {full_content[:100]}..." if len(full_content) > 100 else f"✅ Full content: {full_content}")


class TestChatCompletionErrorHandling:
    """Test cases for error handling"""

    def test_invalid_api_key(self, base_url):
        """Test error handling with invalid API key"""
        invalid_client = OpenAI(
            api_key="invalid-key-12345",
            base_url=base_url,
        )

        with pytest.raises(Exception):
            invalid_client.chat.completions.create(
                model="anthropic/claude-sonnet-4.5",
                messages=[{"role": "user", "content": "Hello"}],
                stream=False
            )

    def test_invalid_model(self, client, messages):
        """Test error handling with invalid model"""
        with pytest.raises(Exception):
            client.chat.completions.create(
                model="invalid-model-name",
                messages=messages,
                stream=False
            )


class TestChatCompletionMocking:
    """Test cases using mocks (for unit testing without API calls)"""

    def test_mocked_non_streaming(self, messages):
        """Test non-streaming with mocked response"""
        # Create mock client directly
        mock_client = Mock()

        # Mock response
        mock_response = Mock()
        mock_message = Mock()
        mock_message.content = "Hello! How can I help you?"
        mock_message.role = "assistant"

        mock_choice = Mock()
        mock_choice.message = mock_message
        mock_choice.finish_reason = "stop"

        mock_response.choices = [mock_choice]
        mock_response.id = "test-id-123"
        mock_response.model = "anthropic/claude-sonnet-4.5"
        mock_response.created = 1234567890
        mock_response.object = "chat.completion"

        mock_client.chat.completions.create.return_value = mock_response

        # Test with mock client directly (no real API call)
        completion = mock_client.chat.completions.create(
            model="anthropic/claude-sonnet-4.5",
            messages=messages,
            stream=False
        )

        # Assertions
        assert completion.choices[0].message.content == "Hello! How can I help you?"
        assert completion.choices[0].finish_reason == "stop"
        mock_client.chat.completions.create.assert_called_once()

    def test_mocked_streaming(self, messages):
        """Test streaming with mocked response"""
        # Create mock client directly
        mock_client = Mock()

        # Mock stream chunks
        mock_chunks = []
        for i, text in enumerate(["Hello", "!", " How", " can", " I", " help", "?"]):
            mock_chunk = Mock()
            mock_delta = Mock()
            mock_delta.content = text
            mock_choice = Mock()
            mock_choice.delta = mock_delta
            mock_chunk.choices = [mock_choice]
            mock_chunk.id = f"test-id-{i}"
            mock_chunk.object = "chat.completion.chunk"
            mock_chunks.append(mock_chunk)

        # Make chunks iterable
        mock_client.chat.completions.create.return_value = iter(mock_chunks)

        # Test with mock client directly (no real API call)
        stream = mock_client.chat.completions.create(
            model="anthropic/claude-sonnet-4.5",
            messages=messages,
            stream=True
        )

        # Collect content
        full_content = ""
        chunk_count = 0
        for chunk in stream:
            if chunk.choices[0].delta.content:
                full_content += chunk.choices[0].delta.content
                chunk_count += 1

        # Assertions
        assert full_content == "Hello! How can I help?"
        assert chunk_count == 7
        mock_client.chat.completions.create.assert_called_once()


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v", "-s"])

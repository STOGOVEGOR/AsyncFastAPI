import pytest
from sqlalchemy.future import select
from unittest.mock import AsyncMock, patch, MagicMock
from api_async.models import Data1
from api_async.main import fetch_data

@pytest.mark.asyncio
async def test_fetch_data():
    # Mocked result to be returned by the mock session
    class MockResult:
        def scalars(self):
            return self

        def all(self):
            return [Data1(id=1, name="Test 1")]

    # Mock session to replace the real database session
    async def mock_db_execute(query):
        return MockResult()

    # Mocked async session context manager
    class MockSession:
        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc_val, exc_tb):
            pass

        async def execute(self, query):
            return await mock_db_execute(query)

    # Creating the mock session factory
    mock_session_factory = MagicMock(return_value=MockSession())

    # Replacing the async_session context manager with our mock session factory
    with patch('api_async.main.async_session', new=mock_session_factory):
        data = await fetch_data(select(Data1))
        assert len(data) == 1
        assert data[0].id == 1
        assert data[0].name == "Test 1"

"""
Unit tests for summary_service.
"""

from datetime import date
from unittest.mock import Mock
from services.summary_service import get_overview


def test_get_overview():
    """Test overview calculation."""
    # Mock DB session
    mock_db = Mock()
    mock_query = Mock()
    mock_db.query.return_value = mock_query

    # Mock income query
    mock_query.filter.return_value.with_entities.return_value.scalar.return_value = 1000.0
    mock_query.count.return_value = 5

    result = get_overview(mock_db, 1, True)
    assert result["total_income"] == 1000.0
    assert result["transaction_count"] == 5

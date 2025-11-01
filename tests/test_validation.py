import pytest
from datetime import datetime, timedelta
from application.app import validate_date

def test_validate_date_valid():
    """Testar giltigt datum inom tillåtet intervall"""
    today = datetime.now()
    year, month, day = today.year, today.month, today.day
    assert validate_date(year, month, day) == True

def test_validate_date_too_old():
    """Testar datum före 2022-11-01"""
    assert validate_date(2020, 1, 1) == False

def test_validate_date_too_far_ahead():
    """Testar datum mer än en dag framåt"""
    tomorrow_plus_2 = datetime.now() + timedelta(days=2)
    assert validate_date(tomorrow_plus_2.year, tomorrow_plus_2.month, tomorrow_plus_2.day) == False

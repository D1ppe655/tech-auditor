import pytest
from main import load_data

def test_load_default():
    # Если файла нет, должна загрузиться база
    import os
    if os.path.exists("audit_data.json"):
        os.remove("audit_data.json")
    data = load_data()
    assert len(data) == 4
    assert data[0]["question"] == "Проверка питания"

def test_status_logic():
    # Проверка логики статуса
    data = [{"id": 1, "status": "OK"}, {"id": 2, "status": "Не ОК"}]
    is_failed = any(item["status"] == "Не ОК" for item in data)
    assert is_failed is True
import pytest
from gacha_logic import roll_gacha

def test_roll_gacha_returns_valid_rank():
    prizes = [
        {"rank": "S", "rate": 0.05},
        {"rank": "A", "rate": 0.10},
        {"rank": "B", "rate": 0.20},
        {"rank": "C", "rate": 0.65},
    ]
    # 100回まわして、必ずS/A/B/Cのいずれかが返ることを確認
    for _ in range(100):
        result = roll_gacha(prizes)
        assert result in {"S", "A", "B", "C"}
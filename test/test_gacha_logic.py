import pytest
from gacha_logic import roll_gacha

def test_roll_gacha_returns_valid_rank():
    prizes = [
        {"rank": "S", "rate": 0.05},
        {"rank": "A", "rate": 0.10},
        {"rank": "B", "rate": 0.20},
        {"rank": "C", "rate": 0.65},
    ]
    for _ in range(100):
        result = roll_gacha(prizes)
        assert result in {"S", "A", "B", "C"}

def test_roll_gacha_probability_distribution():
    prizes = [
        {"rank": "S", "rate": 0.1},
        {"rank": "A", "rate": 0.2},
        {"rank": "B", "rate": 0.3},
        {"rank": "C", "rate": 0.4},
    ]
    total = 10000
    results = [roll_gacha(prizes) for _ in range(total)]
    from collections import Counter
    counter = Counter(results)
    # 理論値との誤差5%以内ならOK
    assert abs(counter["S"]/total - 0.1) < 0.05
    assert abs(counter["A"]/total - 0.2) < 0.05
    assert abs(counter["B"]/total - 0.3) < 0.05
    assert abs(counter["C"]/total - 0.4) < 0.05

def test_roll_gacha_invalid_total_rate():
    # 合計が1.0でない場合は例外
    prizes = [
        {"rank": "S", "rate": 0.2},
        {"rank": "A", "rate": 0.3},
    ]
    with pytest.raises(ValueError):
        roll_gacha(prizes)

def test_roll_gacha_empty_prizes():
    # 空リストの場合は例外
    with pytest.raises(ValueError):
        roll_gacha([])

def test_roll_gacha_negative_rate():
    # 負の確率が含まれる場合は例外
    prizes = [
        {"rank": "S", "rate": -0.1},
        {"rank": "A", "rate": 1.1},
    ]
    with pytest.raises(ValueError):
        roll_gacha(prizes)

def test_roll_gacha_probability_one():
    # rate=1.0の要素があれば必ずそれが出る
    prizes = [
        {"rank": "A", "rate": 1.0},
    ]
    for _ in range(10):
        result = roll_gacha(prizes)
        assert result == "A"

def test_rate_zero_never_appears():
    prizes = [
        {"rank": "A", "rate": 1.0},
        {"rank": "B", "rate": 0.0},
    ]
    for _ in range(100):
        assert roll_gacha(prizes) == "A"

def test_rate_one_always_appears():
    prizes = [
        {"rank": "A", "rate": 0.0},
        {"rank": "B", "rate": 1.0},
    ]
    for _ in range(100):
        assert roll_gacha(prizes) == "B"

def test_sum_rate_just_below_one():
    prizes = [
        {"rank": "A", "rate": 0.999999},
        {"rank": "B", "rate": 0.0000009},
    ]
    with pytest.raises(ValueError):
        roll_gacha(prizes)

def test_sum_rate_just_above_one():
    prizes = [
        {"rank": "A", "rate": 0.5},
        {"rank": "B", "rate": 0.5},
        {"rank": "C", "rate": 0.0000001},
    ]
    with pytest.raises(ValueError):
        roll_gacha(prizes)

def test_extreme_small_probability():
    prizes = [
        {"rank": "A", "rate": 1e-10},
        {"rank": "B", "rate": 1-1e-10},
    ]
    # 1000回実行してAが一度も出ない（極端に低確率）
    results = [roll_gacha(prizes) for _ in range(1000)]
    assert all(r == "B" for r in results)

def test_duplicate_rank_names():
    prizes = [
        {"rank": "A", "rate": 0.5},
        {"rank": "A", "rate": 0.5},
    ]
    # 仕様によるが同名rankが問題ないか(必要なら例外テスト化)
    result = roll_gacha(prizes)
    assert result == "A"
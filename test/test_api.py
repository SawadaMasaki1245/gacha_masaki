import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from main import app

# テストクライアントのインスタンスを作成
client = TestClient(app)

# pytestのフィクスチャを使い、各テスト実行前にカウンターをリセット
@pytest.fixture(autouse=True)
def reset_gacha_counter(monkeypatch):
    """
    各テストの実行前にgacha_counterを0にリセットし、
    テスト終了後にも0に戻すことで、テスト間の独立性を保つ。
    """
    monkeypatch.setattr("main.gacha_counter", 0)


def test_single_gacha_api_success():
    """単発ガチャAPIが正常にレスポンスを返すか"""
    response = client.get("/gacha/single")
    assert response.status_code == 200
    data = response.json()
    assert "result" in data
    assert "count" in data
    assert isinstance(data["result"], str)
    assert isinstance(data["count"], int)

def test_ten_gacha_api_success():
    """10連ガチャAPIが正常にレスポンスを返すか"""
    response = client.get("/gacha/ten")
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert isinstance(data["results"], list)
    assert len(data["results"]) == 10
    assert "count" in data
    assert isinstance(data["count"], int)

def test_invalid_endpoint():
    """存在しないエンドポイントへのアクセス"""
    response = client.get("/gacha/unknown")
    assert response.status_code == 404

def test_method_not_allowed():
    """許可されていないHTTPメソッドでのアクセス"""
    response = client.post("/gacha/single")
    assert response.status_code == 405

# --- 天井システムとカウンターリセットのテスト ---

def test_tenjo_system_in_single_gacha(monkeypatch):
    """天井直前(89)で単発ガチャを引くと、Sランクが出てカウンターが0になる"""
    # mainモジュールのグローバル変数 gacha_counter の値を89に設定
    monkeypatch.setattr("main.gacha_counter", 89)

    response = client.get("/gacha/single")
    data = response.json()

    assert response.status_code == 200
    assert data["result"] == "S"  # 天井機能によりSが確定
    assert data["count"] == 0      # カウンターがリセットされる

@patch("main.roll_gacha", return_value="A")
def test_tenjo_system_in_ten_gacha(mock_roll_gacha, monkeypatch):
    """天井に近い状態(85)で10連ガチャを引くと、途中でSが出てカウンターがリセットされる"""
    # カウンターを85に設定
    monkeypatch.setattr("main.gacha_counter", 85)

    response = client.get("/gacha/ten")
    data = response.json()

    assert response.status_code == 200
    results = data["results"]
    
    # 5回目のガチャ(85+5=90)で天井に到達するため、結果は"S"になる
    assert results[4] == "S"
    
    # 天井Sの後は通常のガチャ結果("A"に固定)
    assert results[5:] == ["A"] * 5
    
    # カウンターはSが出た後にリセットされ、残り5回分(6~10回目)がカウントされる
    assert data["count"] == 5
    
    # roll_gachaは9回呼ばれる（天井Sの1回はroll_gachaを呼ばないため）
    assert mock_roll_gacha.call_count == 9

@patch("main.roll_gacha", return_value="S")
def test_s_rank_resets_counter_in_single_gacha(mock_roll_gacha, monkeypatch):
    """単発ガチャでSランクが出るとカウンターがリセットされる"""
    # カウンターを50に設定
    monkeypatch.setattr("main.gacha_counter", 50)

    response = client.get("/gacha/single")
    data = response.json()

    assert response.status_code == 200
    assert data["result"] == "S"  # モックによりSが返される
    assert data["count"] == 0      # Sが出たのでカウンターがリセット
    mock_roll_gacha.assert_called_once()

@patch("main.roll_gacha")
def test_s_rank_resets_counter_in_ten_gacha(mock_roll_gacha, monkeypatch):
    """10連ガチャの途中でSランクが出るとカウンターがリセットされる"""
    # カウンターを20に設定
    monkeypatch.setattr("main.gacha_counter", 20)

    # roll_gachaの3回目の呼び出しで"S"を、それ以外では"A"を返すように設定
    mock_roll_gacha.side_effect = ["A", "A", "S", "A", "A", "A", "A", "A", "A", "A"]

    response = client.get("/gacha/ten")
    data = response.json()

    assert response.status_code == 200
    results = data["results"]
    assert "S" in results
    
    s_index = results.index("S")  # Sが出た位置（インデックスは2）
    
    # カウンターはSが出た後にリセットされ、残りのガチャ回数(10 - (2+1) = 7)が最終カウントとなる
    assert data["count"] == 10 - (s_index + 1)

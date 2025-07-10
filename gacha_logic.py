import random

def roll_gacha(prizes):
    if not prizes:
        raise ValueError("prizesリストが空です")
    total_rate = sum(p["rate"] for p in prizes)
    if not abs(total_rate - 1.0) < 1e-8:
        raise ValueError("rateの合計が1.0ではありません")
    for prize in prizes:
        if prize["rate"] < 0 or prize["rate"] > 1:
            raise ValueError("rateは0以上1以下でなければなりません")
    rand = random.random()
    total = 0.0
    for prize in prizes:
        total += prize["rate"]
        if rand < total:
            return prize["rank"]
    return prizes[-1]["rank"]

def force_s():
    return "S"
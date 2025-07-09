import random

def roll_gacha(prizes):
    rand = random.random()
    total = 0.0
    for prize in prizes:
        total += prize["rate"]
        if rand < total:
            return prize["rank"]
    return prizes[-1]["rank"]

def force_s():
    return "S"
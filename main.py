from fastapi import FastAPI
from gacha_logic import roll_gacha, force_s
from typing import List

app = FastAPI()

PRIZES = [
    {"rank": "S", "rate": 0.05},
    {"rank": "A", "rate": 0.10},
    {"rank": "B", "rate": 0.20},
    {"rank": "C", "rate": 0.65},
]

# グローバルなカウンター
gacha_counter = 0
TENJO = 90

@app.get("/gacha/single")
def single_gacha():
    global gacha_counter
    gacha_counter += 1

    # 天井判定
    if gacha_counter >= TENJO:
        result = force_s()
        gacha_counter = 0
    else:
        result = roll_gacha(PRIZES)
        if result == "S":
            gacha_counter = 0

    return {"result": result, "count": gacha_counter}

@app.get("/gacha/ten")
def ten_gacha():
    global gacha_counter
    results: List[str] = []
    for _ in range(10):
        gacha_counter += 1
        # 天井判定
        if gacha_counter >= TENJO:
            results.append(force_s())
            gacha_counter = 0
        else:
            prize = roll_gacha(PRIZES)
            results.append(prize)
            if prize == "S":
                gacha_counter = 0
    return {"results": results, "count": gacha_counter}
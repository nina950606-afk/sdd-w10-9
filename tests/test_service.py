"""0B 負責：商業規則層（service.py）的測試。

上面兩個是老師的範例；請在「第一輪」「第二輪」下面加上你的測試。
提示：service 的每個函式都回傳 {"ok": ..., "message": ..., "data": ...}，大多只要檢查 ["ok"]。
"""
import pytest

import service


# ---------------- 範例（老師提供）----------------
def test_report_found_normal(db):
    assert service.report_found(db, "雨傘", "圖書館")["ok"] is True


@pytest.mark.parametrize("item_id, claimer, expected_ok", [
    (1, "王小明", True),      # 正常：認領 1 號
    (99, "王小明", False),    # 錯誤：沒有 99 號
])
def test_claim(sample_db, item_id, claimer, expected_ok):
    assert service.claim(sample_db, item_id, claimer)["ok"] is expected_ok


# ---------------- 第一輪：請從這裡開始加 ----------------
@pytest.mark.parametrize("category, location, expected_ok", [
    ("雨傘", "圖書館", True),
    ("飛機", "圖書館", False),
    ("雨傘", None, False),
    ("雨傘", "月球", False),
])
def test_report_found_cases(db, category, location, expected_ok):
    res = service.report_found(db, category, location)
    assert res["ok"] is expected_ok


def test_claim_without_id_fails(sample_db):
    res = service.claim(sample_db, None, "王小明")
    assert res["ok"] is False


def test_search_umbrella_count(sample_db):
    res = service.search(sample_db, "雨傘", None)
    assert res["ok"] is True
    assert len(res["data"]["items"]) == 2

# ---------------- 第二輪：邊界與錯誤情況 ----------------
@pytest.mark.parametrize("desc_len, expected_ok", [
    (50, True),     # 邊界：剛好 50 字可登記
    (51, False),    # 邊界：超過 50 字（51 字）失敗
    (120, False),   # 邊界：遠超 50 字失敗
])
def test_report_found_description_length_boundary(db, desc_len, expected_ok):
    res = service.report_found(db, "水壺", "教室", "藍" * desc_len)
    assert res["ok"] is expected_ok


@pytest.mark.parametrize("claimer", ["", "   ", None])
def test_claim_invalid_claimer_fails(sample_db, claimer):
    assert service.claim(sample_db, 1, "王小明")["ok"] is True
    assert service.claim(sample_db, 2, "王小明")["ok"] is True
    assert service.claim(sample_db, 3, "王小明")["ok"] is False
    res = service.claim(sample_db, 1, claimer)
    assert res["ok"] is False
"""0A 負責：資料存取層（repository.py）的測試。

上面兩個是老師的範例；請在「第一輪」「第二輪」下面加上你的測試。
提示：sample_db 裡有 1 號雨傘（圖書館）、2 號水壺（餐廳）、3 號雨傘（教室）。
"""
import pytest

import repository


# ---------------- 範例（老師提供）----------------
def test_add_item_returns_new_id(db):
    assert repository.add_item(db, "雨傘", "圖書館", "黑傘") == 1


def test_get_item_not_found_returns_none(db):
    assert repository.get_item(db, 99) is None


# ---------------- 第一輪：請從這裡開始加 ----------------
def test_get_item_2_is_bottle(sample_db):
    item = repository.get_item(sample_db, 2)
    assert item["category"] == "水壺"
    assert item["location"] == "餐廳"
    assert item["status"] == "待認領"


def test_find_umbrellas(sample_db):
    ids = [it["id"] for it in repository.find_items(sample_db, category="雨傘")]
    assert ids == [1, 3]


def test_mark_claimed_returns_true(sample_db):
    assert repository.mark_claimed(sample_db, 1, "王小明") is True


def test_mark_claimed_changes_status(sample_db):
    repository.mark_claimed(sample_db, 1, "王小明")
    assert repository.get_item(sample_db, 1)["status"] == "已認領"


# ---------------- 第二輪：邊界與錯誤情況 ----------------


# 已認領的東西，查詢時不應該出現
def test_claimed_item_not_in_find(sample_db):
    repository.mark_claimed(sample_db, 1, "王小明")
    ids = [it["id"] for it in repository.find_items(sample_db, category="雨傘")]
    assert ids == [3]


# 同一件不能被標記兩次，認領人不會被換掉
def test_mark_claimed_twice_fails(sample_db):
    assert repository.mark_claimed(sample_db, 1, "王小明") is True
    assert repository.mark_claimed(sample_db, 1, "李小華") is False
    assert repository.get_item(sample_db, 1)["claimer"] == "王小明"


# 標記不存在的編號會失敗
def test_mark_claimed_not_found(sample_db):
    assert repository.mark_claimed(sample_db, 99, "王小明") is False


# 同時給類別和地點
@pytest.mark.parametrize("category, location, expected", [
    ("雨傘", "教室", [3]),
    ("雨傘", "餐廳", []),
    (None, "餐廳", [2]),
    (None, None, [1, 2, 3]),
])
def test_find_by_category_and_location(sample_db, category, location, expected):
    ids = [it["id"] for it in repository.find_items(sample_db, category=category, location=location)]
    assert ids == expected


# 認領過的人和沒認領過的人
def test_count_claimed_by(sample_db):
    repository.mark_claimed(sample_db, 1, "王小明")
    repository.mark_claimed(sample_db, 3, "王小明")
    assert repository.count_claimed_by(sample_db, "王小明") == 2
    assert repository.count_claimed_by(sample_db, "李小華") == 0


# 統計表：沒有物品的類別也要列出
def test_stats_empty_category_listed(sample_db):
    stats = {r["類別"]: r for r in repository.category_stats(sample_db)}
    assert stats["鑰匙"]["總件數"] == 0
    assert stats["鑰匙"]["待認領"] == 0
    assert stats["鑰匙"]["已認領"] == 0


# 統計表：雨傘那一列
def test_stats_umbrella_row(sample_db):
    repository.mark_claimed(sample_db, 1, "王小明")
    stats = {r["類別"]: r for r in repository.category_stats(sample_db)}
    assert stats["雨傘"]["總件數"] == 2
    assert stats["雨傘"]["待認領"] == 1
    assert stats["雨傘"]["已認領"] == 1

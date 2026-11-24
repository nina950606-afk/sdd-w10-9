"""0D（加分題 A）：整合測試。從「一句話」經過假 AI，一路測到資料庫。

上面是老師的範例；請加上你的測試。
"""
import service


# ---------------- 範例（老師提供）----------------
def test_register_by_sentence(db, fake_ai):
    ask = fake_ai({"我在餐廳撿到一張學生證": "登記|學生證|餐廳"})
    result = service.handle_message(db, "我在餐廳撿到一張學生證", "", ask)
    assert result["ok"] is True


# ---------------- 請從這裡開始加 ----------------
def test_query_after_register_integration(db, fake_ai):
    reg_ask = fake_ai({"我在圖書館撿到一把雨傘": "登記|雨傘|圖書館"})
    reg_res = service.handle_message(db, "我在圖書館撿到一把雨傘", "", reg_ask)
    assert reg_res["ok"] is True

    query_ask = fake_ai({"幫我查圖書館的雨傘": "查詢|雨傘|圖書館"})
    query_res = service.handle_message(db, "幫我查圖書館的雨傘", "", query_ask)
    assert query_res["ok"] is True
    assert "雨傘" in query_res["reply"]


def test_claim_item_integration(db, fake_ai):
    reg_ask = fake_ai({"我在教室撿到一個錢包": "登記|錢包|教室"})
    reg_res = service.handle_message(db, "我在教室撿到一個錢包", "", reg_ask)
    assert reg_res["ok"] is True

    claim_ask = fake_ai({"我要認領 1 號": "認領|未知|未知"})
    claim_res = service.handle_message(db, "我要認領 1 號", "", claim_ask)
    assert claim_res["ok"] is True
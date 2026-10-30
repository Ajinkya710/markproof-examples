"""Offline tests: no network, no API key needed. Run with `pytest`."""

import hashlib
import hmac
import json
import os
import time
from types import SimpleNamespace

os.environ.setdefault("MARKPROOF_API_KEY", "lt_live_test")
os.environ.setdefault("MARKPROOF_WEBHOOK_SECRET", "whsec_test")

from fastapi.testclient import TestClient  # noqa: E402

import main  # noqa: E402

client = TestClient(main.app)


def test_generate_returns_the_marked_file(monkeypatch):
    def fake_mark(data, **kwargs):
        assert kwargs["generator_name"] == "my-fastapi-app"
        return SimpleNamespace(file=b"marked-bytes", content_type="image/png",
                               verify_url="https://markproof.co/v/ABCD1234", watermark_code="ABCD1234")

    monkeypatch.setattr(main.markproof, "mark", fake_mark)
    r = client.post("/generate", params={"prompt": "a cat"}, files={"file": ("a.png", b"png", "image/png")})
    assert r.status_code == 200
    assert r.content == b"marked-bytes"
    assert r.headers["x-watermark-code"] == "ABCD1234"


def _event():
    return {
        "id": "evt_1", "type": "batch.completed", "created": int(time.time()),
        "data": {
            "id": "b1", "status": "completed", "created_at": "2026-10-30T12:00:00Z", "completed_at": "2026-10-30T12:01:00Z",
            "generator_name": None, "model_name": None,
            "counts": {"total": 1, "queued": 0, "processing": 0, "completed": 1, "failed": 0},
            "webhook": {"url": "https://example.com/hook", "status": "pending", "attempts": 1, "last_status": None, "delivered_at": None},
            "items": [{"index": 0, "status": "completed", "filename": "a.png", "source_url": None, "asset_id": "a1",
                       "watermark_code": "ABCD1234", "kind": "image", "verify_url": "https://markproof.co/v/ABCD1234",
                       "watermark_robust": True, "c2pa_manifest_label": "urn:c2pa:x", "file_url": "https://signed", "error": None}],
        },
    }


def _signed(body: str, secret: str = "whsec_test") -> dict:
    t = int(time.time())
    sig = hmac.new(secret.encode(), f"{t}.{body}".encode(), hashlib.sha256).hexdigest()
    return {"Markproof-Signature": f"t={t},v1={sig}", "Content-Type": "application/json"}


def test_webhook_accepts_a_signed_event():
    body = json.dumps(_event())
    r = client.post("/webhooks/markproof", content=body, headers=_signed(body))
    assert r.status_code == 200 and r.json() == {"received": True}


def test_webhook_rejects_a_bad_signature():
    body = json.dumps(_event())
    r = client.post("/webhooks/markproof", content=body, headers=_signed(body, "whsec_wrong"))
    assert r.status_code == 400

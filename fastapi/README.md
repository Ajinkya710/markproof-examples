# FastAPI + Markproof

Mark every image your API generates (invisible watermark + signed C2PA Content Credentials, for EU AI Act Article 50), and receive batch results by signed webhook.

```bash
pip install -r requirements.txt
export MARKPROOF_API_KEY=lt_live_...          # https://markproof.co/dashboard
export MARKPROOF_WEBHOOK_SECRET=whsec_...     # dashboard → Webhook signing secret
uvicorn main:app --reload
```

Try it:

```bash
curl -F "file=@cat.png" "http://localhost:8000/generate?prompt=a+cat" -o cat.marked.png -D -
```

The response is the marked PNG; `X-Verify-Url` is a public page anyone can open to check it. Drop the file into the [free checker](https://markproof.co/check) to see both marks.

- `POST /generate`: replace `generate_image()` with your model call. Marking is one `markproof.mark(...)` call; pass `visible_label=True` to add a visible "AI-generated" label too.
- `POST /webhooks/markproof`: point a batch's `webhook_url` here. It verifies the `Markproof-Signature` header against the **raw** body before trusting anything.

Tests run offline (no key, no network): `pip install pytest httpx && pytest`.

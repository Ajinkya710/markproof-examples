"""
FastAPI + Markproof: mark every image your app generates, and receive batch
results by webhook.

    pip install -r requirements.txt
    export MARKPROOF_API_KEY=lt_live_...          # markproof.co/dashboard
    export MARKPROOF_WEBHOOK_SECRET=whsec_...     # dashboard, for /webhooks/markproof
    uvicorn main:app --reload
"""

import os

from fastapi import FastAPI, File, HTTPException, Request, UploadFile
from fastapi.responses import Response
from markproof import Markproof, MarkproofError, WebhookSignatureError, parse_webhook_event

app = FastAPI(title="Markproof FastAPI example")
markproof = Markproof(api_key=os.environ["MARKPROOF_API_KEY"])


def generate_image(prompt: str, upload: bytes) -> bytes:
    """Stand-in for your model. Here it just returns the uploaded image."""
    return upload


@app.post("/generate")
async def generate(prompt: str, file: UploadFile = File(...)) -> Response:
    image = generate_image(prompt, await file.read())

    # One call: invisible watermark + signed C2PA manifest (EU AI Act Art. 50).
    try:
        marked = markproof.mark(
            image,
            filename=file.filename or "image.png",
            generator_name="my-fastapi-app",
            model_name="my-model-v1",
            # visible_label=True,  # optional "AI-generated" label (Art. 50(4) deepfakes)
        )
    except MarkproofError as e:
        raise HTTPException(502, f"Marking failed: {e}") from e

    # Store marked.watermark_code / marked.asset_id next to your own record if you
    # want to look the file up later; anyone can check it at marked.verify_url.
    return Response(
        content=marked.file,
        media_type=marked.content_type,
        headers={"X-Verify-Url": marked.verify_url, "X-Watermark-Code": marked.watermark_code},
    )


@app.post("/webhooks/markproof")
async def markproof_webhook(request: Request) -> dict:
    """Receives batch.completed events (POST /v1/batches with webhook_url)."""
    body = await request.body()  # the raw bytes: re-serialized JSON won't verify
    try:
        event = parse_webhook_event(
            body,
            request.headers.get("Markproof-Signature"),
            os.environ["MARKPROOF_WEBHOOK_SECRET"],
        )
    except WebhookSignatureError:
        raise HTTPException(400, "invalid signature")

    batch = event.data
    for item in batch.items:
        if item.file_url:
            print(f"marked: {item.watermark_code} -> {item.file_url}")  # download promptly; links expire
        else:
            print(f"failed: {item.error}")
    return {"received": True}

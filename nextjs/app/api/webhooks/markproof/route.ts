import { parseWebhookEvent, WebhookSignatureError } from "markproof";

/** Receives batch.completed events from POST /v1/batches (set its webhook_url to this route). */
export async function POST(request: Request): Promise<Response> {
  const payload = await request.text(); // the raw body: re-serialized JSON won't verify
  let event;
  try {
    event = parseWebhookEvent({
      payload,
      header: request.headers.get("markproof-signature"),
      secret: process.env.MARKPROOF_WEBHOOK_SECRET!,
    });
  } catch (err) {
    if (err instanceof WebhookSignatureError) return new Response("invalid signature", { status: 400 });
    throw err;
  }

  for (const item of event.data.items) {
    if (item.fileUrl) console.log(`marked ${item.watermarkCode}: ${item.fileUrl}`); // download promptly; links expire
    else console.log(`failed: ${item.error}`);
  }
  return Response.json({ received: true });
}

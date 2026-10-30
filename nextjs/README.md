# Next.js + Markproof

Mark AI-generated images from a Next.js (App Router) app: invisible watermark + signed C2PA Content Credentials in one call, for EU AI Act Article 50. Includes a signed-webhook receiver for batch jobs.

```bash
npm install
cp .env.example .env.local   # add MARKPROOF_API_KEY from https://markproof.co/dashboard
npm run dev                  # http://localhost:3000
```

- `app/api/mark/route.ts`: the integration. One `markproof.mark(...)` call on the server; the key never reaches the browser. Call it wherever your model returns an image.
- `app/api/webhooks/markproof/route.ts`: receives `batch.completed` events and verifies the `Markproof-Signature` header against the raw body.
- `app/page.tsx`: a small upload form to try it.

Check any result in the [free checker](https://markproof.co/check). API reference: [markproof.co/docs](https://markproof.co/docs).

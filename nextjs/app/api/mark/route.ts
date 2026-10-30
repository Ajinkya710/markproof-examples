import { Markproof, MarkproofError } from "markproof";

// Server-only: the API key never reaches the browser. Created on first use,
// not at import, so `next build` works without the key set.
let markproof: Markproof | undefined;
const client = () => (markproof ??= new Markproof({ apiKey: process.env.MARKPROOF_API_KEY! }));

/**
 * POST a generated image as multipart `file`; get it back marked with an
 * invisible watermark + signed C2PA manifest (EU AI Act Article 50).
 * In a real app you'd call this right after your model returns an image.
 */
export async function POST(request: Request): Promise<Response> {
  const form = await request.formData();
  const file = form.get("file");
  if (!(file instanceof File)) {
    return Response.json({ error: "Send an image as `file`." }, { status: 400 });
  }

  try {
    const marked = await client().mark(
      { data: Buffer.from(await file.arrayBuffer()), filename: file.name },
      {
        generatorName: "my-nextjs-app",
        modelName: "my-model-v1",
        visibleLabel: form.get("label") === "on" ? true : undefined, // optional visible "AI-generated" label
      },
    );
    return new Response(new Uint8Array(marked.file!), {
      headers: {
        "content-type": marked.contentType!,
        "x-verify-url": marked.verifyUrl,
        "x-watermark-code": marked.watermarkCode,
      },
    });
  } catch (err) {
    const message = err instanceof MarkproofError ? err.message : "Marking failed.";
    return Response.json({ error: message }, { status: 502 });
  }
}
